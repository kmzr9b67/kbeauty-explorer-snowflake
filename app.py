import streamlit as st

# 1. Konfiguracja strony na tryb szeroki (niezbędne dla 5 kolumn)
st.set_page_config(page_title="K-Beauty Advisor", page_icon="✨", layout="wide")

st.title("✨ K-Beauty Personalized Advisor")
st.markdown("---")

# Sekcja filtrów
col_age, col_skin, col_concern = st.columns(3)

with col_age:
    age = st.selectbox("Your Age Group", ["Under 20", "20-30", "30-50", "50+"])
with col_skin:
    skin_type = st.selectbox("Skin Type", ["Oily", "Dry", "Combination", "Sensitive"])
with col_concern:
    concern = st.selectbox("What to improve?", ["Hydration", "Acne", "Anti-aging", "Glow"])

st.markdown(" ")

# Przycisk generowania wynikow
if st.button('Generate My Routine', use_container_width=True):
    st.divider()
    st.subheader(f"✨ Your Custom 5-Step Routine for {skin_type} & Skin {concern}")
    st.markdown(" ")

    # 2. Definicja kroków rutyny (UX: Jasne etykiety i ikony)
    routine_steps = [
        {"step": "STEP 1", "label": "OIL CLEANSER", "icon": "🧼"},
        {"step": "STEP 2", "label": "WATER CLEANSE", "icon": "🌊"},
        {"step": "STEP 3", "label": "TONER", "icon": "💧"},
        {"step": "STEP 4", "label": "SERUM", "icon": "🧪"},
        {"step": "STEP 5", "label": "PROTECT (SPF)", "icon": "☀️"}
    ]

    # 3. Tworzenie 5 kolumn z równym odstępem (gap)
    cols = st.columns(5, gap="medium")
    
    #  SQL Query - should be here. 
    for i, col in enumerate(cols):
        with col:
            # Użycie kontenera z obramowaniem tworzy estetyczną kartę produktu
            with st.container(border=True):
                # Nagłówek kroku
                st.caption(f"{routine_steps[i]['step']}: {routine_steps[i]['label']}")
                
                # Optional TODO 
                # # Placeholder na zdjęcie produktu
                # st.image(f"", use_container_width=True)
                
                # Nazwa produktu (Tu trafią dane ze Snowflake)
                st.markdown(f"**{routine_steps[i]['icon']} Best-Seller {routine_steps[i]['label'].capitalize()}**")
                
                # Rating - TODO it should be dynamic. 
                st.caption("Rating: ⭐⭐⭐⭐⭐ (4.9)")
                
                # Optional TODO 
                # # Przycisk akcji dla konkretnego produktu
                # st.button("View Details", key=f"btn_{i}", use_container_width=True)
