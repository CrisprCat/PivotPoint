import streamlit as st
from modules.functions import Navbar
from modules.functions import footer
from scipy.stats import chisquare
import statsmodels.stats.proportion as pp
import pandas as pd
import matplotlib.pyplot as plt

def main():
    Navbar()

st.title("Statistical significance tester")
st.caption('''You can use this calculator to test if your experiment result is statistically significant.''')

with st.container():
    st.header("Binary metric (Conversion rate)")
    st.subheader("Please input your data:")
    col1, col2, col3 = st.columns(3)
    with col1:
        power = st.number_input('Desired statistical power'
                                        , min_value = 0.00
                                        , max_value = 1.00
                                        , value = 0.8
                                        , step = 0.05
                                        , help = '''1 - \u03B2: The probability to detect an effect when it is truly there.    
                                        \u03B2 is the probability of maikng a type II error (false negative).'''
                                        )
        if power < 0.8:
            st.warning('⚠️ This statistical power is considered low!')
        mde = st.number_input('Pre-calculate MDE'
                              , min_value = 0.00
                              , max_value = 100.00
                              , value = None
                              , placeholder = 'Enter MDE in %'
                              , help = '''Your MDE should have a business relevant value.''' )
        
    with col2:
        alpha = st.number_input('Statistical significance level'
                                , value = 0.05
                                , min_value = 0.05
                                , max_value = 1.00
                                , step = 0.05
                                , help = '\u03B1: The probability of rejecting a null hypothesis, given that it is true'
                                )
        if alpha > 0.1:
            st.warning('⚠️ This statistical significance level is considered high!')

    with col3:
        test_type = st.radio("Hypothesis type"
                             , ["One-sided", "Two-sided"]
                             , help = '''Use one-sided when you want to detect an effect in a specific direction (increase or decrease).  
                             Use two-sided when you want to detect an effect in either direction. ''')

with st.container():
    st.subheader("Control")
    col1, col2, col3 = st.columns(3)
    with col1:
        Visits_control = st.number_input('Number of visits'
                                         , min_value = 1
                                         , max_value = None
                                         , value = None
                                         , step = 1
                                         , help = '''Enter the number of visits that you had in the control'''
                                         , placeholder = 'Enter a number'
                                         )
    with col2:
        Orders_control = st.number_input('Number of orders'
                                         , min_value = 1
                                         , max_value = None
                                         , value = None
                                         , step = 1
                                         , help = '''Enter the number of orders that you had in the control'''
                                         , placeholder = 'Enter a number'
                                         )
    with col3:
        if Visits_control != None and Orders_control != None:
            CR_control = Orders_control / Visits_control * 100
            st.metric("Control Conversion Rate"
                      , value = f"{round(CR_control, 2)} %")
            
with st.container():
    st.subheader("Variant")
    col1, col2, col3 = st.columns(3)
    with col1:
        Visits_variant = st.number_input('Number of visits'
                                         , min_value = 1
                                         , max_value = None
                                         , value = None
                                         , step = 1
                                         , help = '''Enter the number of visits that you had in the variant'''
                                         , placeholder = 'Enter a number'
                                         )
    with col2:
        Orders_variant = st.number_input('Number of orders'
                                         , min_value = 1
                                         , max_value = None
                                         , value = None
                                         , step = 1
                                         , help = '''Enter the number of orders that you had in the variant'''
                                         , placeholder = 'Enter a number'
                                         )
    with col3:
        if Visits_variant != None and Orders_variant != None:
            CR_variant = Orders_variant / Visits_variant * 100
            st.metric("Variant Conversion Rate"
                      , value = f"{round(CR_variant, 2)} %")
            
## SRM check of input data
    if Visits_control != None and Visits_variant != None:
        sample_sizes = [Visits_control, Visits_variant]
        SRM_result = chisquare(sample_sizes
                               , f_exp = None)
        if SRM_result.pvalue < 0.1:
            st.warning(f"""With a p-value smaller than 0.1 ({round(SRM_result.pvalue, 3)}) a possible SRM is detected. Please check your data collection process before analysing the test results.""")


        with st.container():
            col1, col2, col3 = st.columns(3)
            if Visits_control != None and Orders_control != None and Visits_variant != None and Orders_variant != None:
                # Calculate summary
                diff = CR_variant - CR_control
                lift = diff / CR_control * 100

                # Determine Hypothesis type
                if test_type == 'One-sided' and diff < 0:
                    hypo_type = 'larger'
                elif test_type == 'One-sided' and diff > 0:
                    hypo_type = 'smaller'
                else:
                    hypo_type = 'two-sided'
                
                # Statistical hypothesis test
                stat, pval = pp.proportions_ztest(count = [Orders_control, Orders_variant]
                                                  , nobs = sample_sizes
                                                  , alternative = hypo_type
                                                  )
                if pval > alpha:
                    st.warning(f"""With a p-value of {round(pval, 3)} your result is not statistically significant.""")
                else:
                    st.success(f"""With a p-value of {round(pval, 3)} your result is statistically significant.""")

                
                # # Confidence interval
                # ## If you expect a positive result the CI should not cover 0
                # ## The CI should be narrow around your MDE
                # ### Rule of thumb: Narrow means estimated_effect_size in percent points +/- 1/2 MDE in percent points
                # ci_low, ci_upp = pp.confint_proportions_2indep(count1 = Orders_variant
                #                                                , nobs1 = Visits_variant
                #                                                , count2 = Orders_control
                #                                                , nobs2 = Visits_variant
                #                                                , method = 'score' # Alternatives: 'wald', 'agrestio-caffo', 'newcomb', 'score'
                #                                                , compare = 'diff'
                #                                                , alpha = alpha
                #                                                , correction = True)
                
                # exp_low = diff - 0.5 * diff
                # exp_upp = diff + 0.5 * diff

                # # Create a dataframe
                # names = ['ci', 'ci', 'exp', 'exp']
                # borders = [ci_low*100, ci_upp*100, exp_low, exp_upp]

                # # Creating DataFrame from lists
                # df = pd.DataFrame({'Name': names, 'Border': borders})
                # print(df)

                # # Define a figure object
                # fig = plt.figure(figsize=(8, 6), dpi=100)
                # plt.scatter(df['Border'], df['Name'])
 
                # # Adding Title to the Plot
                # plt.title("Scatter Plot")

                # # Setting the X and Y labels
                # plt.xlabel('Name')
                # plt.ylabel('Border')

                # # Adding a red vertical line at Border value 0
                # plt.axvline(x=0, color='red', linestyle='--')

                # plt.show()


                # st.scatter_chart(df
                #                  , x = 'Border'
                #                  , y = 'Name')
                
                
                # st.pyplot(fig=fig)
                
                # # Output
                # with col1:
                #     st.metric("Lift"
                #               , value = f"{round(lift, 2)} %"
                #               )
                #     st.metric("CI low"
                #               , value = f"{round(ci_low * 100, 5)}"
                #               )
                #     st.metric("CI low exp"
                #               , value = f"{round(exp_low, 5)}"
                #               )
                    
                # with col2:    
                #     st.metric("Difference"
                #               , value = f"{round(diff, 2)} PP"
                #               , help = 'PP = Percent points'
                #               )
                #     st.metric("CI upp"
                #               , value = f"{round(ci_upp * 100, 5)}"
                #               )
                #     st.metric("CI upp exp"
                #               , value = f"{round(exp_upp, 5)}"
                #               )  

                # with col3:
                #     st.metric("p-value"
                #               , value = f"{round(pval, 5)}"
                #               ) 
                 
                    


if __name__ == '__main__':
    main()
    footer()