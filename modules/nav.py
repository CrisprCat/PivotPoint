import streamlit as st

def Navbar():
    with st.sidebar:
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/1_MDE ⏳.py", label="Minimum detectable effect", icon="⏳")
        st.page_link("pages/2_SRM ⚖️.py", label="Sample ratio mismatch", icon="⚖️")
        st.page_link("pages/3_Interaction detector 🕵️‍♀️.py", label="Interaction detection", icon="🕵️‍♀️")
        st.page_link("pages/4_Statistical significance 🌟.py", label="Statistical significance", icon="🌟")
        st.page_link("pages/5_FAQ ❓.py", label="Frequently asked questions", icon="❓")