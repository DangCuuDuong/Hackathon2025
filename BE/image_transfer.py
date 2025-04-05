import os
import cv2
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
import tensorflow as tf
from tqdm import tqdm
seed_value = 50
np.random.seed(seed_value)
random.seed(seed_value)
tf.random.set_seed(seed_value)
# === CẤU HÌNH ===
DATASET_DIR = "BE/train"
IMG_SIZE = (244, 244)
TEST_SIZE = 0.2
AUGMENT = False  # Bật True nếu muốn tăng cường dữ liệu
SAVE_DIR = "BE/CSV"

# === LOAD VGG16 với GlobalAveragePooling2D và fine-tune 4 tầng cuối ===
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(244, 244, 3))
base_model.trainable = True

for layer in base_model.layers[:-4]:  # Chỉ fine-tune 4 tầng cuối
    layer.trainable = False

x = GlobalAveragePooling2D()(base_model.output)  # Giảm xuống 512 chiều
vgg_model = Model(inputs=base_model.input, outputs=x)

# === HÀM TĂNG CƯỜNG DỮ LIỆU ===
def augment_image(img):
    if random.random() < 0.5:
        img = cv2.flip(img, 1)
    angle = random.choice([0, 90, 180, 270])
    if angle:
        img = cv2.rotate(img, getattr(cv2, f"ROTATE_{angle}_CLOCKWISE"))
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img

# === HÀM TRÍCH ĐẶC TRƯNG ===
def extract_features(image_path, augment=False):
    img = cv2.imread(image_path)
    if img is None:
        return None

    # --- Trích ROI ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        img = img[y:y+h, x:x+w]  # Cắt ROI

    img = cv2.resize(img, IMG_SIZE)
    if augment:
        img = augment_image(img)
    img = img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = vgg_model.predict(img)
    return features.flatten()

# === BƯỚC 1: Load đường dẫn ảnh + nhãn ===
image_paths, labels = [], []

for class_name in os.listdir(DATASET_DIR):
    class_dir = os.path.join(DATASET_DIR, class_name)
    if not os.path.isdir(class_dir):
        continue
    for fname in os.listdir(class_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_paths.append(os.path.join(class_dir, fname))
            labels.append(class_name)

# === BƯỚC 2: Chia tập train/val ===
train_paths, val_paths, train_labels, val_labels = train_test_split(
    image_paths, labels, test_size=TEST_SIZE, stratify=labels, random_state=42)

# === BƯỚC 3: Hàm xử lý và lưu ===
def process_and_save(paths, labels, save_csv):
    feature_list = []
    label_list = []

    for img_path, label in tqdm(zip(paths, labels), total=len(paths), desc=f"📦 Processing {save_csv}"):
        vec = extract_features(img_path, augment=AUGMENT)
        if vec is not None:
            feature_list.append(vec)
            label_list.append(label)

    df = pd.DataFrame(feature_list)
    df['label'] = label_list
    os.makedirs(os.path.dirname(save_csv), exist_ok=True)
    df.to_csv(save_csv, index=False)
    print(f"✅ Saved: {save_csv}")

# === BƯỚC 4: Thực thi ===
process_and_save(train_paths, train_labels, os.path.join(SAVE_DIR, "train_features.csv"))
process_and_save(val_paths, val_labels, os.path.join(SAVE_DIR, "val_features.csv"))
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 👇 Sau khi bạn có biến `labels` hoặc `y_train`
encoder = LabelEncoder()
encoder.fit(labels)  # hoặc y_train

# ✅ Lưu vào thư mục BE/PKL
os.makedirs("BE/PKL", exist_ok=True)
joblib.dump(encoder, "BE/PKL/label_encoder.pkl")
print("✅ Đã lưu label_encoder vào BE/PKL/label_encoder.pkl")
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 👇 Sau khi bạn có biến `labels` hoặc `y_train`
encoder = LabelEncoder()
encoder.fit(labels)  # hoặc y_train

# ✅ Lưu vào thư mục BE/PKL
os.makedirs("BE/PKL", exist_ok=True)
joblib.dump(encoder, "BE/PKL/label_encoder.pkl")
print("✅ Đã lưu label_encoder vào BE/PKL/label_encoder.pkl")
