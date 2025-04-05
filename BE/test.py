import os
import cv2
import numpy as np
import joblib
import tkinter as tk
from tkinter import filedialog
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

# === Hàm dự đoán ảnh và hiển thị kết quả ===
def test_image_gui(image_path):
    vec = preprocess_image(image_path)
    vec = vec.reshape(1, -1)

    pred = model.predict(vec)
    class_name = encoder.inverse_transform(pred)[0]

    # Hiển thị ảnh với nhãn
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.resize(img, (400, 400))
        cv2.putText(img, f"Predicted: {class_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Kết quả", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Không đọc được ảnh.")

# === Giao diện chọn ảnh ===
def open_file_dialog():
    filepath = filedialog.askopenfilename(
        title="Chọn ảnh để dự đoán",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if filepath:
        print(f"🖼 Ảnh được chọn: {filepath}")
        test_image_gui(filepath)

# === Tạo GUI đơn giản với Tkinter ===
def main_gui():
    root = tk.Tk()
    root.title("AI - Phân loại ảnh bằng VGG16 + Logistic Regression")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tk.Label(root, text="Kéo hoặc chọn ảnh để phân loại", font=("Arial", 14))
    label.pack(pady=20)

    btn = tk.Button(root, text="📂 Chọn ảnh", command=open_file_dialog, font=("Arial", 12))
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
