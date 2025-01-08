import streamlit as st
from modules.functions import Navbar
from modules.functions import footer
import numpy as np
from scipy.stats import chisquare

# set tab title and Favicon
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

    st.title ("Sample ratio mismatch (SRM) detector")
    st.caption('Use this calculator to detect discrepancies between your expected and actual number of visitors per sample in your experiment.')

    # Initial Input container
    with st.container():
        st.subheader('Please input your data:')
        colA1, colA2 = st.columns(2)
        with colA1:
            num_of_samples = st.number_input(
                'How many variants are you testing?'
                , value = 2
                , step = 1
                )
        with colA2:
            distribution = st.radio(
                'What distribution did you set between control and variants?'
                , ['Equal', 'Unequal']
                , help = 'Choose Equal when you expect the same number of visitors in all your variants.'
                )

    # Variable input container
    # depending on the input of the initial input container
    with st.container():
        sample_sizes = []
        # create two colummns
        col1, col2 = st.columns(2)

        # Create entry fields dynamically
        for i in range(num_of_samples):
            if i % 2 == 0:
                with col1:
                    sample_size = st.number_input(
                        f"Visitors in Sample {i+1}:"
                        , key = f"input_{i+1}"
                        , min_value = 1
                        , max_value = None
                        , value = None
                        , step = 1
                        , placeholder = 'Enter a number'
                        )
                    sample_sizes.append(sample_size)
            else:
                with col2:
                    sample_size = st.number_input(
                        f"Visitors in Sample {i+1}:"
                        , key = f"input_{i+1}"
                        , min_value = 1
                        , max_value = None
                        , value = None
                        , step = 1
                        , placeholder = 'Enter a number'
                        )
                    sample_sizes.append(sample_size)

    with st.container():
        exp_freq = []
        # create two colummns
        col1, col2 = st.columns(2)
        if distribution == 'Unequal':
            for i in range(num_of_samples):
                if i % 2 == 0:
                    with col1:
                        exp_frequency = st.number_input(
                            f"What is your expected frequency in Sample {i+1}:"
                            , min_value= 0.00
                            , max_value =1.00
                            , value = None
                            , step = 0.05
                            , placeholder = 'Enter a number'
                            )
                        exp_freq.append(exp_frequency)
                else:
                    with col2:
                        exp_frequency = st.number_input(
                            f"What is your expected frequency in Sample {i+1}:"
                            , min_value= 0.00
                            , max_value =1.00
                            , value = None
                            , step = 0.05
                            , placeholder = 'Enter a number'
                            )
                        exp_freq.append(exp_frequency)

    if np.all(exp_freq) and distribution == 'Unequal':
        if sum(exp_freq) != 1.00:
            st.warning(f"""Your expected frequencies should sum up to 1.00""")
        else:
            total_sample = sum(sample_sizes)
            exp_freq = [freq * total_sample for freq in exp_freq]
            test_result = chisquare(sample_sizes, f_exp=exp_freq)
            if test_result.pvalue < 0.1:
                st.warning(f"""The p-value is smaller than 0.1 ({round(test_result.pvalue, 3)}). A possible SRM is detected. Please contact your AB test experts before analysing the test results.""")
            else:
                st.balloons()
                st.success(f"""The p-value is greater than 0.1 ({round(test_result.pvalue, 3)}). No SRM is detected. Happy analysing your test results.""")

    if np.all(sample_sizes) and distribution == 'Equal':
        test_result = chisquare(sample_sizes, f_exp=None)
        if test_result.pvalue < 0.1:
            st.warning(f"""The p-value is smaller than 0.1 ({round(test_result.pvalue, 3)}). A possible SRM is detected. Please double check your data generating process before applying statistical analysis.""")
        else:
            st.balloons()
            st.success(f"""The p-value is greater than 0.1 ({round(test_result.pvalue, 3)}). No SRM is detected. Happy analysing your test results.""")

if __name__ == '__main__':
    main()
    footer()





