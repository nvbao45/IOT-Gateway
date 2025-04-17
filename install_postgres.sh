#!/bin/bash

# Load environment variables from .env file
if [[ -f .env ]]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ File .env không tồn tại."
    exit 1
fi

# Define PostgreSQL version
PG_VERSION=15  # Thay đổi phiên bản nếu cần

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ Không thể xác định hệ điều hành."
    exit 1
fi

echo "🔍 Phát hiện hệ điều hành: $OS"

# Install PostgreSQL based on OS
if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
    echo "🔄 Cài đặt PostgreSQL trên Ubuntu/Debian..."
    
    # Update system packages
    sudo apt update -y
    sudo apt install -y postgresql postgresql-contrib

elif [[ "$OS" == "centos" || "$OS" == "rhel" ]]; then
    echo "🔄 Cài đặt PostgreSQL trên CentOS/RHEL..."

    # Enable PostgreSQL repo
    sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %rhel)-x86_64/pgdg-redhat-repo-latest.noarch.rpm
    sudo yum install -y postgresql$PG_VERSION-server postgresql$PG_VERSION

    # Initialize database
    sudo /usr/pgsql-$PG_VERSION/bin/postgresql-$PG_VERSION-setup initdb

    # Enable and start service
    sudo systemctl enable postgresql-$PG_VERSION
    sudo systemctl start postgresql-$PG_VERSION

else
    echo "❌ Hệ điều hành không được hỗ trợ!"
    exit 1
fi

# Start and enable PostgreSQL
echo "🚀 Khởi động PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Create default user and database using .env variables
echo "🔧 Tạo user và database từ file .env..."
sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USERNAME WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USERNAME;
ALTER DATABASE $DB_NAME OWNER TO $DB_USERNAME;
EOF

echo "✅ PostgreSQL đã được cài đặt thành công!"
