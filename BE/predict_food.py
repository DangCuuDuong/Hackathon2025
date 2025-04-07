import cv2
import numpy as np
import joblib
from collections import Counter
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import img_to_array

# === CẤU HÌNH ===
IMG_SIZE = (244, 244)
MODEL_PATH = 'BE/PKL/logistic_regression.pkl'
ENCODER_PATH = 'BE/PKL/label_encoder.pkl'
WEIGHT_MAP = {
    'apple': 180,
    'banana': 120,
    'beef': 150,           # 1 miếng ~150g
    'beetroot': 130,
    'bell pepper': 120,
    'cabbage': 500,        # 1 bắp nhỏ ~500g
    'carrot': 100,
    'cauliflower': 600,    # 1 bông ~600g
    'chicken': 200,        # 1 miếng ~200g
    'corn': 250,           # 1 trái bắp
    'cucumber': 200,
    'eggplant': 150,
    'eggs': 60,            # 1 quả trứng gà
    'nuts': 30,            # 1 nắm nhỏ
    'pineapple': 1000,     # 1 trái ~1kg
    'pork': 150,           # 1 miếng thịt
    'potato': 130,
    'sweetcorn': 200,
    'sweetpotato': 150,
    'tomato': 100
}

# === Load mô hình ML + LabelEncoder ===
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

# === Load mô hình VGG16 trích đặc trưng ===
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(244, 244, 3))
x = GlobalAveragePooling2D()(base_model.output)
vgg_model = Model(inputs=base_model.input, outputs=x)

# === Hàm xử lý ảnh đầu vào và trích đặc trưng cho 1 vật thể ===
def extract_features_from_roi(roi):
    roi = cv2.resize(roi, IMG_SIZE)
    roi = img_to_array(roi)
    roi = preprocess_input(roi)
    roi = np.expand_dims(roi, axis=0)
    features = vgg_model.predict(roi)
    return features.flatten().reshape(1, -1)

# === Hàm nhận diện và đếm vật thể trong ảnh ===
# === Hàm nhận diện và tính khối lượng vật thể trong ảnh ===
def predict_objects_and_weight(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("❌ Ảnh không hợp lệ!")

    orig_img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.dilate(binary, kernel, iterations=2)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    results = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 300:
            continue

        roi = orig_img[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi, IMG_SIZE)
        roi_array = img_to_array(roi_resized)
        roi_array = preprocess_input(roi_array)
        roi_array = np.expand_dims(roi_array, axis=0)

        feature = vgg_model.predict(roi_array).flatten().reshape(1, -1)
        pred = model.predict(feature)
        label = encoder.inverse_transform(pred)[0]
        results.append(label)

        # Vẽ khung
        cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(orig_img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (36, 255, 12), 2)

    cv2.imwrite("output_detected.png", orig_img)

    # Đếm số lượng và tính khối lượng
    count_result = Counter(results)
    weight_result = {}
    for label, count in count_result.items():
        weight = WEIGHT_MAP.get(label, 0)
        total_weight = weight * count
        weight_result[label] =  total_weight
    
    return weight_result


# === Test thử ===
if __name__ == "__main__":
    image_path = 'image.png'
    result = predict_objects_and_weight(image_path)
