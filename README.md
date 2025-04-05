
# **HACKATHON 2025**  
**Đề tài:** .  

---

## **Introduction**  
Đây là project nhằm vận dụng các kiến thức đã học vào thực tế thông qua việc xây dựng một website bán hàng.  
- Mục tiêu: Giúp sinh viên nắm vững kiến thức về Java Web, từ đó nâng cao khả năng phát triển ứng dụng thực tế.  
- Công nghệ được sử dụng:
   - **Backend:** Servlet, JSP/JSTL, JPA  
   - **Frontend:** Bootstrap  
   - **Bảo mật:** HTTPS, TLS, JWT  
   - **Database:** SQLServer, MySQL, PostgreSQL  
   - **Khác:** OAuth, Sitemesh Decorator  

---

## **Features**  
- **Tính năng 1:** Website bán hàng các loại thực phẩm sạch với các chức năng cơ bản:  
   - Xem sản phẩm  
   - Tìm kiếm sản phẩm  
   - Thêm vào giỏ hàng và thanh toán
   - Trang quản trị của admin  

- **Tính năng 2:** Đăng nhập và xác thực OAuth với **Google** và **Facebook**.  

- **Tính năng 3:** Bảo mật hệ thống với:  
   - **HTTPS** và **TLS**  
   - File cấu hình bảo mật: `Keystore.jks` và `.env`  
   - Bộ lọc bảo mật **Filter** trong Servlet  

- **Tính năng 4:** Tích hợp cơ sở dữ liệu **Cloud Database** để lưu trữ và truy xuất dữ liệu.  

---

## **How To Setup**  

### **Yêu Cầu Hệ Thống**  
- **IDE Java:** Spring Tool Suite 4, Eclipse  
- **Cơ sở dữ liệu:** SQLServer, MySQL hoặc PostgreSQL  
- **Server:** Apache Tomcat 10.1.24 (khuyến khích)  
- **Thư viện:** Apache Maven 3.9.9 (khuyến khích)  
- **Java Development Kit (JDK):** JDK 22 (khuyến khích)  

---

### **Steps**  

1. **Clone Project**  
   ```bash
   git clone https://github.com/duyhao76/HKT_Shop
   ```

2. **Thêm File Cấu Hình Bảo Mật**  
   - Thêm file `Client_Secret.env` vào thư mục `src/main/resource/`.
   - Thêm file`keystore.jks` vào thư mục chứa Project.  

3. **Cấu Hình Server**  
   - Mở file `server.xml` trong Apache Tomcat.  
   - Tìm đến dòng 64 và thay thế đoạn `<Connector>...</Connector>` như sau:  

   ```xml
   <Connector connectionTimeout="20000" maxParameterCount="1000" port="8080" protocol="HTTP/1.1" redirectPort="8443"/>
   <Connector SSLEnabled="true" maxThreads="150" port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol" scheme="https" secure="true">
       <SSLHostConfig protocols="+TLSv1.2,+TLSv1.3">
           <Certificate certificateKeystoreFile="...\keystore.jks" certificateKeystorePassword="123456" type="RSA"/>
       </SSLHostConfig>
   </Connector>
   ```

   - Thay đường dẫn `"certificateKeystoreFile="...\keystore.jks"` bằng đường dẫn thực tế tới file `keystore.jks`.  

4. **Cập Nhật Maven và Restart Server**  
   - Update Maven Project.  
   - Restart Apache Tomcat.  

---

## **Cách Sử Dụng**  
1. Chạy server trên Apache Tomcat.  
2. Truy cập vào đường dẫn:  
   ```plaintext
   https://localhost:8443/HKT_Shop/
   ```

---

## **Cấu Trúc Thư Mục**  

```bash
HKT_Shop/
│
├── src/                      # Mã nguồn chính
│   ├── main/  
│   │   ├── java/             # Code backend
│   │   │   └── vn/HKT/
│   │   │       ├── configs/          # Cấu hình ứng dụng
│   │   │       ├── controllers/      # Controller xử lý logic
│   │   │       ├── daos/             # Lớp truy cập dữ liệu
│   │   │       ├── dtos/             # Đối tượng truyền dữ liệu
│   │   │       ├── entities/         # Entity ánh xạ cơ sở dữ liệu
│   │   │       ├── services/         # Lớp dịch vụ xử lý logic nghiệp vụ
│   │   │       ├── filters/          # Bộ lọc bảo mật
│   │   │       └── utils/            # Các hàm tiện ích
│   │   ├── resources/        # File cấu hình (META-INF, .env)
│   │   │   └── META-INF/             # File cấu hình JPA
│   │   └── webapp/           # Giao diện và cấu hình frontend
│   │       ├── commons/             # Tài nguyên dùng chung (HTML, CSS)
│   │       ├── WEB-INF/             # Cấu hình Sitemesh Decorator
│   │       ├── views/               # Các file JSP giao diện
│   │       └── assets/              # CSS, JS, Images
│   └── test/                 # Các file kiểm thử
│
├── docs/                     # Tài liệu hướng dẫn
├── pom.xml                   # File cấu hình Maven
├── README.md                 # File mô tả dự án
├── keystore.jks              # Chứng chỉ TSL 
└── .gitignore                # File bỏ qua khi commit lên GitHub
```
---

## **Thông Tin Nhóm**  
- **Thành viên:**  
   1. Đăng Cửu Dương  
   2. Trịnh Hửu Thọ
   3. Phan Văn Quân
   4. Hoàng Mạnh Tường 
---

## **Liên Hệ**  
- **Email:** trinhuutho@gmail.com  
- **GitHub:** [https://github.com/username](https://github.com/TrinhHuuTho)  

---

### **Ghi Chú**  
Các tài nguyên như **keystore.jks** và **.env** cần được tạo trước khi chạy ứng dụng để đảm bảo bảo mật.  
