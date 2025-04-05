from BE.predict_food import predict_multiple_objects

image_path = 'image.png'  # Thay bằng đường dẫn ảnh của bạn
counts = predict_multiple_objects(image_path)
print("📊 Kết quả nhận diện và đếm vật thể:")
for label, count in counts.items():
    print(f" - {label}: {count}")
