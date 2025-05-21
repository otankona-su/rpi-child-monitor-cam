# rpi-child-monitor-cam
# 👶 Child Monitor Camera with Motion Detection
A home baby monitor system built with Raspberry Pi and a camera module.
Runs on a local network and streams real-time video to smartphones and PCs, with motion-based alerts.

Raspberry Pi とカメラモジュールを用いた、**子ども見守りカメラシステム**です。
ローカルネットワーク上で動作し、スマホやPCからリアルタイム映像の閲覧と動作通知を受けることができます。  


---

## 🤩 Features / 特徴

- 📷 ** Video Streaming / カメラ映像のストリーミング **
  - Real-time streaming using Flask, OpenCV, and Picamera2.
  - Flask + OpenCV + Picamera2 によりリアルタイム配信  

- 🧠 **Motion Detection / 動体検知機能**
  - Detects movement such as rolling or waking.
  - 寝転りや起き上がりを検知して通知  
    
- 🔔 **Notification System** / 通知システム
  - Alerts with sound and visual border changes.
  - Supports uploading `.mp3` alert sounds via the web UI.
  - 音と画面の枠色で即時にアラート  
  - 通知音は `.mp3` をWeb UIからアップロード可能  
    

- Web-Based Configuration / ⚙️ **Web UI での操作**
  - All parameters adjustable from a browser.
  - Responsive UI for smartphone compatibility.
  - すべての設定と通知方法をブラウザ上から調整可能
  - スマホ表示にも対応したレスポンシブ設計  
    

- ⚖️ **systemd Autostart / systemd による自動起動**
  - Server starts automatically on boot.
  - Raspberry Pi 起動時に自動でサーバ開始
    
---

## 📸 スクリーンショット / Screenshot

![demo](docs/demo.png)  
<!-- ※ 適当に画像を追加 / Replace with your own image -->

---

## 🚀 Quick Install / セットアップ方法（1行インストール）

```bash
curl -sSL https://raw.githubusercontent.com/otankona-su/rpi-child-monitor-cam/refs/heads/main/install.sh | bash
```
> Replace the URL with your actual install script path
> 🔧 `install.sh` のURLは実環境に合わせて変更してください  

---

## 📍 Manual Installation / 手動セットアップ手順

1. **Install dependencies / 依存ライブラリのインストール**

```bash
sudo apt install -y python3-flask python3-picamera2 libcamera-apps
```

2. **Clone the repository** / リポジトリをクローン

```bash
git clone https://github.com/otankona-su/rpi-child-monitor-cam.git
cd child-monitor-camera
```

3. **(Optional) Create virtualenv / 仮想環境の作成（任意）**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Start the server / サーバを起動**

```bash
python server.py
```

5. **Access via browser / ブラウザからアクセス**

```
http://raspberrypi.local:5000
```

---

## ⚙️ Configurable Parameters via Web UI / 設定項目（ブラウザで調整可能）

| 項目 / Parameter         | 説明 / Description                                 |
|--------------------------|--------------------------------------------------|
| Motion Threshold         | Sensitivity threshold for motion detection / 動体検知のしきい値（感度） |
| Min Contour Area         | Minimum area to detect an object / ノイズ除去のための最小面積     |
| Reload Interval (sec)    | Auto reload interval for settings / 設定の再読込間隔       |
| 視覚通知（ON/OFF）       | Visual alert with screen border / 枠表示による通知         |
| Alert Color / 通知色     | Color of the alert border / アラート表示色               |
| 通知音アップロード       | `.mp3` Upload custom alert sound / アップロード            |

---

## 📁 Project Structure / ディレクトリ構成例

```
project/
├── server.py
├── config.yaml
├── static/
│   └── audio/
├── templates/
├── utils/
│   ├── helpers.py
│   └── motion_detector.py
└── README.md
```

---

## 🔐 Security Notes / セキュリティ・注意事項
- This system is intended for local network use.
- If exposing to the internet, implement HTTPS and authentication.
- 本システムはローカルネット用です
- 外部公開時は HTTPS やパスワード保護を適用してください  


---

## 📜 License / ライセンス

MIT License
