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
import FE.Home as home

st.set_page_config(page_title="Smart Refrigerator", page_icon="🍽️")


st.markdown(
    """
    <style>
    .title_main {
        font-size: 60px !important; 
        font-weight: bold;
        color: #54b8cf; /* Màu sắc của tiêu đề */
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        font-family: 'Open Sans'; /* Phông chữ */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Đổ bóng cho tiêu đề */
    }

    .one1{
        font-size: 35px !important;
        font-weight: bold;
        color: #eab676; /* Màu sắc của tiêu đề */
        color: #FFFFF; /* Màu sắc của tiêu đề */
        text-align: left;
        font-family: 'Open Sans'; /* Phông chữ */
    }


    .stButton > button {
        height: 38px; /* Giảm chiều cao nút để khớp với ô nhập liệu */
        padding: 0 10px; /* Điều chỉnh padding nếu cần */
        display: flex;
        text-sỉze: 5px; /* Kích thước chữ trong nút */
        margin-top: 30px;
        align-items: center;
        justify-content: center;
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

st.markdown("<div class='title_main'>Smart Refrigerator</div>", unsafe_allow_html=True)

siddbar_option = ["Home", "Collection Component", "Collection By Image"]
st.sidebar.title("Navigation")
selected_sidebar = st.sidebar.selectbox("Select Option", siddbar_option)

if selected_sidebar == "Home":
    home.get_page_home()
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

# --- CHẾ ĐỘ ĂN UỐNG ---
# --- DIET TYPE ---
st.markdown("## 🥗 Suitable Diet Type")
diet_option = st.selectbox(
    "Choose the diet you’re interested in:",
    [
        "Normal",
        "Vegetarian",
        "Healthy",
        "Keto (Low Carb)",
        "High Protein",
        "Weight Loss",
        "Diabetic-friendly"
    ]
)

# --- SPICY LEVEL ---
st.markdown("## 🌶️ Your Spiciness Level")
spicy_level = st.selectbox(
    "Choose your spiciness level:",
    [
        "none",
        "little",
        "medium",
        "high",
        "super hot"
    ]
)

# --- PERSONAL FOOD PREFERENCES ---
st.markdown("## 🍽️ Personal Food Preferences")
favorite_dish = st.text_input("🥰 What is your favorite dish? (separate multiple with commas)")
disliked_dish = st.text_input("⚠️ Any dish you dislike or are allergic to? (separate multiple with commas)")
main_json_path = "JSON_FILE/main.json"

# Lưu user ingredients từ main.json
if os.path.exists(main_json_path):
    with open(main_json_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    ingredient_list = list(main_data.keys())

    if st.button("📦 Save All Ingredients"):
        data_to_save = {
            "user_ingredients": ingredient_list
        }

        # ⚠️ Sửa lỗi đường dẫn bị sai khoảng trắng
        with open("Generate_Receipt/user_ingredients.json", "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        st.success("✅ All ingredients saved successfully!")
        st.json(data_to_save)

# --- GỢI Ý CÔNG THỨC ---

recipes = load_and_generate_recipes()

st.markdown("## 🍱 Recipe Overview (3x3 Grid)")

if recipes:
    for i in range(0, len(recipes), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(recipes):
                recipe = recipes[i + j]
                with cols[j]:
                    st.markdown(f"### 🍽️ {recipe['name']}")
                    st.markdown(f"📝 _{recipe.get('description', 'No description')}_", unsafe_allow_html=True)

                    # Highlighted ingredients (nếu có)
                    highlights = recipe.get("highlighted_ingredients", [])
                    if highlights:
                        st.markdown("🧂 **Main Ingredients:**")
                        st.write(", ".join(highlights))

                    st.markdown(f"🌶️ **Spice:** {recipe.get('spice_level', 'N/A')}")
                    st.markdown(f"🥗 **Diet:** {recipe.get('diet_type', 'N/A')}")

                    # Optional: nút mở chi tiết
                    with st.expander("👀 View details"):
                        for ing in recipe.get("ingredients", []):
                            st.write(f"- {ing['name']}: {ing['quantity']}")
                        st.markdown("**Steps:**")
                        for step in recipe.get("steps", []):
                            st.markdown(f"🔹 {step}")

                    st.markdown("---")
else:
    st.warning("⚠️ No recipes found.")

# --- CHỌN MÓN YÊU THÍCH ---
st.markdown("## 🧡 Select Your Favorite Dish")

# Lấy danh sách tên món
recipe_names = [recipe.get("name", "Unnamed") for recipe in recipes]

selected_recipe_name = st.selectbox("🍽️ Choose your favorite recipe:", recipe_names)

# Tìm công thức tương ứng
selected_recipe = next((r for r in recipes if r.get("name") == selected_recipe_name), None)

if selected_recipe:
    st.markdown(f"### ✅ You selected: **{selected_recipe_name}**")
    st.markdown(f"📝 _{selected_recipe.get('description', 'No description')}_", unsafe_allow_html=True)

    st.markdown("**🧂 Ingredients:**")
    for ing in selected_recipe.get("ingredients", []):
        st.write(f"- {ing['name']}: {ing['quantity']}")

    st.markdown("**👩‍🍳 Steps:**")
    for step in selected_recipe.get("steps", []):
        st.markdown(f"🔹 {step}")

    st.markdown("**🌶️ Spice Level:** " + selected_recipe.get("spice_level", "N/A"))
    st.markdown("**🥗 Diet Type:** " + selected_recipe.get("diet_type", "N/A"))
import re

def extract_quantity_number(qty_str):
    match = re.match(r"\s*(\d+)", qty_str)
    return int(match.group(1)) if match else 1

# NÚT "NẤU" - TRỪ NGUYÊN LIỆU
if st.button("👨‍🍳 Cook this recipe"):
    used_ingredients = {}
    for ing in selected_recipe.get("ingredients", []):
        name = ing["name"]
        quantity = extract_quantity_number(ing["quantity"])
        used_ingredients[name] = -quantity  # số âm

    # Lưu vào file
    with open("Generate_Receipt/used_ingredients.json", "w", encoding="utf-8") as f:
        json.dump(used_ingredients, f, ensure_ascii=False, indent=4)

    st.success("✅ Cooking completed! Ingredients usage saved.")
    st.json(used_ingredients)

    from JSON_FILE.combine import combind_json
    JSON_FLE = "JSON_FILE/main.json"
    other_file = "Generate_Receipt/used_ingredients.json"
    combind_json(JSON_FLE, other_file)

    st.subheader("Current Ingredients")
    with open('JSON_FILE/main.json', 'r') as f:
        json_data = json.load(f)

    # Chuyển thành DataFrame
    df_components = pd.DataFrame(list(json_data.items()), columns=["name", "count"])
    df_components = df_components.sort_values(by="count", ascending=False)
    st.subheader("🧾 Current Ingredients")
    st.dataframe(df_components)  # hoặc st.table(df_components)

st.header("Selection spice level")
spice_level = st.selectbox("Select spice level", ["None", "Low", "Medium", "High"])
st.header("Selection spice level")
spice_level = st.selectbox("Select spice level", ["None", "Low", "Medium", "High"])




# Footer
st.markdown("---")
st.markdown("© 2025 My App. All rights reserved.")