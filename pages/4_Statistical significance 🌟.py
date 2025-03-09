import streamlit as st
from modules.functions import Navbar
from modules.functions import footer
from scipy.stats import chisquare
import statsmodels.stats.proportion as pp
import statsmodels.stats.power as pw
import pandas as pd
from modules.stat_functions import check_numeric_columns
from modules.stat_functions import check_value_size
from statsmodels.stats.weightstats import ttest_ind

st.set_page_config(
    page_title="CRO Calculators"
    , page_icon="pictures\Favicon.png"
    , layout="centered"
    , initial_sidebar_state="auto"
    , menu_items=None
    )
# hide burger menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def main():
    Navbar()

    st.title("Statistical hypothesis tester")
    st.caption(
        '''You can use this calculator to test if your experiment result is statistically significant.  
        If you ran an experiment with multiple variants this calculator uses Bonferroni correction to correct for multiple comparisons. Comparisons are only done between the control and each variant. This calculator does not compare the variants with each other.'''
        )

# Statistical parameter
    with st.container():
        st.header('Statistical parameter')

        col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="bottom")

        with col1:
            power = st.number_input(
                'Statistical power'
                , value = 0.80
                , min_value = 0.05
                , max_value = 1.00
                , step = 0.05
                , help = '''1 - \u03B2: The probability to detect an effect that is truly there.  
                \u03B2 is the probability of making a type II error (false negative).'''
                )
            if power < 0.8:
                st.warning('⚠️ This statistical power is considered low!')
        
        with col2:
            alpha = st.number_input(
                'Statistical significance level'
                , value = 0.05
                , min_value = 0.05
                , max_value = 1.00
                , step = 0.05
                , help = '\u03B1: The probability of rejecting a null hypothesis, given that it is true.'
                )
            if alpha >= 0.1:
                st.warning('⚠️ This statistical significance level is considered high!')
        
        with col3:
            num_of_variants = st.number_input(
                'Number of variants'
                , min_value = 1
                , max_value = None
                , value = 1
                , step = 1
                , help = '''For multiple variants this calculator uses Bonferroni correction.      
                This calculator assumes only comparisons between control and each variant.  
                It does not compare the variants with each other.'''
                )
        
        with col4:
            test_type = st.radio(
                "Hypothesis type"
                , ["Two-sided", "One-sided"]
                , help = '''Use one-sided when you want to detect an effect in a specific direction (increase or decrease).  
                Use two-sided when you want to detect an effect in either direction. ''')
            if test_type == 'One-sided':
                test_type = st.radio(
                    "Hypothesis direction"
                    , ["Larger", "Smaller"]
                    , help = '''Choose "Larger" when you want to detect an uplift in the conversion rate.  
                    Choose "Smaller" when you want to detect a downlift in the conversion rate.''')
            hypo_type = test_type.lower()

