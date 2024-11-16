import streamlit as st
from modules.functions import Navbar
from modules.functions import footer

st.set_page_config(
    page_title="PivotPoint"
    , page_icon="🏠"
    , layout="centered"
    , initial_sidebar_state="auto"
    , menu_items=None)


def main():
    Navbar()

    st.title("Pivot Point 🎈")
    st.subheader("The One Where We Test")
    st.write(
        "This app is intended to provide a comprehensive resource about statistical hypothesis testing all around AB testing.  "
    )
 
    st.page_link("pages/1_MDE ⏳.py", label="Minimum detectable effect", icon="⏳")
    st.page_link("pages/2_SRM ⚖️.py", label="Sample ratio mismatch", icon="⚖️")
    st.page_link("pages/3_Interaction detector 🕵️‍♀️.py", label="Interaction detection", icon="🕵️‍♀️")
    st.page_link("pages/4_Statistical significance 🌟.py", label="Statistical significance", icon="🌟")
    st.page_link("pages/5_FAQ ❓.py", label="Frequently asked questions", icon="❓")

if __name__ == '__main__':
    main()
    footer()
