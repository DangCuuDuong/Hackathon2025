# streamlit run c:/Users/Admin/Documents/Study/Projects/HK6/Hackathon2025/BE/main.py
import streamlit as st
import pandas as pd
import os
from pathlib import Path
import CollectionComponets as clp
import ImageCollection as ic


# Cấu hình đường dẫn
CSV_PATH = "ingredients.csv"
UPLOAD_DIR = "uploads"



Path(UPLOAD_DIR).mkdir(exist_ok=True)

# Khởi tạo CSV nếu chưa tồn tại
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=["name", "category", "count"])
    df.to_csv(CSV_PATH, index=False)




st.set_page_config(page_title="Smart Refrigerator", page_icon="🍽️")
st.header("Smart Refrigerator")

siddbar_option = ["Home", "Collection Component", "Collection By Image"]
st.sidebar.title("Navigation")
selected_sidebar = st.sidebar.selectbox("Select Option", siddbar_option)

if selected_sidebar == "Home":
    st.subheader("Welcome to the Smart Refrigerator App!")
    st.write("This app helps you manage your ingredients efficiently.")
elif selected_sidebar == "Collection Component":
    clp.create_recommendation()
elif selected_sidebar == "Collection By Image":
    ic.ImageCollection()


df_components = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
st.subheader("Current Ingredients")
if not df_components.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Name")
        st.write(df_components["name"].values)
    with col2:
        st.write("Count")
        st.write(df_components["count"].values)
else:
    st.write("No ingredients available.")


# Footer
st.markdown("---")
st.markdown("© 2025 My App. All rights reserved.")