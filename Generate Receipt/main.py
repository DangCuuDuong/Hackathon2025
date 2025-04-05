import json
from recipe_generator import main as generate_recipes

# Đọc dữ liệu từ file JSON
with open("ingredients.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Lấy danh sách nguyên liệu
user_ingredients = data.get("user_ingredients", [])

# Gọi hàm và lấy kết quả
recipes = generate_recipes(user_ingredients)

# Nếu muốn: hiển thị thêm nội dung gì đó
if recipes:
    print("\n🥘 Sample recipe preview:")
    print(recipes[0]['name'])
    print("Ingredients:", ", ".join([i['name'] for i in recipes[0]['ingredients']]))
    print("Steps:", ", ".join(recipes[0]['steps']))
