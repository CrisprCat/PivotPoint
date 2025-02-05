import streamlit as st
from modules.functions import Navbar
from modules.functions import footer

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

    st.title("🧮 CRO Calculators")
    st.write("This app is intended to provide a tool collection about statistical hypothesis testing all around AB testing.")
 
    st.page_link("pages/1_MDE ⏳.py", label='''Minimum detectable effect (MDE) calculator''', icon="⏳")
    st.page_link("pages/2_SRM ⚖️.py", label="Sample ratio mismatch (SRM) detector", icon="⚖️")
    st.page_link("pages/3_Interaction detector 🕵️‍♀️.py", label="Interaction detector", icon="🕵️‍♀️")
    st.page_link("pages/4_Statistical significance 🌟.py", label="Statistical hypothesis tester", icon="🌟")
    st.page_link("https://www.conversion-stash.com/cro-glossary", label = "Conversion Stash CRO Glossary", icon = ":material/open_in_new:")

if __name__ == '__main__':
    main()
    footer()
