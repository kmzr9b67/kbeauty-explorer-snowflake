import yaml

import streamlit as st
import pandas as pd

from k_beauty_app.database import DataBase
from k_beauty_app.models import AgeRanges, SkinType, Concerns

st.set_page_config(page_title="K-Beauty Explorer", page_icon="✨", layout="centered")

db = DataBase.get_instance()
age_keys = db.get_keys(AgeRanges)
skin_type_keys = db.get_keys(SkinType)
concern_keys = db.get_keys(Concerns)


if 'form_page' not in st.session_state:
    st.session_state.form_page = True

if st.session_state.form_page:
    with st.container(horizontal_alignment="center", vertical_alignment="center"):
        st.space(size = "medium")
        st.header("K-Beauty Advisor", text_alignment = "center", width = "stretch")
        st.space(size = "small")
        col1, col2, col3, col4 = st.columns(width = "stretch", vertical_alignment = "bottom", spec = [0.3, 0.3, 0.3, 0.1])
        
        with col1:
            age = st.selectbox(label = "Your Age Group", options = list(age_keys), label_visibility="visible")
        with col2:
            skin_type = st.selectbox(label = "Skin Type",options = list(skin_type_keys), label_visibility="visible")
        with col3:
            concern = st.selectbox(label = "Primary Skin Concern", options = list(concern_keys), label_visibility="visible")
        with col4:
            if st.button(width="content", label = "->", type = "primary"):
                st.session_state.results = db.get_recommendations(age_val = age, skin_val = skin_type, concern_val = concern)
                st.session_state.form_page = False
                st.rerun()
        
        st.space(size = "medium")
        with st.container(horizontal_alignment= "center"):
            st.text("The results will be with you in 5-10 secends.")
        st.space(size = "medium")


else:
    results = st.session_state.results
    if results == None:
        st.header("✨ No Match Found", text_alignment="center")
        st.space("small")
        st.markdown("**We couldn't find a perfect routine for this specific combination.**", text_alignment= "center")
        st.space("small")
        _, col1, _ = st.columns([0.4, 0.2, 0.4], gap="small", width="stretch", vertical_alignment="top")
        st.divider()
        col1.link_button("Contact us", url = "https://github.com/kmzr9b67/kbeauty-explorer-snowflake/issues/new", type = "primary", use_container_width=True)
    else:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            routine_info = yaml.safe_load(file)['steps']
        st.header("YOUR PERSONALIZED ROUTINE")
        st.divider()

        table_data = {
            "Step": [],
            "Routine": [],
            "Product": [],
            "Brand": [],
            "Rating": [],
        }

        for i, res in enumerate(results):
            table_data["Step"].append(f"STEP {i+1}")
            table_data["Routine"].append(f"{routine_info[i]['icon']} {routine_info[i]['name']}")
            table_data["Product"].append(res["product_name"])
            table_data["Brand"].append(res["brand"])
            

            rating = float(res["rating"])
            stars = "⭐" * int(round(rating))
            table_data["Rating"].append(f"{stars}")

        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    _, col1, _ = st.columns([0.45, 0.1, 0.45], gap="small", width="stretch", vertical_alignment="top")
    if col1.button( label = "<-", type = "primary", use_container_width=True):
        st.session_state.form_page = True
        st.rerun()