# Binomial metric
    with st.container():
        st.header("Binomial metric (Conversion rate)")
        st.subheader("Please input your data:")
        
        # Control
        with st.container():
            st.subheader("Control")
            
            col1, col2, col3 = st.columns(3)
            
            # Input
            with col1:
                Visitors_control = st.number_input(
                    'Number of visitors'
                    , min_value = 1
                    , max_value = None
                    , value = None
                    , step = 1
                    , help = '''Enter the number of visitors that you had in the control'''
                    , placeholder = 'Enter a number'
                    )
            
            with col2:
                Orders_control = st.number_input(
                    'Number of orders'
                    , min_value = 1
                    , max_value = None
                    , value = None
                    , step = 1
                    , help = '''Enter the number of orders that you had in the control'''
                    , placeholder = 'Enter a number'
                    )
            
            # Output
            with col3:
                if Visitors_control != None and Orders_control != None:
                    if Orders_control > Visitors_control:
                        st.error(
                            "You shouldn't have more conversions than visitors."
                            , icon = '🚨')
                    elif Orders_control == Visitors_control:
                        st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
                    else:
                        CR_control = Orders_control / Visitors_control
                        CR_control_perc = CR_control * 100
                        st.metric(
                            "Control conversion rate"
                            , value = f"{round(CR_control_perc, 2)} %")

        # Variant            
        with st.container():
            Visitors_variants = []
            Orders_variants = []
            CR_variants = []
            CR_variants_perc = []
            # Create entry fields dynamically
            for i in range(1, num_of_variants + 1):
                st.subheader(f'''Variant {i}''')

                col1, col2, col3 = st.columns(3)

                # Input
                with col1:
                    Visitors_variant = st.number_input(
                        'Number of visitors'
                        , key = f"visitors_{i+1}"
                        , min_value = 1
                        , max_value = None
                        , value = None
                        , step = 1
                        , help = '''Enter the number of visitors that you had in the variant'''
                        , placeholder = 'Enter a number'
                        )
                    Visitors_variants.append(Visitors_variant)

                with col2:
                    Orders_variant = st.number_input(
                        'Number of orders'
                        , key = f"orders_{i+1}"
                        , min_value = 1
                        , max_value = None
                        , value = None
                        , step = 1
                        , help = '''Enter the number of orders that you had in the variant'''
                        , placeholder = 'Enter a number'
                        )
                    Orders_variants.append(Orders_variant)

                # Output    
                with col3:
                    if Visitors_variant != None and Orders_variant != None:
                        if Orders_variant > Visitors_variant:
                            st.error(
                                "You shouldn't have more conversions than visitors."
                                , icon = '🚨')
                        elif Orders_variant == Visitors_variant:
                            st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
                        else:
                            CR_variant = Orders_variant / Visitors_variant
                            CR_variant_perc = CR_variant * 100
                            st.metric(
                                "Variant conversion rate"
                                , value = f"{round(CR_variant_perc, 2)} %"
                                )
                            CR_variants.append(CR_variant)
                            CR_variants_perc.append(CR_variant_perc)

            ## SRM check of input data
                if Visitors_control != None and Visitors_variant != None:
                    sample_sizes = [Visitors_control, Visitors_variant]
                    SRM_result = chisquare(
                        sample_sizes
                        , f_exp = None
                        )
                    if SRM_result.pvalue < 0.1:
                        st.warning(f"""With a p-value smaller than 0.1 ({round(SRM_result.pvalue, 3)}) a possible SRM between control and this variant is detected. Please check your data collection process before analysing the test results.""")

                # Result output
                with st.container():
                    col1, col2, col3 = st.columns(3)
                    if Visitors_control != None and Orders_control != None and Visitors_variant != None and Orders_variant != None:
                        # Calculate summary
                        differences = []
                        for i in CR_variants_perc:
                            diff = CR_variant_perc - CR_control_perc
                            differences.append(diff)
                        changes = []
                        for i in differences:
                            change = diff / CR_control_perc * 100
                            changes.append(change)

                            # Statistical hypothesis test
                        stat, pval = pp.proportions_ztest(
                            count = [Orders_control, Orders_variant]
                            , nobs = sample_sizes
                            , alternative = hypo_type
                            )
                        
                        # Output
                        with col1:
                            st.metric(
                                "Change"
                                , value = f"{round(change, 2)} %"
                                )
                        with col2:    
                            st.metric(
                                "Difference"
                                , value = f"{round(diff, 2)} PP"
                                , help = 'PP = Percent points'
                                )
                        with col3:
                            st.metric(
                                "p-value"
                                , value = f"{round(pval, 3)}"
                                )

                        if pval > alpha/num_of_variants:
                            st.warning(f"""With a p-value of {round(pval, 3)} your result is not statistically significant.""")
                        else:
                            st.success(f"""With a p-value of {round(pval, 3)} your result is statistically significant.""")

                        # Determine post-hoc power. Careful! This should not be your default wy to judge if your user reached their sample size. Just use it as a nudge
                        effect = pp.proportion_effectsize (
                            CR_control
                            , CR_variant
                            , method = "normal"
                            )

                        posthoc_power = pw.zt_ind_solve_power(
                            effect_size = effect
                            , nobs1 = Visitors_control
                            , alpha = alpha
                            , alternative = hypo_type
                            )
                        if posthoc_power < 0.8:
                            st.warning('''Did you reach your pre-calculated sample size?''')


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

