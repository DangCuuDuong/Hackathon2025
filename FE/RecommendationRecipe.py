import streamlit as st
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

from Generate_Receipt.main import load_and_generate_recipes
from Generate_Receipt.meal_plan_generator import main
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

    if st.button("View", key="view_recommendation_button"):
        main()
        
    with open("Generate_Receipt/meal_plan.json", "r", encoding="utf-8") as f:
        meal_plans = json.load(f)

    st.markdown("<div class='one1'>📅 Daily Meal Plan</div>", unsafe_allow_html=True)

    for day_plan in meal_plans:
        st.markdown(f"<h2>📆 {day_plan['day']}</h2>", unsafe_allow_html=True)
        
        for meal in day_plan.get("meals", []):
            
            st.markdown(f"<h5>🍴 {meal['meal_name']}</h5>", unsafe_allow_html=True)
            
            recipes = meal.get("recipes", [])
            for i in range(0, len(recipes), 3):
                cols = st.columns(2)
                for j in range(3):
                    if i + j < len(recipes):
                        recipe = recipes[i + j]
                        with cols[j]:
                            st.markdown(f"<div class='recipe_suggestion'>🍽️ {recipe['name']}</div>", unsafe_allow_html=True)
                            st.markdown(f"📝 _{recipe.get('description', 'No description')}_", unsafe_allow_html=True)

                            # Thành phần nổi bật
                            highlights = recipe.get("highlighted_ingredients", [])
                            if highlights:
                                st.markdown("🧂 **Main Ingredients:**")
                                st.write(", ".join(highlights))

                            st.markdown(f"🌶️ **Spice:** {recipe.get('spice_level', 'N/A')}")
                            st.markdown(f"🥗 **Diet:** {recipe.get('diet_type', 'N/A')}")
                            st.markdown(f"💪 **Suitable For:** {', '.join(recipe.get('suitable_for', []))}")

                            # Nutrition facts
                            nutrition = recipe.get("nutrition", {})
                            if nutrition:
                                st.markdown("📊 **Nutrition Facts:**")
                                col1, col2= st.columns(2)
                                with col1:
                                    st.write(f"- Calories: {nutrition.get('calories', 'N/A')}")
                                    st.write(f"- Protein: {nutrition.get('protein', 'N/A')}")                                
                                    st.write(f"- Carbs: {nutrition.get('carbs', 'N/A')}")
                                with col2:
                                    st.write(f"- Fat: {nutrition.get('fat', 'N/A')}")
                                    st.write(f"- Fiber: {nutrition.get('fiber', 'N/A')}")
                                    st.write(f"- Sugar: {nutrition.get('sugar', 'N/A')}")
                                    st.write(f"- Sodium: {nutrition.get('sodium', 'N/A')}")

                            # View details
                            with st.expander("👀 View details"):
                                st.markdown("**Ingredients:**")
                                for ing in recipe.get("ingredients", []):
                                    st.write(f"- {ing['name']}: {ing['quantity']}")
                                st.markdown("**Steps:**")
                                for step in recipe.get("steps", []):
                                    st.markdown(f"🔹 {step}")
                                
                                avoided = recipe.get("avoided_ingredients", [])
                                if avoided:
                                    st.markdown("🚫 **Avoided Ingredients:**")
                                    st.write(", ".join(avoided))

                                ref = recipe.get("reference")
                                if ref:
                                    st.markdown(f"[🔗 Reference]({ref})")
    if st.button("Go to Market", key="go_to_market_button"):
        with open('Generate_Receipt/processed_ingredients_plan.json', 'r') as f:
            food_need = json.load(f)
        df_gotomarket = pd.DataFrame(
                                    [(k, v["quantity"]) for k, v in food_need.items()],
                                    columns=["name", "quantity"]
                                    )
        st.dataframe(df_gotomarket, use_container_width=True)
        
            


