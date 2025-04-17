#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    source .env
else
    echo "Error: .env file not found!"
    exit 1
fi

# Validate required variables
if [[ -z "$DB_USERNAME" || -z "$DB_PASSWORD" || -z "$DB_HOST" || -z "$DB_PORT" || -z "$DB_NAME" ]]; then
    echo "Error: Missing required environment variables in .env!"
    exit 1
fi

# Update system
echo "Updating system..."
sudo apt update -y

# Install MariaDB Server
echo "Installing MariaDB Server..."
sudo apt install -y mariadb-server

# Start MariaDB Service
echo "Starting MariaDB service..."
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure MariaDB Installation (Optional: Uncomment if needed)
# echo "Securing MariaDB installation..."
# sudo mysql_secure_installation

# Configure MariaDB for remote access
echo "Updating MariaDB configuration..."
sudo sed -i "s/^bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mariadb.conf.d/50-server.cnf

# Restart MariaDB to apply changes
sudo systemctl restart mariadb

# Create MariaDB User & Database with Remote Access
echo "Creating MariaDB database and user..."
sudo mariadb -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
sudo mariadb -e "CREATE USER IF NOT EXISTS '$DB_USERNAME'@'%' IDENTIFIED BY '$DB_PASSWORD';"
sudo mariadb -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USERNAME'@'%';"
sudo mariadb -e "FLUSH PRIVILEGES;"

# Open MariaDB port in firewall
echo "Opening MariaDB port $DB_PORT in firewall..."
sudo ufw allow $DB_PORT/tcp
sudo ufw reload

echo "MariaDB setup is complete!"
echo "You can now connect remotely using:"
echo "mysql -u $DB_USERNAME -p -h 0.0.0.0 -P $DB_PORT -D $DB_NAME"
