# Sử dụng image Python chính thức
FROM python:3.8-slim

# Cài đặt nano, dos2unix và các gói phụ thuộc
RUN apt-get update && apt-get install -y nano libc-bin dos2unix

# Thiết lập thư mục làm việc
WORKDIR /usr/src/app

# Sao chép file yêu cầu của ứng dụng (requirements.txt) vào container
COPY requirements.txt ./

# Cài đặt các thư viện yêu cầu
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Thiết lập command mặc định khi chạy container
# CMD ["python", "consumer.py"]



# Sao chép file startup.sh vào container
COPY startup.sh /root/startup.sh

# Chuyển đổi line endings của file startup.sh từ Windows-style sang Unix-style
RUN dos2unix /root/startup.sh

# Thiết lập command mặc định khi chạy container
CMD ["/bin/bash", "/root/startup.sh"]