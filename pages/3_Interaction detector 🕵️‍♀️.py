import streamlit as st
from modules.functions import Navbar
from modules.functions import footer
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

st.set_page_config(
    page_title="CRO Calculators"
    , page_icon="pictures\Favicon.png"
    , layout="centered"
    , initial_sidebar_state="auto"
    , menu_items=None
    )

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def main():
    Navbar()

    st.title ("Interaction detector")
    st.caption('When you run parallel experiments and suspect an interaction between your experiments you can use this detector to test if there is evidence for such an interaction.')

    with st.container():
        st.header("Traffic interactions")
        st.caption('Traffic interactions are defined as an imbalance in the visitor distribution between your experiments. In a perfectly randomized experiment you expect, that visitors from the control group of your first experiment split equally between control and variant of your second experiment.')
        st.subheader("Please input your data:")

        # Not yet sure that it would really be needed to test more than two parallel experiments
        # colA1, colA2 = st.columns([1, 2])
        # with colA1:
        #     num_of_experiments = st.number_input('How many experiments did you run in parallel?'
        #                                          , 2
        #                                          , 2
        #                                          , help = 'Currently this calculator only supports analysis of two parallel experiments.'
        #                                          )

    df = pd.DataFrame(np.nan
                      , index=['Visitors in Control of Experiment 2'
                               , 'Visitors in Variant of Experiment 2']
                      , columns=['A'
                                 , 'B']
                      )

    input_data = st.data_editor(data = df
                                , num_rows = 'fixed'
                                , column_config = {
                                    'A' : st.column_config.NumberColumn(
                                        label = "Visitors in Control of Experiment 1"
                                        , required = True
                                        , default = "int"
                                        , min_value = 1
                                    ),
                                    'B' : st.column_config.NumberColumn(
                                        label = "Visitors in Variant of Experiment 1"
                                        , required = True
                                        , default = "int"
                                        , min_value = 1
                                    ),
                                    }
                                    )

    print(input_data)
    print(chi2_contingency(input_data))

    if input_data is not None and input_data.values.sum() > 0:
        stat, pvalue, dof, exp_freq = chi2_contingency(input_data)
        if pvalue < 0.1:
            st.warning(f"""The p-value is smaller than 0.1 ({round(pvalue, 3)}). A possible traffic interaction in between your experiments was detected.""")
        else:
            st.balloons()
            st.success(f"""The p-value is greater than 0.1 ({round(pvalue, 3)}). No traffic interaction in between your experiments was detected. Happy analysing your test results.""")

if __name__ == '__main__':
    main()
    footer()










# st.title ("Metric interactions")

# import pandas as pd

# from statsmodels.formula.api import ols

# model = ols("REVENUE ~ X_VARIATION_NAME * Y_VARIATION_NAME", data=pdf_xy_rpv)

# results = model.fit()

# results.summary()
