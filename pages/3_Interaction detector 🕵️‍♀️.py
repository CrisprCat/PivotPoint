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
    , menu_items=None)


def main():
    Navbar()

    st.title ("Interaction detector")

    with st.container():
        st.header("Traffic interactions")
        st.subheader("Please input your data:")

        colA1, colA2 = st.columns([1, 2])
        with colA1:
            num_of_experiments = st.number_input('How many experiments did you run in parallel?'
                                                 , 2
                                                 , 2
                                                 , help = 'Currently this calculator only supports analysis of two parallel experiments.'
                                                 )

    df = pd.DataFrame(np.nan
                      , index=['Visits in A of Experiment 2'
                               , 'Visits in B of Experiment 2']
                      , columns=['A'
                                 , 'B']
                      )

    input_data = st.data_editor(data = df
                                , num_rows = 'fixed'
                                , column_config = {
                                    'A' : st.column_config.NumberColumn(
                                        label = "Visits in A of Experiment 1"
                                        , required = True
                                        , default = "int"
                                    ),
                                    'B' : st.column_config.NumberColumn(
                                        label = "Visits in B of Experiment 1"
                                        , required = True
                                        , default = "int"
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
