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

## 🚀 セットアップ方法（1行インストール） / Quick Install

```bash
curl -sSL https://raw.githubusercontent.com/otankona-su/rpi-child-monitor-cam/refs/heads/main/install.sh | bash
```

> 🔧 `install.sh` のURLは実環境に合わせて変更してください  
> Replace the URL with your actual install script path

---

## 📍 手動セットアップ手順 / Manual Installation

1. **依存ライブラリのインストール / Install dependencies**

```bash
sudo apt install -y python3-flask python3-picamera2 libcamera-apps
```

2. **リポジトリをクローン / Clone the repository**

```bash
git clone https://github.com/otankona-su/rpi-child-monitor-cam.git
cd child-monitor-camera
```

3. **仮想環境の作成（任意） / (Optional) Create virtualenv**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **サーバを起動 / Start the server**

```bash
python server.py
```

5. **ブラウザからアクセス / Access via browser**

```
http://raspberrypi.local:5000
```

---

## ⚙️ 設定項目（ブラウザで調整可能） / Configurable Parameters via Web UI

| 項目 / Parameter         | 説明 / Description                                 |
|--------------------------|--------------------------------------------------|
| Motion Threshold         | 動体検知のしきい値（感度） / Sensitivity threshold for motion detection |
| Min Contour Area         | ノイズ除去のための最小面積 / Minimum area to detect an object     |
| Reload Interval (sec)    | 設定の再読込間隔 / Auto reload interval for settings       |
| 視覚通知（ON/OFF）       | 枠表示による通知 / Visual alert with screen border         |
| 通知色 / Alert Color     | アラート表示色 / Color of the alert border               |
| 通知音アップロード       | `.mp3` アップロード / Upload custom alert sound            |

---

## 📁 ディレクトリ構成例 / Project Structure

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

## 🔐 セキュリティ・注意事項 / Security Notes

- 本システムはローカルネット用です  
  This system is intended for local network use.
- 外部公開時は HTTPS やパスワード保護を適用してください  
  If exposing to the internet, implement HTTPS and authentication.

---

## 📜 ライセンス / License

MIT License


---

## 📜 ライセンス

MIT License
