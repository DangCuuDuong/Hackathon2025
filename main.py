# streamlit run c:/Users/Admin/Documents/Study/Projects/HK6/Hackathon2025/BE/main.py
import streamlit as st
import pandas as pd
import os
from pathlib import Path
import FE.CollectionComponets as clp
import FE.ImageCollection as ic
import json
from JSON_FILE.combine import combind_json
from BE.predict_food import predict_objects_and_weight

# Cấu hình đường dẫn
CSV_PATH = "ingredients.csv"



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
    img = ic.ImageCollection()
    
    if img != None:
        result = predict_objects_and_weight(img)
        with open("JSON_FILE/predict.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        combind_json("JSON_FILE/main.json", "JSON_FILE/predict.json")
    st.write(img)

df_components = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
st.subheader("Current Ingredients")
with open('JSON_FILE/main.json', 'r') as f:
    json_data = json.load(f)

# Chuyển thành DataFrame
df_components = pd.DataFrame(list(json_data.items()), columns=["name", "count"])
df_components = df_components.sort_values(by="count", ascending=False)

if not df_components.empty:
    # Hiển thị bảng
    st.subheader("🧾 Current Ingredients")
    st.dataframe(df_components)  # hoặc st.table(df_components)


# Footer
st.markdown("---")
st.markdown("© 2025 My App. All rights reserved.")