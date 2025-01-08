import streamlit as st
from modules.functions import Navbar
from modules.functions import footer
from modules.functions import calculate_mde_CR
import pandas as pd

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
    # Page design
    st.title ('Minimal detectable effect (MDE) calculator')
    st.caption(f'''Use this calculator to understand the MDE that you can statistically reliably detect, depending on your websites traffic, the statistical power and significance level you want to reach, and the time you can run your experiment.  
               You should choose your runtime to statistically reliably detect an effect size that is meaningful for your business, ensuring that the experiment can capture a difference that would have real value or impact on your key metrics!''')

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
                , help = '''Enter the number of variants you want to test. You should always have one control group + a variable number of variants.  
                For more than 2 variants Bonferroni correction is applied'''
                )
        with col4:
            hypo_type = st.radio(
                'Hypothesis type'
                , options = ['Two-sided', 'One-sided']
                , index = 0
                , help = 'Use one-sided when you want to detect an effect in a specific direction (increase or decrease). Use two-sided when you want to detect an effect in either direction. '
                )
            if hypo_type == 'One-sided':
                hypo = 'larger'
            else:
                hypo = 'two-sided'
    
    # Input container CR
    with st.container():
        st.header('Binomial Metric (Conversion rate, CR)')
        st.caption('For a binomial metric this calculator uses the z-test for proportions.')
        st.subheader('Input your data:')

        # Insert 3 columns to place input widgets in them
        col_CR_A1, col_CR_A2 = st.columns(2)

        with col_CR_A1:
            cr_weekly_visitors = st.number_input(
                'Average weekly visitors'
                , min_value = 1
                , max_value = None
                , value = None
                , step = 1
                , help = 'Enter the number of average weekly visitors you expect during your experiment'
                , placeholder = ' Enter a number'
                )
        with col_CR_A2:
            cr_weekly_orders = st.number_input(
                'Average weekly conversions'
                , min_value = 1
                , max_value = None
                , value = None
                , step = 1
                , help = 'Enter the number of average weekly conversions you expect during your experiment. These conversions can be orders or any microconversion you define.'
                , placeholder = 'Enter a number'
                )
    
        # calculate output CR
        if cr_weekly_visitors != None and cr_weekly_orders != None: # calculations should only run when variables are unequal to 0 to avoid errors.
            if cr_weekly_orders > cr_weekly_visitors:
                st.error(
                    "You shouldn't have more conversions than visitors."
                    , icon = '🚨')
            elif cr_weekly_orders == cr_weekly_visitors:
                st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
            else:          
                CR = cr_weekly_orders / cr_weekly_visitors
                Num_of_weeks = [1, 2, 3, 4, 5, 6]
                CR_sample_size_per_week = [int(i * cr_weekly_visitors / num_of_variants) for i in  Num_of_weeks]
                mde_per_week = []
                potential_CR = []
                difference_CR = []

                for i in Num_of_weeks:
                    mde_i = calculate_mde_CR(
                        alpha = alpha /(num_of_variants) # /(num_of_variants) is the bonferroni correction for multiple comparisons
                        , power = power
                        , p1 = CR
                        , n = i * cr_weekly_visitors / num_of_variants
                        , alternative = hypo
                        )
                    mde = mde_i/CR*100
                    CR_new = CR * (1 + (mde / 100)) * 100
                    CR_diff = ((CR_new / 100) - CR) * 100
                    mde_per_week.append(mde)
                    potential_CR.append(CR_new)
                    difference_CR.append(CR_diff)

                result = pd.DataFrame(
                    {'Runtime' : Num_of_weeks
                    , 'MDE_perc' : mde_per_week
                    , 'MDE_PP' : difference_CR
                    , 'Sample_size' : CR_sample_size_per_week
                    , 'new_CR' : potential_CR
                    }) 

            # Output display container CR
                with st.container():
                    st.subheader('Your result:')
                    
                    col_CR_B1, col_CR_B2 = st.columns([1, 2])
    
                    with col_CR_B1:
                        st.metric(
                            'Conversion Rate'
                            , value = f"{round(CR * 100, 2)} %"
                            )
                        
                    with col_CR_B2:
                        st.dataframe(
                            data=result
                            , hide_index = 1
                            , column_order = (
                                "Runtime"
                                , "MDE_perc"
                                , "MDE_PP"
                                , "new_CR"
                                , "Sample_size"
                                )
                            , column_config = {
                                'Runtime' : '''Time (weeks)''',
                                'MDE_perc': st.column_config.NumberColumn(
                                    'MDE (%)',
                                    help = 'Minimal detectable effect in percent',
                                    format = "%.2f %%"),
                                'MDE_PP': st.column_config.NumberColumn(
                                    'MDE (PP)',
                                    help = 'Minimal detectable effect in Percent points',
                                    format = "%.3f PP"),
                                'new_CR' : st.column_config.NumberColumn(
                                    'Potential CR',
                                    format = "%.2f %%"),
                                'Sample_size' : 'Sample size per variant'
                                })
                        if hypo_type == 'One-sided':
                            st.caption(f"Reading example: After 1 week of runtime you would be able to statistically reliably detect an effect of {round(result.loc[0, 'MDE_perc'], 2)} %. This could mean an increase of your Conversion rate from {round(CR * 100, 2)} % to {round((CR * 100) * (1 + result.loc[0, 'MDE_perc']/100), 2)} %")
                        else:
                            st.caption(f"Reading example: After 1 week of runtime you would be able to statistically reliably detect an effect of {round(result.loc[0, 'MDE_perc'], 2)} %. This could mean a Conversion rate between {round((CR * 100) * (1 - result.loc[0, 'MDE_perc']/100), 2)} % and {round((CR * 100) * (1 + result.loc[0, 'MDE_perc']/100), 2)} %")
    
                if result.loc[5, 'MDE_perc'] >= 5.00:
                    st.warning('💡 Your MDE is quite high. Consider if the contrast of you A/B test is high enough.')

    # Input container RPV
    with st.container():
        st.header('Continuous metric (Revenue per Visitor, RPV)')
        st.caption('For a continuous metric this calculator uses the t-test.')
        st.subheader('Input your data:')

        # Insert 3 columns to place input widgets in them
        col_RPV_A1, col_RPV_A2 = st.columns([1, 2])
        
        with col_RPV_A1:
            RPV_num_visitors = st.number_input(
                'Number of visitors'
                , min_value = 1
                , max_value = None
                , value = None
                , step = 1
                , help = 'Enter the number of visitors you had during the last 4 weeks that would enter your experiment.'
                , placeholder = ' Enter a number'
                )
        with col_RPV_A2:
            RPV_order_value = st.file_uploader(
                'Order value'
                , type = ['csv']
                , accept_multiple_files = False
                , help = '''Upload a .csv file with the revenue values for each order in the last 4 weeks that would be included in your experiment.   
                Your .csv file should contain a header cell.'''
                )

        if RPV_order_value is not None:
            rpv_df = pd.read_csv(
                RPV_order_value
                # , sep = ';'
                , header = 0
                # , decimal = ','
                )
            # debugging
            # print(rpv_df)
            
            # Sanity checks
            ## The column should only contain numeric values
            from modules.functions import check_numeric_columns
            san_num = check_numeric_columns (rpv_df, [0])
            if san_num == False:
                st.warning(
                    'It looks like your revenue data contains non-numeric values.'
                    , icon = '⚠️')
            else:
                ## All values shoudl be > 0  
                from modules.functions import check_value_size
                san_zero = check_value_size(rpv_df, 0) 
                if san_zero == False:
                    st.warning(
                        'It looks like you have orders with 0 € revenue or less.'
                        , icon = '⚠️')
                else:
                    # Calculate mde RPV output
                    if RPV_order_value is not None and RPV_num_visitors is not None:
                        RPV_num_orders = len(rpv_df)
                        RPV_CR = RPV_num_orders / RPV_num_visitors

                        #debugging
                        # print(RPV_num_orders)

                        if RPV_num_orders > RPV_num_visitors:
                            st.error(
                                "You shouldn't have more conversions than visitors."
                                , icon = '🚨'
                                )
                        elif RPV_num_orders == RPV_num_visitors:
                            st.warning('⚠️ You have a Conversion rate of 100 %, there seems to be nothing left to optimize 😲')
                        else:
                            num_null_orders = RPV_num_visitors - RPV_num_orders
                            RPV_full_data = pd.concat([rpv_df.squeeze(), pd.Series([0] * num_null_orders)]).reset_index(drop=True)
                            RPV_mean = RPV_full_data.mean(skipna = False)
                            RPV_std = RPV_full_data.std(skipna = False)

                            # debugging
                            # print(num_null_orders)
                            # print(RPV_full_data)

                            Num_of_weeks = [1, 2, 3, 4, 5, 6]
                            RPV_sample_size_per_week = [int(i * (RPV_num_visitors/4) / num_of_variants) for i in  Num_of_weeks]
                            RPV_mde_per_week = []
                            potential_RPV = []
                            difference_RPV = [] 
                            from modules.functions import calculate_mde_RPV
                            for i in Num_of_weeks:
                                mde_i = calculate_mde_RPV(
                                    alpha = alpha /(num_of_variants) # /(num_of_variants) is the bonferroni correction for multiple comparisons
                                    , power = power
                                    , n = i * (RPV_num_visitors/4)
                                    , ttype = hypo
                                    , std = RPV_std
                                    )
                                mde = (mde_i/RPV_mean * 100)
                                RPV_mde_per_week.append(mde)
                                RPV_new = RPV_mean * (1 + (mde))
                                RPV_diff = ((RPV_new / 100) - RPV_mean) * 100
                                potential_RPV.append(RPV_new)
                                difference_RPV.append(RPV_diff)

                            RPV_result = pd.DataFrame(
                                {'Runtime' : Num_of_weeks
                                , 'RPV_MDE_perc' : RPV_mde_per_week
                                , 'RPV_MDE_PP' : difference_RPV
                                , 'RPV_Sample_size' : RPV_sample_size_per_week
                                , 'new_RPV' : potential_RPV
                                }
                                )
                            # Output display container CR
                            with st.container():
                                st.subheader('Your result:')
                                col_RPV_B1, col_RPV_B2, col_RPV_B3 = st.columns(3)
                                with col_RPV_B1:
                                    st.metric(
                                        'Conversion Rate'
                                        , value = f"{round(RPV_CR * 100, 2)} %"
                                        )
                                with col_RPV_B2:
                                    st.metric(
                                        "Revenue per Visitor"
                                        , value = f"{round(RPV_mean, 2)} €"
                                        )
                                with col_RPV_B3:
                                    st.metric(
                                        "Standard deviation"
                                        , value = f"{round(RPV_std, 2)} €"
                                        )
                                    
                                st.dataframe(
                                    data = RPV_result
                                    , hide_index = 1
                                    , column_order = (
                                        "Runtime"
                                        , "RPV_MDE_perc"
                                        , "RPV_MDE_PP"
                                        , "new_RPV"
                                        , "RPV_Sample_size"
                                        )
                                    , column_config = {
                                                'Runtime' : '''Time (weeks)''',
                                                'RPV_MDE_perc': st.column_config.NumberColumn(
                                                    'MDE (%)',
                                                    help = 'Minimal detectable effect in percent',
                                                    format = "%.2f %%"),
                                                'RPV_MDE_PP': st.column_config.NumberColumn(
                                                    'MDE (€)',
                                                    help = 'Minimal detectable effect in Euro',
                                                    format = "%.3f €"),
                                                'new_RPV' : st.column_config.NumberColumn(
                                                    'Potential RPV',
                                                    format = "%.2f %% €"),
                                                'RPV_Sample_size' : 'Sample size per variant'
                                                })
                                if hypo_type == 'One-sided':
                                    st.caption(f"Reading example: After 1 week of runtime you would be able to statistically reliably detect an effect of {round(RPV_result.loc[0, 'RPV_MDE_perc'], 2)} %. This could mean an increase of your Revenue per Visitor from {round(RPV_mean, 2)} € to {round(RPV_mean * (1 + RPV_result.loc[0, 'RPV_MDE_perc']/100), 2)} €")
                                else:
                                    st.caption(f"Reading example: After 1 week of runtime you would be able to statistically reliably detect an effect of {round(RPV_result.loc[0, 'RPV_MDE_perc'], 2)} %. This could mean a Conversion rate between {round((RPV_mean) * (1 - RPV_result.loc[0, 'RPV_MDE_perc']/100), 2)} % and {round((RPV_mean) * (1 + RPV_result.loc[0, 'RPV_MDE_perc']/100), 2)} €")
                            if RPV_result.loc[5, 'RPV_MDE_perc'] >= 5.00:
                                st.warning('💡 Your MDE is quite high. Consider if the contrast of you A/B test is high enough.')


if __name__ == '__main__':
    main()
    footer()