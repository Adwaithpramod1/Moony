#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[+] Installing Python..."
pkg install python -y

echo "[+] Installing required dependencies..."
pip install --upgrade pip

pip install \
requests \
beautifulsoup4 \
dnspython \
python-whois \
colorama \
geoip2 \
lxml

echo ""
echo "[✔] Installation Complete!"
echo "[+] Run the tool using:"
echo "python moony.py"
