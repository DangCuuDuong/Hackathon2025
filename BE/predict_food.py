import cv2
import numpy as np
import joblib
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import img_to_array

# === CẤU HÌNH ===
IMG_SIZE = (244, 244)
MODEL_PATH = 'BE/PKL/logistic_regression.pkl'
ENCODER_PATH = 'BE/PKL/label_encoder.pkl'

# === Load mô hình ML + LabelEncoder ===
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

# === Load mô hình VGG16 trích đặc trưng ===
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(244, 244, 3))
x = GlobalAveragePooling2D()(base_model.output)
vgg_model = Model(inputs=base_model.input, outputs=x)

# === Tiền xử lý ảnh giống khi training ===
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Ảnh không hợp lệ!")

    # Tìm ROI tự động
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        img = img[y:y + h, x:x + w]

    img = cv2.resize(img, IMG_SIZE)
    img = img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = vgg_model.predict(img)
    return features.flatten()

# === Hàm dự đoán ===
def predict_image(image_path):
    vec = preprocess_image(image_path)
    vec = vec.reshape(1, -1)
    pred = model.predict(vec)
    class_name = encoder.inverse_transform(pred)[0]
    return class_name

# === Gọi thử hàm ===
if __name__ == "__main__":
    result = predict_image('image.png')
    print("✅ Kết quả nhận diện:", result)

#lấy hàm predict_image(image_path) để nhận diện ảnh từ bên ngoài