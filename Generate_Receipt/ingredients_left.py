import json
import os

# Hàm đọc file nguyên liệu và quy đổi khẩu phần
def process_ingredients(input_file, output_file):
    # Đọc dữ liệu từ file JSON đầu vào
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    ingredients_used = {}  # Dictionary để lưu nguyên liệu và số lượng sử dụng

    # Duyệt qua tất cả các công thức
    for recipe in data:
        # Lấy danh sách nguyên liệu trong công thức
        ingredients = recipe.get("ingredients", [])
        
        # Duyệt qua từng nguyên liệu và quy đổi
        for ingredient in ingredients:
            name = ingredient.get("name")
            quantity = ingredient.get("quantity")
            
            if name and quantity:
                # Quy đổi số lượng nguyên liệu về số âm (đại diện cho việc nguyên liệu bị giảm sau khi nấu)
                # Ví dụ: nếu nguyên liệu đã có trong dictionary, giảm số lượng đi, nếu không, thêm mới
                if name not in ingredients_used:
                    ingredients_used[name] = {"quantity": 0, "unit": quantity}  # Khởi tạo số lượng ban đầu
                
                # Cộng thêm số lượng đã sử dụng (số lượng sẽ được quy đổi về dạng số âm)
                # Cần xử lý để lấy được đơn vị số và đơn vị của nguyên liệu (ví dụ "200g", "1 tsp", v.v.)
                quantity_value = int(extract_quantity(quantity))
                ingredients_used[name]["quantity"] -= quantity_value
    
    # Lưu dữ liệu nguyên liệu đã xử lý vào file JSON mới
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ingredients_used, f, ensure_ascii=False, indent=4)
    
    print(f"Processed ingredients have been saved to {output_file}")

# Hàm trích xuất số lượng từ chuỗi (ví dụ: "200g" -> 200)
def extract_quantity(quantity_str):
    # Xử lý chuỗi như "200g", "1 tsp", ... để lấy phần số
    try:
        quantity_value = float(''.join(filter(str.isdigit, quantity_str)))
    except ValueError:
        quantity_value = 0  # Nếu không có số trong chuỗi, mặc định là 0
    return quantity_value

# Test hàm với file input và output
input_file = "recipes.json"  # Đảm bảo rằng file này tồn tại trong thư mục
output_file = "processed_ingredients.json"  # File lưu nguyên liệu đã xử lý

process_ingredients(input_file, output_file)
