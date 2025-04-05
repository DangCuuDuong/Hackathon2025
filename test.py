import json
from BE.predict_food import predict_multiple_objects
from JSON_FILE.combine import combind_json
image_path = 'image.png'  # ảnh bạn vừa gửi
counts = predict_multiple_objects(image_path)

# === Ghi kết quả ra file JSON ===
with open("JSON_FILE/predict.json", "w", encoding="utf-8") as f:
    json.dump(counts, f, ensure_ascii=False, indent=4)

combind_json("JSON_FILE/main.json", "JSON_FILE/predict.json")