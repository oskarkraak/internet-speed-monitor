#!/bin/bash

# Update and install required packages
sudo apt update
sudo apt install -y python3 python3-pip sqlite3 nginx git
sudo pip3 install speedtest-cli flask

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the path to the Python3 binary dynamically
PYTHON_PATH=$(which python3)

# Create SQLite database and table
sqlite3 "$SCRIPT_DIR/data.db" <<EOF
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    download_mbps REAL,
    upload_mbps REAL,
    ping_ms REAL
);
EOF

# Make run_speedtest.py executable
chmod +x "$SCRIPT_DIR/run_speedtest.py"

# Add run_speedtest.py to crontab to run every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * $PYTHON_PATH $SCRIPT_DIR/run_speedtest.py") | crontab -

# Create a systemd service file for the Flask app
SERVICE_FILE="/etc/systemd/system/internet-speed-monitor.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Internet Speed Monitor Web App
After=network.target

[Service]
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=$PYTHON_PATH $SCRIPT_DIR/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable internet-speed-monitor.service
sudo systemctl start internet-speed-monitor.service
