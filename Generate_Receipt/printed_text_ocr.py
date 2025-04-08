
import cv2
import pytesseract
from PIL import Image
import pandas as pd

# (Nếu dùng Windows thì cần dòng sau)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load ảnh
image = cv2.imread('sample bill.png')

# Xử lý cơ bản: chuyển sang grayscale và threshold
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# (Tùy trường hợp, bạn có thể dùng adaptive threshold hoặc GaussianBlur)

# Chuyển ảnh sang định dạng PIL (tesseract yêu cầu)
pil_img = Image.fromarray(thresh)

# Nhận diện văn bản
text = pytesseract.image_to_string(pil_img, lang='eng')  # hoặc 'vie' nếu là tiếng Việt

print("Văn bản nhận diện được:")
# Lưu văn bản nhận diện vào file Excel

# Tách văn bản thành các dòng
lines = text.split('\n')

# Xử lý để tạo DataFrame với 2 cột: quantity và name
data = []
for line in lines:
    line = line.strip()  # Loại bỏ khoảng trắng thừa ở đầu và cuối dòng
    if line:  # Bỏ qua các dòng trống
        parts = line.split(' ', 1)  # Tách thành 2 phần: số lượng và tên
        if len(parts) == 2 and parts[0].replace('°', '').isdigit():  # Kiểm tra nếu phần đầu là số (bỏ qua ký tự đặc biệt như °)
            quantity = int(parts[0].replace('°', ''))  # Loại bỏ ký tự đặc biệt trước khi chuyển sang số
            name = parts[1]
            data.append({'Quantity': quantity, 'Name': name})

# Tạo DataFrame từ dữ liệu đã xử lý
df = pd.DataFrame(data)

# Lưu DataFrame vào file Excel
df.to_excel('output.xlsx', index=False)

