import streamlit as st
import pandas as pd
import os
import json
from JSON_FILE.combine import combind_json
from BE.input_clean import clean_ingredient_name
CSV_PATH = "ingredients.csv"

def output_json(df):
    data_dict = dict(zip(df["name"], df["count"]))
    with open("JSON_FILE/main.json", "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

def create_recommendation():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=["name", "count"]).astype({"count": int})

    st.header("➕ Add New Ingredient")
    name = st.text_input("Ingredient name (e.g., Salt)")
    name = clean_ingredient_name(name)  # Chuẩn hóa tên nguyên liệu
    count = st.number_input("Count", min_value=1, value=1, step=1)
    add_components = st.button("Add Ingredient")

    if add_components:
        if name.strip():
            # ✅ Cập nhật CSV
            if name in df["name"].values:
                df.loc[df["name"] == name, "count"] += count
            else:
                df = pd.concat([df, pd.DataFrame([{"name": name, "count": count}])], ignore_index=True)
            df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

            # ✅ Ghi vào add.json
            add_json_path = "Generate_Receipt/add.json"
            if os.path.exists(add_json_path):
                with open(add_json_path, "r", encoding="utf-8") as f:
                    add_data = json.load(f)
            else:
                add_data = {}

            if name in add_data:
                add_data[name] += count
            else:
                add_data[name] = count

            with open(add_json_path, "w", encoding="utf-8") as f:
                json.dump(add_data, f, ensure_ascii=False, indent=4)

            st.success(f"✅ Added {count} x {name}")
        else:
            st.warning("⚠️ Please enter a valid ingredient name.")


    # ✅ Nút Merge
    if st.button("🔄 Merge CSV ➜ main.json"):
        if os.path.exists(CSV_PATH):
            # Đọc dữ liệu từ CSV
            df_csv = pd.read_csv(CSV_PATH, encoding='utf-8-sig')

            # Nhóm lại nếu có trùng
            df_merged = df_csv.groupby('name', as_index=False)['count'].sum()

            # Ghi đè lại CSV
            df_merged.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

            # ✅ Ghi vào main.json (output)
            output_json(df_merged)

            st.success("✅ Ingredients merged and saved to main.json.")
            st.dataframe(df_merged)
        else:
            st.error("❌ Missing ingredients.csv file.")