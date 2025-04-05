import streamlit as st
import pandas as pd
import os
import pandas as pd



def ImageCollection():
    st.subheader("Upload Image to Identify Ingredients")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    return f"{uploaded_file}"  # Tên file được upload
