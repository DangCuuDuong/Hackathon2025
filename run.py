import json
from BE.predict_food import predict_objects_and_weight
from JSON_FILE.combine import combind_json
image_path = 'image.png'  # ảnh bạn vừa gửi

image_path = 'image.png'
result = predict_objects_and_weight(image_path)

# === Ghi kết quả ra file JSON ===
with open("JSON_FILE/predict.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

combind_json("JSON_FILE/main.json", "JSON_FILE/predict.json")