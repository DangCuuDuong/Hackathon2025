import json
from Generate_Receipt.recipe_generator import main as generate_recipes

def load_and_generate_recipes(
    ingredients_path="Generate_Receipt/user_ingredients.json",
    preferences_path="Generate_Receipt/preferences.json",
    health_path="Generate_Receipt/health.json",
    show_sample=True
):
    try:
        # Đọc dữ liệu từ các file
        with open(ingredients_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(preferences_path, "r", encoding="utf-8") as f:
            preferences = json.load(f)
        with open(health_path, "r", encoding="utf-8") as f:
            health = json.load(f)

        # Lấy danh sách thông tin
        user_ingredients = data.get("user_ingredients", [])
        user_preferences = preferences.get("user_preferences", [])
        user_health = health.get("user_health", [])

        # Gọi hàm sinh công thức
        recipes = generate_recipes(user_ingredients, user_preferences, user_health)

        # Hiển thị mẫu công thức đầu tiên (tùy chọn)
        if show_sample and recipes:
            print("\n🥘 Sample recipe preview:")
            print("Name:", recipes[0].get("name", "N/A"))
            print("Ingredients:", ", ".join(i.get("name", "") for i in recipes[0].get("ingredients", [])))
            print("Steps:", ", ".join(recipes[0].get("steps", [])))

        return recipes

    except Exception as e:
        print(f"❌ Error while generating recipes: {e}")
        return []
