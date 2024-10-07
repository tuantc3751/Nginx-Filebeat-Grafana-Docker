# Sử dụng image Nginx dựa trên Alpine làm cơ sở
FROM nginx:alpine

# Cài đặt các gói cần thiết để tải và cài đặt Packetbeat
RUN apk add --no-cache curl bash libc6-compat

# Tải xuống và cài đặt Packetbeat phiên bản 8.5.3
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-8.5.3-linux-x86_64.tar.gz \
    && tar -xzf packetbeat-8.5.3-linux-x86_64.tar.gz \
    && mv packetbeat-8.5.3-linux-x86_64 /usr/share/packetbeat \
    && rm packetbeat-8.5.3-linux-x86_64.tar.gz

# Thêm cấu hình Packetbeat
COPY packetbeat.yml /usr/share/packetbeat/packetbeat.yml

# Thêm file index.html vào thư mục chứa file của Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY assets/ /usr/share/nginx/html/assets/

# Mở cổng cho Nginx
EXPOSE 80

# Khởi động Nginx và Packetbeat khi container chạyCMD nginx && /usr/share/packetbeat/packetbeat -e -c /usr/share/packetbeat/packetbeat.yml
