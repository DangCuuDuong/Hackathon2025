import streamlit as st
import pandas as pd
import os
import json

from Generate_Receipt.main import load_and_generate_recipes

def RecommendationRecipe():
    with open('JSON_FILE/main.json', 'r') as f:
        json_data = json.load(f)

    # Chuyển thành DataFrame
    df_components = pd.DataFrame(list(json_data.items()), columns=["name", "count"])
    df_components = df_components.sort_values(by="count", ascending=False)

    if not df_components.empty:
        # Hiển thị bảng
        st.markdown("<div class='one1'; >Current Ingredients</div>", unsafe_allow_html=True)
        st.dataframe(df_components, use_container_width=True)

    st.button("View", key="view_recommendation_button")


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


