#!/bin/bash
set -e

echo "install nessesary packages ..."
sudo apt update
sudo apt upgrade -y
sudo apt install  -y git python3-picamera2

echo "📁 プロジェクトを ~/monitoring_project にクローン..."
cd ~
if [ ! -d monitoring_project ]; then
  git clone https://github.com/otankona-su/rpi-child-monitor-cam.git monitoring_project
else
  echo "⚠️ monitoring_project ディレクトリはすでに存在します。"
fi

cd monitoring_project

# 以下、前回のインストール手順と同じ -----------------------

echo "🐍 仮想環境作成とパッケージインストール..."
python3 -m --system-site-packages venv monitoring
source monitoring/bin/activate
pip install --upgrade pip
pip install flask opencv-python-headless pyyaml

# config.yaml 初期化（必要なら）
if [ ! -f config.yaml ]; then
  cat <<EOF > config.yaml
camera_index: 0
resolution: "640x480"
framerate: 30
preview_window: false
motion_threshold: 25
min_contour_area: 500
config_reload_interval: 5
alert_sound: "/usr/share/sounds/alsa/Front_Center.wav"
alert_border: 10
EOF
fi

echo "⚙️ systemd 登録..."
sudo tee /etc/systemd/system/monitoring.service > /dev/null <<EOL
[Unit]
Description=Child Monitor Flask
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/monitoring_project
ExecStart=/home/pi/monitoring_project/monitoring/bin/python server.py
Restart=always
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable monitoring
sudo systemctl start monitoring

echo "✅ セットアップ完了！ http://raspberrypi.local:5000 にアクセスしてください。"

