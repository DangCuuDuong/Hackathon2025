import streamlit as st
import pandas as pd
import os
from pathlib import Path

CSV_PATH = "ingredients.csv"
componets_prepare = pd.DataFrame(columns=["name", "count"]).astype({"count": int})

def create_recommendation():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
    else:
        df = pd.DataFrame(columns=["name", "count"]).astype({"count": int})

    def update_csv(name, count_value=1):
        nonlocal df
        mask = (df["name"] == name)
        
        if df[mask].empty:
            new_row = {"name": name, "count": count_value}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df.loc[mask, "count"] += count_value
        
        df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
        return df

    # Input section
    st.header("Add New Ingredient")
    name = st.text_input("Ingredient name (e.g., Salt)")
    count = st.number_input("Count", min_value=1, value=1, step=1)
    add_components = st.button("Add Ingredient")

    if add_components:
        if name and count > 0:
            
            global componets_prepare
            if name in componets_prepare['name'].values:
                componets_prepare.loc[componets_prepare['name'] == name, 'count'] += count
            else:
                new_row = pd.DataFrame({'name': [name], 'count': [count]})
                componets_prepare = pd.concat([componets_prepare, new_row], ignore_index=True)
            
            st.success(f"Added {count} {name} successfully!")

    # Display results
    st.header("Components Prepare")
    if not componets_prepare.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Name")
            st.write(componets_prepare["name"].values)
        with col2:
            st.write("Count")
            st.write(componets_prepare["count"].values)
    else:
        st.write("No ingredients added yet.")

    


    # Export button
    if st.button("Merge Ingredients"):
        df_main = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
        df_combined = pd.concat([df_main, componets_prepare], ignore_index=True)
        df_main = df_combined.groupby('name', as_index=False)['count'].sum()
        df_main.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
        componets_prepare = pd.DataFrame(columns=componets_prepare.columns)
        output_json(df_main)


def output_json(df):
    summary = df.groupby("name")["count"].sum().to_dict()

    with open("ingredients.json", "w", encoding='utf-8') as f:
        import json
        json.dump(summary, f, ensure_ascii=False, indent=4)

    st.success("JSON file exported successfully!")
