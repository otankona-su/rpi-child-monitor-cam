# rpi-child-monitor-cam
# 👶 Child Monitor Camera with Motion Detection

Raspberry Pi とカメラモジュールを用いた、**子ども見守りカメラシステム**です。  
ローカルネットワーク上で動作し、スマホやPCからリアルタイム映像の閲覧と動作通知を受けることができます。

---

## 🤩 特徴

- 📷 **カメラ映像のストリーミング**
  - Flask + OpenCV + Picamera2 によりリアルタイム配信
- 🧠 **動体検知機能**
  - 寝転りや起き上がりを検知して通知
- 🔔 **通知システム**
  - 音と画面の枠色で即時にアラート
  - 通知音は `.mp3` をWeb UIからアップロード可能
- ⚙️ **Web UI での操作**
  - すべての設定と通知方法をブラウザ上から調整可能
  - スマホ表示にも対応したレスポンシブ設計
- ⚖️ **systemd による自動起動**
  - Raspberry Pi 起動時に自動でサーバ開始

---

## 📸 スクリーンショット

![demo](docs/demo.png)  
<!-- ※ 適当に画像を追加 -->

---

## 🚀 セットアップ方法（1行インストール）

```bash
curl -sSL https://example.com/install.sh | bash
```

> 🔧 `install.sh` のURLは実環境に合わせて変更して使用してください

---

## 📍 手動セットアップ手順

1. **依存ライブラリのインストール**

```bash
sudo apt install -y python3-flask python3-picamera2 libcamera-apps
```

2. **リポジトリをクローン**

```bash
git clone https://github.com/yourusername/child-monitor-camera.git
cd child-monitor-camera
```

3. **仮想環境の作成（任意）**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **サーバを起動**

```bash
python server.py
```

5. **ブラウザからアクセス**

```
http://raspberrypi.local:5000
```

---

## ⚙️ 設定項目（ブラウザ上で調整可能）

| 設定項目             | 説明                                               |
|----------------------|----------------------------------------------------|
| Motion Threshold     | 動体検知のしきい値（感度）                         |
| Min Contour Area     | 検出対象とする最小の物体サイズ（ノイズ除去）       |
| Reload Interval      | 設定ファイルの再読込周期（秒）               |
| 視覚通知（ON/OFF）  | 検出時に画面枠を赤く点灯                          |
| 通知色                | 枠の色（カラーピッカーで選択）               |
| 通知音アップロード    | 任意の `.mp3` ファイルをアップロード可能         |

---

## 📁 ディレクトリ構成例

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

## 🔐 セキュリティ・注意事項

- 本システムはローカルネット宜用です
- 外部からアクセスさせる場合は HTTPS や認証などの設定を行ってください

---

## 📜 ライセンス

MIT License
