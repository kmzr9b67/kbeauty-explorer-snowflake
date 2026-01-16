import yaml

import streamlit as st
import pandas as pd

from k_beauty_app.database import DataBase
from k_beauty_app.models import AgeRanges, SkinType, Concerns

# Sets up the basic Streamlit page appearance and metadata
st.set_page_config(page_title="K-Beauty Explorer", page_icon="✨", layout="centered")

# Connects to Snowflake using the singleton instance of DataBase class
db = DataBase.get_instance()

# Fetches filter options from the database to populate dropdown menus
age_keys = db.get_keys(AgeRanges)
skin_type_keys = db.get_keys(SkinType)
concern_keys = db.get_keys(Concerns)

def init_state():
    """Initializes the Streamlit session state variables.
    
    Ensures that the application remembers the user's progress (form vs results)
    and stores the recommendation results during a session.
    """
    if "form_page" not in st.session_state:
        st.session_state.form_page = True # Controls which UI section to display
    if "results" not in st.session_state:
        st.session_state.results = None # Stores query results from Snowflake


def submit_form(age, skin_type, concern):
    """Handles the form submission and triggers the recommendation engine.

    Args:
        age (str): User selected age range.
        skin_type (str): User selected skin type.
        concern (str): User selected primary skin concern.
    """
    # Calls the database to find products matching the specific criteria
    st.session_state.results = db.get_recommendations(
        age_val=age,
        skin_val=skin_type,
        concern_val=concern
    )
    # Switches the view to the result page
    st.session_state.form_page = False


def go_back():
    """Resets the view state to show the initial input form."""
    st.session_state.form_page = True

# Execute state initialization
init_state()

# FORM PAGE
if st.session_state.form_page:
    st.space(size = "medium")
    st.header("K-Beauty Advisor", text_alignment="center")
    st.space(size = "small")
    # Layout with 4 columns for a sleek horizontal selection bar
    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.1] ,vertical_alignment = "bottom")

    with col1:
        age = st.selectbox("Your Age Group",age_keys)

    with col2:
        skin_type = st.selectbox("Skin Type",skin_type_keys)

    with col3:
        concern = st.selectbox("Primary Skin Concern",concern_keys)

    with col4:
        # Primary button triggers the submit_form callback with user inputs
        st.button("→",type="primary",on_click=submit_form,args=(age, skin_type, concern),
            use_container_width=True
        )

    st.space(size = "medium")
    with st.container(horizontal_alignment= "center"):
        st.text("The results will be with you in 5-10 secends.")
    st.space(size = "medium")

# RESULT PAGE
else:
    results = st.session_state.results
    # Error handling: Displays a friendly message if no matching products were found
    if not results or results == [{}]:
        st.header("✨ No Match Found", text_alignment="left")
        st.space("small")
        st.markdown(
            "**We couldn't find a perfect routine for this specific combination.**"
        )
        st.divider()
        st.link_button(
            "Contact us",
            url="https://github.com/kmzr9b67/kbeauty-explorer-snowflake/issues/new",
            type="primary"
        )

    else:
        # Load external configuration for UI icons and step names
        with open("config.yaml", encoding="utf-8") as file:
            routine_info = yaml.safe_load(file)["steps"]
        st.header("YOUR PERSONALIZED ROUTINE")
        st.divider()
        
        # Data preparation for tabular display
        table_rows = []
        for i, res in enumerate(results):
            # Visual representation of ratings using star emojis
            stars = "⭐" * round(float(res["rating"]))
            table_rows.append({
                "Step": f"STEP {i+1}",
                "Routine": f"{routine_info[i]['icon']} {routine_info[i]['name']}",
                "Product": res["product_name"],
                "Brand": res["brand"],
                "Rating": stars
            })
        
        # Display results in an interactive table
        df = pd.DataFrame(table_rows)

        st.dataframe(df,use_container_width=True,hide_index=True)
    
    # Navigation button to return to the search form
    st.button("← Back",type="primary",on_click=go_back)