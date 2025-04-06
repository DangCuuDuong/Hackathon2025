from PIL import Image
import streamlit as st
import tempfile

def ImageCollection():
    st.subheader("Upload Image to Identify Ingredients")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="📷 Uploaded Image", use_column_width=True)

            # ✅ Lưu ảnh tạm vào file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            img.save(temp_file.name)
            return temp_file.name  # ✅ Trả về đường dẫn ảnh
        except Exception as e:
            st.error(f"❌ Không thể xử lý ảnh: {e}")
    return None
