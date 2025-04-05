import json
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
    st.markdown("<div class='one1'>Add Ingredients</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 1]) 

    with col1:
        name = st.text_input("Ingredient name (e.g., Salt)")
    with col2:
        count = st.number_input("Count", min_value=1, value=1, step=1)
    with col3:
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
    if not componets_prepare.empty:
        st.markdown("<div class='one1'>Components Prepare</div>", unsafe_allow_html=True)
        tempshow = componets_prepare.rename(columns={"name": "Food Name", "count": "Kg"})
        st.dataframe(tempshow.reset_index(drop=True), use_container_width=True)

    


    # Export button
    if st.button("Merge Ingredients"):
        with open("JSON_FILE/main.json", "r") as f:
            json_data = json.load(f)

        for index, row in componets_prepare.iterrows():
            name = str(row["name"])
            count = int(row["count"])
            if name in json_data:
                json_data[name] += count
            else:
                json_data[name] = count

        with open("data.json", "w") as f:
            json.dump(json_data, f, indent=4)

        st.success("Merged successfully!")


def output_json(df):
    summary = df.groupby("name")["count"].sum().to_dict()

    with open("ingredients.json", "w", encoding='utf-8') as f:
        import json
        json.dump(summary, f, ensure_ascii=False, indent=4)

    st.success("JSON file exported successfully!")
