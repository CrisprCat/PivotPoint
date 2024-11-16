import streamlit as st

def Navbar():
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #F6F6F6;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/1_MDE ⏳.py", label="Minimum detectable effect", icon="⏳")
        st.page_link("pages/2_SRM ⚖️.py", label="Sample ratio mismatch", icon="⚖️")
        st.page_link("pages/3_Interaction detector 🕵️‍♀️.py", label="Interaction detection", icon="🕵️‍♀️")
        st.page_link("pages/4_Statistical significance 🌟.py", label="Statistical significance", icon="🌟")
        st.page_link("pages/5_FAQ ❓.py", label="Frequently asked questions", icon="❓")


from statsmodels.stats.power import zt_ind_solve_power
import math

def calculate_mde(alpha, power, p1, n, alternative):
    # Calculate the effect size using statsmodels
    effect_size = zt_ind_solve_power(effect_size=None # returns the effect size as a standardized value
                                     , nobs1=n 
                                     , alpha=alpha 
                                     , power=power 
                                     , alternative=alternative
                                     , ratio = 1.0
                                     )
    # Translate effect size to MDE
    mde = effect_size * math.sqrt(p1 * (1 - p1))
    return mde