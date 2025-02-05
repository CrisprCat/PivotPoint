import streamlit as st

# Create a sidebar
def Navbar():
    with st.sidebar:
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/1_MDE ⏳.py", label='''Minimum detectable effect (MDE) calculator''', icon="⏳")
        st.page_link("pages/2_SRM ⚖️.py", label="Sample ratio mismatch (SRM) detector", icon="⚖️")
        st.page_link("pages/3_Interaction detector 🕵️‍♀️.py", label="Interaction detector", icon="🕵️‍♀️")
        st.page_link("pages/4_Statistical significance 🌟.py", label="Statistical hypothesis tester", icon="🌟")

# Create a footer
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="#1A1B1F",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)
br

def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://www.linkedin.com/in/dr-katharina-bursch-143a70120", "Kathi"),
        ". Find source code at ",
        link("https://github.com/CrisprCat/PivotPoint", "Github"),
        "."
    ]
    layout(*myargs)

# Define mde function
from statsmodels.stats import power as pwr
import math

def calculate_mde_CR(alpha, power, p1, n, alternative):
    # Calculate the effect size using statsmodels
    effect_size = pwr.zt_ind_solve_power(effect_size=None # returns the effect size as a standardized value
                                        , nobs1=n 
                                        , alpha=alpha 
                                        , power=power 
                                        , alternative=alternative
                                        , ratio = 1.0
                                        )
    # Translate effect size to MDE
    mde = effect_size * math.sqrt(p1 * (1 - p1))
    return mde

## Sanity checks for csv file uploads
### check if revenue file data only contains numeric values
import pandas as pd
def check_numeric_columns (df, col_indices):
    is_numeric = []
    for col_idx in col_indices:
        col = df.iloc[:, col_idx]
        is_numeric.append(pd.to_numeric(col, errors = 'coerce').notnull().all())

    return all(is_numeric)

### check if revenue file contains orders with revenue <=0
def check_value_size(df, col_indices):
    is_greater_zero = df.iloc[:, col_indices].gt(0).all().all()

    return is_greater_zero

def calculate_mde_RPV(alpha, power, n, ttype, std):
    analysis = pwr.TTestIndPower()
    RPV_effect_size = analysis.solve_power(effect_size = None
                                           , nobs1 = n
                                           , alpha = alpha
                                           , power = power
                                           , ratio = 1.0
                                           , alternative = ttype)
    RPV_mde = (RPV_effect_size * std)
    return RPV_mde

