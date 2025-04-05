import json
from recipe_generator import main as generate_recipes

# Đọc dữ liệu từ file JSON
with open("ingredients.json", "r", encoding="utf-8") as f:
    data = json.load(f)
with open("preferences.json", "r", encoding="utf-8") as f:
    preferences = json.load(f)
with open("health.json", "r", encoding="utf-8") as f:
    health = json.load(f)

# Lấy danh sách nguyên liệu, sở thích và sức khỏe
user_ingredients = data.get("user_ingredients", [])
user_preferences = data.get("user_preferences", [])
user_health = data.get("user_health", [])

# Gọi hàm và lấy kết quả
recipes = generate_recipes(user_ingredients, user_preferences, user_health)

# Nếu muốn: hiển thị thêm nội dung gì đó
if recipes:
    print("\n🥘 Sample recipe preview:")
    print(recipes[0]['name'])
    print("Ingredients:", ", ".join([i['name'] for i in recipes[0]['ingredients']]))
    print("Steps:", ", ".join(recipes[0]['steps']))
