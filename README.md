# rpi-child-monitor-cam
👶 Child Monitor Camera with Motion Detection
Raspberry Pi とカメラモジュールを用いた、子ども見守りカメラシステムです。
ローカルネットワーク上で動作し、スマホやPCからリアルタイム映像の閲覧と動作通知を受けることができます。

🧩 特徴
📷 カメラ映像のストリーミング

Flask + OpenCV + Picamera2 によりリアルタイム配信

🧠 動体検知機能

寝返りや起き上がりを検知して通知

🔔 通知システム

音と画面の枠色で即時にアラート

通知音は .mp3 をWeb UIからアップロード可能

🛠 Web UI での操作

すべての設定（しきい値・通知方法など）をブラウザ上から調整可能

スマホ表示にも対応したレスポンシブ設計

⚙️ systemd による自動起動

Raspberry Pi 起動時に自動でサーバ開始

📸 スクリーンショット
<!-- (必要に応じて追加) -->

🚀 セットアップ方法（1行インストール）
'''bash
curl -sSL https://example.com/install.sh | bash
※ install.sh は仮のURLです。あなたのスクリプトに差し替えてください。
'''

📝 手動セットアップ手順
依存ライブラリをインストール:

bash
コピーする
編集する
sudo apt install -y python3-flask python3-picamera2 libcamera-apps
リポジトリをクローン:

bash
コピーする
編集する
git clone https://github.com/yourusername/child-monitor-camera.git
cd child-monitor-camera
仮想環境の構築（推奨）:

bash
コピーする
編集する
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
サーバを起動:

bash
コピーする
編集する
python server.py
ブラウザでアクセス:

arduino
コピーする
編集する
http://raspberrypi.local:5000
⚙️ 設定項目（Web上で調整可能）
項目	説明
Motion Threshold	動体検知のしきい値
Min Contour Area	検出する物体の最小サイズ
Reload Interval	設定の自動再読込間隔
視覚通知	赤枠などの表示有無
通知音アップロード	任意の .mp3 ファイルを使用可能

📁 ディレクトリ構成例
arduino
コピーする
編集する
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
🔐 セキュリティ・注意事項
本システムはローカルネットワーク内のみを対象としています。

外部公開する場合は適切な認証・暗号化を実装してください。

📜 ライセンス
MIT License
