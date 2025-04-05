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
from BE.input_clean import clean_ingredient_name
import FE.Home as home
import FE.RecommendationRecipe as rr

st.set_page_config(page_title="Smart Refrigerator", page_icon="🍽️", layout="wide")


st.markdown(
    """
    <style>
    .title_main {
        font-size: 85px !important; 
        font-weight: bold;
        color: #54b8cf; /* Màu sắc của tiêu đề */
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        font-family: 'Open Sans'; /* Phông chữ */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Đổ bóng cho tiêu đề */
    }

    .one1{
        font-size: 45px !important;
        font-weight: bold;
        color: #eab676; /* Màu sắc của tiêu đề */
        text-align: center;
        font-family: 'Open Sans'; /* Phông chữ */
    }

    .one2{
        font-size: 30px !important;
        font-weight: bold;
        color: #f0dba2; /* Màu sắc của tiêu đề */
        margin-bottom: 8px;
        color: #4CAF50;
        text-align: left;
        font-family: 'Open Sans'; /* Phông chữ */
        
    }
    
    .recipe_suggestion {
        font-size: 30px !important;
        font-weight: bold;
        color: #83d4e5; /* Màu sắc của tiêu đề */
        text-align: center;
        font-family: 'Open Sans'; /* Phông chữ */
        margin-top: 20px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Đổ bóng cho tiêu đề */
    }


    .stButton > button {
        height: 45px; /* Giảm chiều cao nút để khớp với ô nhập liệu */
        padding: 0 10px; /* Điều chỉnh padding nếu cần */
        display: flex;
        text-sỉze: 5px; /* Kích thước chữ trong nút */
        margin-top: 30px;
        align-items: center;
        justify-content: center;    
    }

    div.stButton > button:first-child {
        background-color: #953608;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #45a049;
        color: #fff;
    }



    div.stButton > button[aria-label="📦 Save All Ingredients"] {
        width: 100%; /* hoặc giá trị cụ thể như 300px */
        max-width: 400px;  /* tránh vượt quá */
        padding: 12px 24px;
        font-size: 18px;
        border-radius: 8px;
        background-color: #FF5733;
        color: white;
    }

    /* Thay đổi phong cách cho selectbox */
    div.stSelectbox > div { 
        border-radius: 1px; /* Bo tròn góc */
        font-size: 16px; /* Kích thước chữ */
        font-family: 'Poppins', sans-serif; /* Font chữ */
        color: #333; /* Màu chữ */
        transition: all 0.3s ease; /* Hiệu ứng chuyển động */
    }

    /* Hiệu ứng hover cho selectbox */
    div.stSelectbox > div:hover {
        border-color: #45a049; /* Đổi màu viền khi hover */
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Thêm bóng mờ khi hover */
    }

    /* Style cho label */
    label[for="selectbox"] {
        font-size: 18px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 10px;
    }


}
    </style>
    """,
    unsafe_allow_html=True
)
from Generate_Receipt.main import load_and_generate_recipes
# Cấu hình đường dẫn
CSV_PATH = "ingredients.csv"



# Khởi tạo CSV nếu chưa tồn tại
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=["name", "category", "count"])
    df.to_csv(CSV_PATH, index=False)

st.markdown("<div class='title_main'>Fridgey</div>", unsafe_allow_html=True)

siddbar_option = ["Home", "Recommendation Recipe", "Collection Component", "Collection By Image"]
st.sidebar.title("Navigation")
selected_sidebar = st.sidebar.selectbox("Select Option", siddbar_option)

if selected_sidebar == "Home":
    home.get_page_home()
elif selected_sidebar == "Recommendation Recipe":
    rr.RecommendationRecipe()
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







# Footer
st.markdown("---")
st.markdown("© 2025 My App. All rights reserved.")