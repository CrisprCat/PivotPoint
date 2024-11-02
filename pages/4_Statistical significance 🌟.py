import streamlit as st
from modules.functions import Navbar
from scipy.stats import chisquare
import statsmodels.stats.proportion as pp

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
                                         , min_value = 0
                                         , max_value = None
                                         , step = 1
                                         , value = None
                                         , placeholder = 'Enter a number'
                                         , help = '''Enter the number of visits that you had in the control''')
    with col2:
        Orders_control = st.number_input('Number of orders'
                                         , min_value = 0
                                         , max_value = None
                                         , step = 1
                                         , help = '''Enter the number of orders that you had in the control''')
    with col3:
        if Visits_control != 0 and Orders_control != 0:
            CR_control = Orders_control / Visits_control
            st.metric("Control Conversion Rate"
                      , value = f"{round(CR_control * 100, 2)} %")
            
with st.container():
    st.subheader("Variant")
    col1, col2, col3 = st.columns(3)
    with col1:
        Visits_variant = st.number_input('Number of visits'
                                         , min_value = 0
                                         , max_value = None
                                         , step = 1
                                         , help = '''Enter the number of visits that you had in the variant''')
    with col2:
        Orders_variant = st.number_input('Number of orders'
                                         , min_value = 0
                                         , max_value = None
                                         , step = 1
                                         , help = '''Enter the number of orders that you had in the variant''')
    with col3:
        if Visits_variant != 0 and Orders_variant != 0:
            CR_variant = Orders_variant / Visits_variant
            st.metric("Variant Conversion Rate"
                      , value = f"{round(CR_variant * 100, 2)} %")
            
## SRM check of input data
    if Visits_control != 0 and Visits_variant != 0:
        sample_sizes = [Visits_control, Visits_variant]
        SRM_result = chisquare(sample_sizes
                               , f_exp = None)
        if SRM_result.pvalue < 0.1:
            st.warning(f"""With a p-value smaller than 0.1 ({round(SRM_result.pvalue, 3)}) a possible SRM is detected. Please check your data collection process before analysing the test results.""")


with st.container():
    col1, col2 = st.columns([1,2])
    if Visits_control != 0 and Orders_control != 0 and Visits_variant != 0 and Orders_variant != 0:
        stat, pval = pp.proportions_ztest(count = [Orders_control, Orders_variant]
                                                  , nobs = sample_sizes
                                                  , alternative = 'two-sided')
        diff = CR_variant - CR_control
        lift = diff / CR_control * 100


if __name__ == '__main__':
    main()