# Continous metric
    with st.container():
        st.header("Continous metric (Revenue per visitor)")
        st.subheader("Please input your data:")
        st.markdown(
            """
            Upload your revenue data and enter the number of visitors.  
            Please upload one csv file for the control and each variant. The csv files should contain one column with the revenue data per order and one header cell.   
            """
        )

        # Control
        with st.container():
            st.subheader("Control")

            col1, col2 = st.columns([2,1], vertical_alignment = "bottom")

            # User input
            with col1:
                rpv_control_revenue = st.file_uploader(
                    label = "Revenue data"
                    , type = ['csv']
                    , help = '''Upload your test results (revenue data per order) for your control as a csv file.'''
                    )
            if rpv_control_revenue != None:
                rpv_control_revenue_df = pd.read_csv(
                    rpv_control_revenue
                    , header = 0
                    )
                # Sanity checks
                ## The column should only contain numeric values
                san_num = check_numeric_columns (rpv_control_revenue_df, [0])
                if san_num == False:
                    st.warning(
                        'It looks like your revenue data contains non-numeric values.'
                        , icon = '⚠️')
                else:
                    ## All values should be > 0    
                    san_zero = check_value_size(rpv_control_revenue_df, 0) 
                    if san_zero == False:
                        st.warning(
                            'It looks like you have orders with 0 € revenue or less.'
                            , icon = '⚠️'
                            )
                    else:
                        rpv_num_orders_control = len(rpv_control_revenue_df)

            with col2:
                rpv_control_visitors = st.number_input(
                    'Number of visitors'
                    , min_value = 1
                    , max_value = None
                    , value = None
                    , step = 1
                    , help = '''Enter the number of visitors that you had in the control.'''
                    , placeholder = 'Enter a number'
                    )
                                
            # Output
            with st.container():
                if rpv_control_revenue != None and rpv_control_visitors != None:
                    if rpv_num_orders_control > rpv_control_visitors:
                        st.error(
                            "You shouldn't have more conversions than visitors."
                            , icon = '🚨')
                    elif rpv_num_orders_control == rpv_control_visitors:
                        st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
                    else:
                        rpv_cr_control = rpv_num_orders_control / rpv_control_visitors
                        rpv_cr_control_perc = rpv_cr_control * 100

                        rpv_null_order_control = rpv_control_visitors - rpv_num_orders_control
                        rpv_control_full = pd.concat([rpv_control_revenue_df.squeeze(), pd.Series([0] * rpv_null_order_control)]).reset_index(drop=True)

                        rpv_control = rpv_control_full.mean(skipna = False)

                        col1, col2, col3 = st.columns(3)            
                        with col1:
                            st.data_editor(
                                data = rpv_control_revenue_df
                                , disabled = True
                            )
                        with col2:
                            st.metric(
                                "Control conversion rate"
                                , value = f"{round(rpv_cr_control_perc, 2)} %"
                                )
                        with col3:
                            st.metric(
                                "Control revenue per visitor"
                                , value = f"{round(rpv_control, 2)} €"
                            )

        # Variant
        with st.container():
            for i in range(1, num_of_variants + 1):
                st.subheader(f'''Variant {i}''')

                col1, col2 = st.columns([2,1], vertical_alignment = "bottom")

                # User Input
                with col1:
                    rpv_variant_revenue = st.file_uploader(
                        label = "Revenue data"
                        , key = f"revenue_{i+1}"
                        , type = ['csv']
                        , help = f'''Upload your test results (revenue data per order) for your variant {i} as a csv file.'''
                        )
                if rpv_variant_revenue != None:
                    rpv_variant_revenue_df = pd.read_csv(
                        rpv_variant_revenue
                        , header = 0
                        )
                    # Sanity checks
                    ## The column should only contain numeric values
                    san_num = check_numeric_columns (rpv_variant_revenue_df, [0])
                    if san_num == False:
                        st.warning(
                            'It looks like your revenue data contains non-numeric values.'
                            , icon = '⚠️')
                    else:
                        ## All values should be > 0  
                        san_zero = check_value_size(rpv_variant_revenue_df, 0) 
                        if san_zero == False:
                            st.warning(
                                'It looks like you have orders with 0 € revenue or less.'
                                , icon = '⚠️'
                                )
                        else:
                            rpv_num_orders_variant = len(rpv_variant_revenue_df)

                with col2:
                    rpv_variant_visitors = st.number_input(
                        'Number of visitors'
                        , key = f"rpv_variant_visitors_{i+1}"
                        , min_value = 1
                        , max_value = None
                        , value = None
                        , step = 1
                        , help = f'''Enter the number of visitors that you had in the variant {i}.'''
                        , placeholder = 'Enter a number'
                        )
                ## SRM check of input data
                if rpv_control_visitors != None and rpv_variant_visitors != None:
                    rpv_sample_sizes = [rpv_control_visitors, rpv_variant_visitors]
                    rpv_SRM_result = chisquare(
                        rpv_sample_sizes
                        , f_exp = None
                        )
                    if rpv_SRM_result.pvalue < 0.1:
                        st.warning(f"""With a p-value smaller than 0.1 ({round(rpv_SRM_result.pvalue, 3)}) a possible SRM between control and this variant is detected. Please check your data collection process before analysing the test results.""")
                
            # Output                    
            with st.container():
                if rpv_variant_revenue != None and rpv_variant_visitors != None:
                    if rpv_num_orders_variant > rpv_variant_visitors:
                        st.error(
                            "You shouldn't have more conversions than visitors."
                            , icon = '🚨')
                    elif rpv_num_orders_variant == rpv_variant_visitors:
                        st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
                    else:
                        rpv_cr_variant = rpv_num_orders_variant / rpv_variant_visitors
                        rpv_cr_variant_perc = rpv_cr_variant * 100

                        rpv_null_order_variant = rpv_variant_visitors - rpv_num_orders_variant
                        rpv_variant_full = pd.concat([rpv_variant_revenue_df.squeeze(), pd.Series([0] * rpv_null_order_variant)]).reset_index(drop=True)

                        rpv_variant = rpv_variant_full.mean(skipna = False)

                        col1, col2, col3 = st.columns(3)            
                        with col1:
                            st.data_editor(
                                data = rpv_variant_revenue_df
                                , key = f"rpv_data_variant_{i+1}"
                                , disabled = True
                            )
                        with col2:
                            st.metric(
                                f'''Variant {i} conversion rate'''
                                , value = f"{round(rpv_cr_variant_perc, 2)} %"
                                )
                        with col3:
                            st.metric(
                                f'''Variant {i} revenue per visitor'''
                                , value = f"{round(rpv_variant, 2)} €"
                            )
                
            # Result Output
            with st.container():
                if rpv_control_visitors != None and rpv_control_revenue != None and rpv_variant_visitors != None and rpv_variant_revenue != None:
                    rpv_diff = rpv_variant - rpv_control
                    rpv_change = rpv_diff / rpv_control * 100

                    #Statistical hypothesis test
                    tstat, pvalue, degf = ttest_ind(
                        rpv_control_full
                        , rpv_variant_full
                        , alternative = hypo_type
                        , usevar = 'pooled'
                        , weights = (None, None)
                        , value = 0
                    )
                    col1, col2, col3 = st.columns(3) 
                    # Output
                    with col1:
                        st.metric(
                            "Change"
                            , value = f"{round(rpv_change, 2)} %"
                            )
                    with col2:    
                        st.metric(
                            "Difference"
                            , value = f"{round(rpv_diff, 2)} €"
                            )
                    with col3:
                        st.metric(
                            "p-value"
                            , value = f"{round(pvalue, 3)}"
                            )
                    if pvalue > alpha/num_of_variants:
                        st.warning(f"""With a p-value of {round(pvalue, 3)} your result is not statistically significant.""")
                    else:
                        st.success(f"""With a p-value of {round(pvalue, 3)} your result is statistically significant.""")

if __name__ == '__main__':
    main()
    footer()