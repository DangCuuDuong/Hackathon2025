import json

def combind_json(main_file, other_file):
    # === Đọc dữ liệu từ file predict ===
    with open(other_file, 'r', encoding='utf-8') as f:
        predict_data = json.load(f)

    # === Đọc dữ liệu từ file main (nếu chưa có thì tạo mới) ===
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            main_data = json.load(f)
    except FileNotFoundError:
        main_data = {}

    # === Cập nhật dữ liệu ===
    for item, qty in predict_data.items():
        if item in main_data:
            main_data[item] += qty  # Cộng dồn
        else:
            main_data[item] = qty   # Thêm mới

    # === Loại bỏ những nguyên liệu có giá trị <= 0 ===
    main_data = {k: v for k, v in main_data.items() if v > 0}

    # === Ghi lại vào main.json ===
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=4)

    # === Xóa nội dung predict.json ===
    with open(other_file, 'w', encoding='utf-8') as f:
        json.dump({}, f)
