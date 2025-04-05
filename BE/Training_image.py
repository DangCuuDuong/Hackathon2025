import numpy as np
import random
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from tabulate import tabulate
import joblib  # ✅ Thư viện để lưu mô hình
import os
# === Đặt seed để tái hiện kết quả ===
seed_value = 50
np.random.seed(seed_value)
random.seed(seed_value)
tf.random.set_seed(seed_value)

# === CẤU HÌNH CÁC MÔ HÌNH ===
MODELS = {
    'SVM (RBF Kernel)': SVC(kernel='rbf', probability=True, random_state=seed_value),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=seed_value)
}

# === HÀM LOAD DỮ LIỆU ===
def load_data(path):
    df = pd.read_csv(path)
    X = df.drop('label', axis=1).values
    y = df['label'].values
    return X, y

# === MAIN ===
def main():
    print("🚀 So sánh SVM & Logistic Regression + Lưu mô hình\n")

    # Load dữ liệu
    X_train, y_train = load_data('BE/CSV/train_features.csv')
    X_val, y_val = load_data('BE/CSV/val_features.csv')

    # Mã hóa label
    encoder = LabelEncoder()
    y_train_enc = encoder.fit_transform(y_train)
    y_val_enc = encoder.transform(y_val)

    # So sánh mô hình
    results = []

    for name, model in MODELS.items():
        print(f"\n🔧 Đang huấn luyện: {name}")
        model.fit(X_train, y_train_enc)
        y_pred = model.predict(X_val)

        acc = accuracy_score(y_val_enc, y_pred)
        f1 = f1_score(y_val_enc, y_pred, average='macro')

        results.append([name, round(acc * 100, 2), round(f1 * 100, 2)])

        # === Lưu mô hình thành file .pkl ===
        model_filename = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "") + ".pkl"
        save_path = os.path.join("BE", "PKL", model_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(model, save_path)

        print(f"💾 Mô hình đã lưu vào: {model_filename}")

    # In bảng kết quả
    print("\n📊 Kết quả so sánh mô hình:\n")
    print(tabulate(results, headers=["Mô hình", "Accuracy (%)", "F1-score (%)"], tablefmt="github"))

if __name__ == "__main__":
    main()
