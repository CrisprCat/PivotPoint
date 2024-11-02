import streamlit as st
from modules.functions import Navbar
from modules.functions import calculate_mde
import pandas as pd

st.set_page_config(
    page_title="PivotPoint - MDE"
    , page_icon="⏳"
    , layout="centered"
    , initial_sidebar_state="auto"
    , menu_items=None)

def main():
    Navbar()
    # Page design
    st.title ('Minimal detectable effect (MDE) calculator')
    st.caption('Use this calculator to understand the MDE that you can statistically reliably detect, depending on your websites traffic, the statistical power and significance level you want to reach, and the time you can run your experiment.')

    # Input container
    with st.container():
        st.header('Binary Metric (Conversion rate)')
        st.caption('For a binary metric this calculator uses the z-test for proportions.')
        st.subheader('Input your data:')

        # Insert 3 columns to place input widgets in them
        colA1, colA2, colA3 = st.columns(3)

        with colA1:
            weekly_visits = st.number_input('Average weekly visits'
                                            , min_value = 1
                                            , max_value = None
                                            , value = None
                                            , step = 1
                                            , help = 'Enter the number of average weekly visits you expect during your experiment'
                                            , placeholder = ' Enter a number'
                                            )
            power = st.number_input('Statistical power'
                                    , value = 0.80
                                    , min_value = 0.05
                                    , max_value = 1.00
                                    , step = 0.05
                                    , help = '''1 - \u03B2: The probability to detect an effect that is truly there.  
                                    \u03B2 is the probability of making a type II error (false negative).'''
                                    )
            if power < 0.8:
                st.warning('⚠️ This statistical power is considered low!')
        with colA2:
            weekly_orders = st.number_input('Average weekly conversions'
                                            , min_value = 1
                                            , max_value = None
                                            , value = None
                                            , step = 1
                                            , help = 'Enter the number of average weekly conversions you expect during your experiment. These conversions can be orders or any microconversion you define.'
                                            , placeholder = 'Enter a number'
                                            )
            alpha = st.number_input('Statistical significance level'
                                    , value = 0.05
                                    , min_value = 0.05
                                    , max_value = 1.00
                                    , step = 0.05
                                    , help = '\u03B1: The probability of rejecting a null hypothesis, given that it is true'
                                    )
            if alpha > 0.1:
                st.warning('⚠️ This statistical significance level is considered high!')

        with colA3:
            num_of_variants = st.number_input('Number of experiment groups'
                                              , min_value = 2
                                              , max_value = None
                                              , value = 2
                                              , step = 1
                                              , help = '''Enter the number of experiment groups you want to test, one control group + a variable number of variants.  
                                              For more than 2 variants Bonferroni correction is used'''
                                              )
            hypo_type = st.radio('Hypothesis type'
                                 , options = ['One-sided'
                                              , 'Two-sided'
                                              ]
                                 , index = 0
                                 , help = 'Use one-sided when you want to detect an effect in a specific direction (increase or decrease). Use two-sided when you want to detect an effect in either direction. '
                                )



    # calculate output
    if weekly_visits != None and weekly_orders != None: # calculations should only run when variables are unequal to 0 to avoid errors.
        CR = weekly_orders / weekly_visits
        Num_of_weeks = [1, 2, 3, 4, 5, 6]
        sample_size_per_week = [int(i * weekly_visits / num_of_variants) for i in  Num_of_weeks]
        mde_per_week = []
        potential_CR = []
        difference_CR = []

        if hypo_type == 'One-sided':
            hypo = 'larger'
        else:
            hypo = 'two-sided'

        for i in Num_of_weeks:
            mde_i = calculate_mde(alpha = alpha /(num_of_variants - 1) # /(num_of_variants - 1) is the bonferroni correction for multiple comparisons
                                  , power = power
                                  , p1 = CR
                                  , n = i * weekly_visits / num_of_variants
                                  , alternative = hypo
                                  )
            mde = mde_i/CR*100
            CR_new = CR * (1 + (mde / 100)) * 100
            CR_diff = ((CR_new / 100) - CR) * 100
            mde_per_week.append(mde)
            potential_CR.append(CR_new)
            difference_CR.append(CR_diff)

        result = pd.DataFrame({'Runtime' : Num_of_weeks
                               , 'MDE_perc' : mde_per_week
                               , 'MDE_PP' : difference_CR
                               , 'Sample_size' : sample_size_per_week
                               , 'new_CR' : potential_CR
                               }) 

    # Output display container
        with st.container():
            st.subheader('Your result:')
            colB1, colB2 = st.columns([1, 2])

            with colB1:
                st.metric('Conversion Rate'
                          , value = f"{round(CR * 100, 2)} %"
                          )

            with colB2:
                st.dataframe(data=result
                             , hide_index = 1
                             , column_config = {
                                'Runtime' : 'Runtime (weeks)',
                                'MDE_perc': st.column_config.NumberColumn(
                                    'MDE in %',
                                    help = 'Minimal detectable effect in percent',
                                    format = "%.2f %%"),
                                'MDE_PP': st.column_config.NumberColumn(
                                    'MDE in PP',
                                    help = 'Minimal detectable effect in Percent points',
                                    format = "%.2f PP"),
                                'Sample_size' : 'Sample size per variant',
                                'new_CR' : st.column_config.NumberColumn(
                                    'Potential CR',
                                    format = "%.2f %%")
                                })
                st.caption(f"Reading example: After 1 week of runtime you would be able to statistically reliably detect an effect of {result.loc[0, 'MDE_perc']} %. This could mean an increase of your Conversion Rate from {round(CR * 100, 2)} % to {round((CR * 100) * (1 + result.loc[0, 'MDE_perc']/100), 2)} %")

        if result.loc[5, 'MDE_perc'] >= 5.00:
            st.warning('💡 Your MDE is quite high. Consider if the contrast of you A/B test is high enough.')

if __name__ == '__main__':
    main()