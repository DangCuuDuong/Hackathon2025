import openai
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# 1. Cấu hình API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

# # 2. Nguyên liệu người dùng có
# user_ingredients = [
#     "chicken", "tomato", "tofu", "onion", "garlic", "beef",
#     "potato", "carrot", "sugar", "red pepper powder", "salt",
#     "sesame oil", "cooking oil"
# ]

# 3. Mẫu JSON đầu ra
recipe_form = {
    "name": "Recipe Name",
    "description": "A brief description of the dish.",
    "nutrition": {
        "calories": "Calories info",
        "protein": "Protein g",
        "carbs": "Carbohydrates g",
        "fat": "Fat g",
        "fiber": "Fiber g",
        "sugar": "Sugar g",
        "sodium": "Sodium mg"
    },
    "ingredients": [
        {"name": "example", "quantity": "100g"}
    ],
    "steps": ["Step 1", "Step 2"],
    "spice_level": "not spicy/ little / medium / spicy / very spicy",
    "diet_type": "eat clean / keto / low carb / v.v.",
    "suitable_for": ["muscle gain", "diet", "gym goer"],  # list mục tiêu phù hợp
    "highlighted_ingredients": ["chicken breast", "tofu"],  # từ sở thích
    "avoided_ingredients": ["butter", "duck eggs"],  # nếu có
    "reference": "Recipe reference website url"
}


def build_prompt(ingredients, preferences, health):
    # Kiểm tra kiểu dữ liệu của health và preferences
    if isinstance(preferences, list):
        preferences = {key: preferences for key in ["spice_level", "diet_type", "allergies_or_dislikes", "favorite_foods"]}
    
    if isinstance(health, list):
        health = {key: {} for key in ["health_status", "health_goals", "nutrition_targets"]}

    return f"""
You have access to a list of ingredients currently available in a user's refrigerator.

**Available ingredients:** {", ".join(ingredients)}

Additionally, the user has shared their personal preferences and health condition:

### 🍱 Personal Preferences
- Spice tolerance: {preferences.get("spice_level", "not specified")}
- Diet type: {", ".join(preferences.get("diet_type", []))}
- Food allergies or dislikes: {", ".join(preferences.get("allergies_or_dislikes", []))}
- Favorite ingredients: {", ".join(preferences.get("favorite_foods", []))}

### ❤️ Health Condition
- General condition: {health.get("health_status", "not specified")}
- Health goal: {health.get("health_goals", "not specified")}
- Desired nutrients/calories: {", ".join([f"{key}: {value}" for key, value in health.get("nutrition_targets", {}).items()]) if isinstance(health.get("nutrition_targets", {}), dict) else "not specified"}

---

Based on all of the above, suggest **five recipes** that can be made.

### 🧠 Recipe Selection Criteria
1. Prioritize recipes that use as many available ingredients as possible.
2. Respect dietary preferences (e.g., vegetarian, keto), avoid any listed allergies/dislikes, and include favorite ingredients if possible.
3. Adjust spice level to fit the user's preference.
4. Align the recipe with health goals (e.g., low sugar for diabetes, high protein for muscle gain).
5. Add numbers to each step of the recipe.
6. Write a detailed recipe that includes:
    - Preparation instructions: how to wash, peel, cut, or marinate each ingredient.
    - Step-by-step cooking instructions with clear order of operations.
    - Precise cooking times and temperatures for each step (e.g., "simmer for 10 minutes at medium heat").
    - Ensure clarity and completeness so anyone can follow and cook the dish successfully.
7. Ensure that the **quantities listed in the ingredients section match the quantities used in the steps**.
8. Use **common kitchen measurements** such as grams (g), milliliters (ml), teaspoons (tsp), tablespoons (tbsp), and cups.

### ✅ Output Format (Valid JSON)
[
    {json.dumps(recipe_form, indent=4, ensure_ascii=False)},
    ...
]
"""


# 5. Gửi prompt và xử lý response
def get_recipes(ingredients, preferences, health):
    prompt = build_prompt(ingredients, preferences, health)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    recipe_data = response.choices[0].message.content

    # Bỏ ```json nếu có
    recipe_data = re.sub(r"```json\n(.*?)\n```", r"\1", recipe_data, flags=re.DOTALL).strip()

    try:
        return json.loads(recipe_data)
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return None

# 6. Hàm chạy chính
def main(ingredients, preferences, health):
    recipes = get_recipes(ingredients, preferences, health)
    if recipes:
        with open("recipes.json", "w", encoding="utf-8") as f:
            json.dump(recipes, f, indent=4, ensure_ascii=False)

        print("\n🎉 Successfully generated recipes:")
        for recipe in recipes:
            print(f"🍽️  {recipe['name']}: uses {len(recipe['ingredients'])} ingredients.")
    return recipes


# if __name__ == "__main__":
#     default_ingredients = [
#         "chicken", "tomato", "tofu", "onion", "garlic", "beef",
#         "potato", "carrot", "sugar", "red pepper powder", "salt",
#         "sesame oil", "cooking oil"
#     ]
#     main(default_ingredients)

