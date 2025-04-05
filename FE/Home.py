import json
import os
import pandas as pd
import streamlit as st

from BE.input_clean import clean_ingredient_name
from Generate_Receipt.main import load_and_generate_recipes

def get_page_home():
    with open('JSON_FILE/main.json', 'r') as f:
        json_data = json.load(f)

    # Chuyển thành DataFrame
    df_components = pd.DataFrame(list(json_data.items()), columns=["name", "count"])
    df_components = df_components.sort_values(by="count", ascending=False)

    if not df_components.empty:
        # Hiển thị bảng
        st.markdown("<div class='one1'; >Current Ingredients</div>", unsafe_allow_html=True)
        st.dataframe(df_components, use_container_width=True)


    # --- CHẾ ĐỘ ĂN UỐNG ---
    # --- DIET TYPE ---
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='one2'>🥗 Suitable Diet Type</div>", unsafe_allow_html=True)
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

        with col2:
            st.markdown("<div class='one2'>🌶️ Your Spiciness Level</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='one1'>🍽️ Personal Food Preferences</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        favorite_dish = st.text_input("🥰 What is your favorite dish? (separate multiple with commas)")
        favorite_dish = clean_ingredient_name(favorite_dish)  # Chuẩn hóa tên món ăn
    with col2: 
        disliked_dish = st.text_input("⚠️ Any dish you dislike or are allergic to? (separate multiple with commas)")
        disliked_dish = clean_ingredient_name(disliked_dish)  # Chuẩn hóa tên món ăn

    main_json_path = "JSON_FILE/main.json"

    # Lưu user ingredients từ main.json
    if os.path.exists(main_json_path):
        with open(main_json_path, 'r', encoding='utf-8') as f:
            main_data = json.load(f)

        ingredient_list = list(main_data.keys())
        col1, col2, col3 = st.columns([2, 2, 1])  # tỉ lệ giữa 3 cột

        with col2:
            if st.button("📦 Save All Ingredients", key="save_all_ingredients"):
                data_to_save = {
                    "user_ingredients": ingredient_list
                }

                # ⚠️ Sửa lỗi đường dẫn bị sai khoảng trắng
                with open("Generate_Receipt/user_ingredients.json", "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

                st.toast("✅ All ingredients saved successfully!", icon="📦")
                st.json(data_to_save)

    # --- GỢI Ý CÔNG THỨC ---

    recipes = load_and_generate_recipes()

    st.markdown("<div class='one1'>🍽️ Recipe Suggestions</div>", unsafe_allow_html=True)

    if recipes:
        for i in range(0, len(recipes), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(recipes):
                    recipe = recipes[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='recipe_suggestion'>🍽️ {recipe['name']}</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='one1'>🍽️ Select Your Cooking</div>", unsafe_allow_html=True)

    # Lấy danh sách tên món
    recipe_names = [recipe.get("name", "Unnamed") for recipe in recipes]

    selected_recipe_name = st.selectbox("🍽️ Choose your favorite recipe:", recipe_names)

    # Tìm công thức tương ứng
    selected_recipe = next((r for r in recipes if r.get("name") == selected_recipe_name), None)

    if selected_recipe:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### ✅ You selected: **{selected_recipe_name}**")
            st.markdown(f"📝 _{selected_recipe.get('description', 'No description')}_", unsafe_allow_html=True)

            st.markdown("**🧂 Ingredients:**")
            for ing in selected_recipe.get("ingredients", []):
                st.write(f"- {ing['name']}: {ing['quantity']}")
        with col2:
            st.markdown("**👩‍🍳 Steps:**")
            for step in selected_recipe.get("steps", []):
                st.markdown(f"🔹 {step}")

            st.markdown("**🌶️ Spice Level:** " + selected_recipe.get("spice_level", "N/A"))
            st.markdown("**🥗 Diet Type:** " + selected_recipe.get("diet_type", "N/A"))
    import re

    def extract_quantity_number(qty_str):
        match = re.match(r"\s*(\d+)", qty_str)
        return int(match.group(1)) if match else 1
    def cook_recipe():
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
        st.dataframe(df_components)

    # NÚT "NẤU" - TRỪ NGUYÊN LIỆU
    with st.container():
        st.markdown("---")
        col1, col2, col3 =st.columns([2,2,1])
        with col2:
            if st.button("👨‍🍳 Cook this recipe"):
                cook_recipe()
    