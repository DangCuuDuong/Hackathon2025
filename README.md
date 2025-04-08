# 🧊 Fridgey – Trợ lý nhà bếp thông minh  

**Repo**: Hackathon2025 - HCMUTE
**Team**: Dare To Take Quest  

---

## 🎯 Mục tiêu dự án  

Fridgey là một trợ lý nhà bếp thông minh, giúp người dùng – đặc biệt là sinh viên, dân văn phòng và người bận rộn – quản lý nguyên liệu trong tủ lạnh và gợi ý thực đơn phù hợp.  

Trong thực tế, nhiều bạn sinh viên nhận thực phẩm từ gia đình nhưng lại không biết nấu gì và nấu như thế nào. Fridgey ra đời để giải quyết vấn đề đó: giúp người dùng tiết kiệm thời gian suy nghĩ, nấu nướng nhanh chóng và khoa học hơn.  

---

## ✨ Tính năng chính  

- 🧾 **Quản lý nguyên liệu trong tủ lạnh**  
   - Nhập tay  
   - Quét ảnh nguyên liệu  
   - *(Đang phát triển)* Quét hóa đơn mua hàng  

- 🍱 **Gợi ý thực đơn**  
   - Dựa trên nguyên liệu có sẵn  
   - Dựa trên sở thích, tình trạng sức khỏe  

- 🛒 **Gợi ý danh sách thực phẩm cần mua thêm**  

- 📆 **Kế hoạch ăn uống cho 3–5 ngày tới**  

- 🍳 **Cách nấu chi tiết từng món**  

---

## 🛠 Công nghệ sử dụng  

- **Ngôn ngữ**: `Python`, `HTML`, `CSS`  
- **Thư viện & Framework**:  
   - `Streamlit`  
   - `OpenAI API`  
   - Các model `Machine Learning / Deep Learning` tự huấn luyện  

---

## 🚀 Hướng dẫn cài đặt & chạy

```bash
# 1. Clone repository
git clone https://github.com/yourusername/Hackathon2025.git
cd Hackathon2025

# 2. Tạo virtual environment (nếu muốn)
python -m venv venv
source venv/bin/activate  # hoặc .\venv\Scripts\activate trên Windows

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Tạo file ".env" và thêm vào dòng sau:
OPENAI_API_KEY = "your api key"

# 5. Chạy ứng dụng
streamlit run main.py
```

💡 **Lưu ý**: Tên file chạy chính (như `app.py`) có thể thay đổi tuỳ theo cấu trúc repo của bạn.  

### ⚙️ Yêu cầu hệ thống  

- Python >= 3.11  
- Internet để gọi OpenAI API (nếu sử dụng)  

---

## 👨‍👩‍👧‍👦 Thành viên nhóm  

| **Họ tên**       | **Vai trò**  |  
|-------------------|--------------|  
| Dương             | Backend      |  
| Trịnh Hửu Thọ     | Backend      |  
| Tường             | Frontend     |  
| Quân              | Frontend     |  

---

## 🧪 Trạng thái chức năng  

| **Tính năng**                                | **Trạng thái**         |  
|----------------------------------------------|-------------------------|  
| Gợi ý thực đơn                               | ✅ Hoàn thành           |  
| Kế hoạch ăn uống 3 ngày tới                  | ✅ Hoàn thành           |  
| Quản lý nguyên liệu (nhập tay, quét ảnh)     | ✅ Hoàn thành           |  
| Chi tiết cách nấu món ăn                     | ✅ Hoàn thành           |  
| Gợi ý đi chợ                                 | ✅ Hoàn thành           |  
| Quản lý nguyên liệu bằng hóa đơn            | 🔄 Đang phát triển      |  
| Tinh chỉnh lượng nguyên liệu khi nấu        | 🔜 Dự kiến phát triển   |  
| Hướng dẫn nấu bằng âm thanh/video           | 🔜 Dự kiến phát triển   |  
| Tối ưu hoá gợi ý bằng database công thức riêng | 🔜 Dự kiến phát triển   |  
| Công thức có ảnh minh hoạ                   | 🔜 Dự kiến phát triển   |  

---

## 🏁 Hướng phát triển tương lai  

- Hướng dẫn nấu ăn bằng âm thanh/video trực quan  
- Điều chỉnh linh hoạt lượng nguyên liệu khi nấu  
- Tích hợp database công thức nấu ăn riêng, cải thiện khả năng gợi ý  
- Minh hoạ từng công thức bằng hình ảnh hấp dẫn  

---

## 📸 Ảnh Demo  

*(Sẽ được cập nhật sau khi hoàn thiện UI/UX và chức năng chính)*  

📍 **Placeholder ảnh**:  

---

## 💬 Liên hệ  

Nếu bạn có câu hỏi hoặc muốn đóng góp, đừng ngần ngại tạo Issue hoặc PR cho repo!  

Made with ❤️ by Dare To Take Quest – Hackathon 2025  