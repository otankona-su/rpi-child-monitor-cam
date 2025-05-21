# ✅ Flask アップロード + 通知色設定付き WebUI（統合版）

import os
import yaml
import cv2
import time
import logging
from flask import Flask, request, jsonify, Response, stream_with_context, render_template_string
from werkzeug.utils import secure_filename
from picamera2 import Picamera2
from motion_detector import MotionDetector
from utils.helpers import parse_resolution
from queue import Queue

# Flask 準備
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = "static/audio/uploads"
ALLOWED_EXTENSIONS = {"mp3"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename("alert_custom.mp3")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        config_path = "config.yaml"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        config["alert_sound_web"] = f"/{filepath}"
        with open(config_path, "w") as f:
            yaml.safe_dump(config, f)

        return jsonify({"status": "ok", "path": f"/{filepath}"})
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.errorhandler(500)
def handle_500(err):
    app.logger.error(f"Unhandled Exception: {err}", exc_info=True)
    return {"error": "Internal Server Error"}, 500

cfg = yaml.safe_load(open("config.yaml"))
width, height = parse_resolution(cfg["resolution"])
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"size": (width, height), "format": "RGB888"}
))
picam2.start()
md = MotionDetector(cfg["motion_threshold"], cfg["min_contour_area"])
last_reload = time.time()
event_queue = Queue()

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Child Monitor</title>
  <style>
    html, body { margin:0; padding:0; height:100%; }
    #layout { display: flex; height: 100vh; }
    #configPanel {
      width: 280px;
      background: rgba(255,255,255,0.95);
      padding: 12px;
      box-sizing: border-box;
      border-right: 1px solid #ccc;
      overflow-y: auto;
      font-family: sans-serif;
      font-size: 0.9rem;
    }
    #configPanel h4 { margin-top: 1rem; margin-bottom: 0.5rem; border-bottom: 1px solid #ccc; padding-bottom: 2px; }
    #configPanel label { display: block; margin-top: 6px; }
    #videoContainer { flex-grow: 1; position: relative; background: #000; }
    #videoContainer img {
      width: 100%; height: 100vh; object-fit: contain; display: block;
    }
    #overlay {
      position: absolute; top:0; left:0; right:0; bottom:0;
      background: rgba(0,0,0,0.7); color: #fff;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem; z-index: 1000;
    }
    #overlay button { padding: 0.8rem 1.2rem; font-size: 1rem; }

    .info {
      cursor: pointer;
      margin-left: 6px;
      font-weight: bold;
      color: #007bff;
      user-select: none;
    }
    
    .help-text {
      display: none;
      font-size: 0.8rem;
      color: #555;
      margin-bottom: 6px;
    }

  </style>
</head>
<body>
  <div id="layout">
    <div id="configPanel">
      <h4>📷 カメラと検知</h4>
      <label>
        Motion Threshold: <span id="thVal"></span>
        <span class="info" onclick="toggleHelp('desc-th')">ⓘ</span>
        <div id="desc-th" class="help-text">動きと判定するピクセルの差。大きくすると敏感度が下がります。</div>
      </label>
      <input type="range" id="motionThreshold" min="0" max="255" value="128" oninput="document.getElementById('thVal').textContent = this.value">

      <label>
        Min Contour Area: <span id="areaVal"></span>
        <span class="info" onclick="toggleHelp('desc-area')">ⓘ</span>
        <div id="desc-area" class="help-text">検出対象とみなす最小面積（ピクセル単位）。ノイズ除去に有効です。</div>
      </label>
      <input type="range" id="minArea" min="100" max="5000" step="100" value="1000" oninput="document.getElementById('areaVal').textContent = this.value">


      <label>
        Reload Interval (s): <span id="intVal"></span>
        <span class="info" onclick="toggleHelp('desc-reload')">ⓘ</span>
        <div id="desc-reload" class="help-text">設定ファイルを何秒ごとに再読み込みするか。</div>
      </label>
      <input type="number" id="reloadInt" min="1" max="60">

      <h4>👁 視覚通知設定</h4>
      <label><input type="checkbox" id="useVisualAlert" checked> 視覚通知を行う</label>
      <label>通知色: <input type="color" id="alertColor" value="#ff0000"></label>

      <h4>🔔 通知音設定</h4>
      <label><input type="checkbox" id="toggleSound" checked> 通知音を鳴らす</label>
      <label>通知音アップロード (.mp3):</label>
      <input type="file" id="audioUpload" accept=".mp3">
      <button id="uploadBtn">アップロード</button>

      <h4>⚙️ 表示設定</h4>
      <label><input type="checkbox" id="toggleVideo" checked> カメラ映像を表示</label>

      <button id="saveBtn" style="margin-top: 1rem;">保存</button>
    </div>

    <div id="videoContainer">
      <div id="overlay">
        <div>
          <p>🔔 通知を有効にするにはタップ／クリックしてください</p>
          <button id="enableBtn">Enable Notifications</button>
        </div>
      </div>
      <img id="streamView" src="{{ url_for('stream') }}">
      <audio id="alertSound" src="{{ cfg['alert_sound_web'] }}" preload="auto"></audio>
    </div>
  </div>

  <script>
    async function loadConfig() {
      const res = await fetch("/api/config");
      const cfg = await res.json();
      document.getElementById("motionThreshold").value = cfg.motion_threshold;
      document.getElementById("thVal").innerText = cfg.motion_threshold;
      document.getElementById("minArea").value = cfg.min_contour_area;
      document.getElementById("areaVal").innerText = cfg.min_contour_area;
      document.getElementById("reloadInt").value = cfg.config_reload_interval;
      document.getElementById("intVal").innerText = cfg.config_reload_interval;
      document.getElementById("alertSound").src = cfg.alert_sound_web;
    }

    function toggleHelp(id) {
      const el = document.getElementById(id);
      el.style.display = el.style.display === 'block' ? 'none' : 'block';
    }

    document.getElementById("uploadBtn").onclick = async () => {
      const fileInput = document.getElementById("audioUpload");
      if (!fileInput.files.length) return alert("ファイルを選択してください");
      const formData = new FormData();
      formData.append("file", fileInput.files[0]);
      const res = await fetch("/upload_audio", { method: "POST", body: formData });
      const result = await res.json();
      if (res.ok) {
        alert("アップロード成功");
        document.getElementById("alertSound").src = result.path;
      } else {
        alert("アップロード失敗: " + result.error);
      }
    };

    document.getElementById("enableBtn").onclick = () => {
      const audio = document.getElementById("alertSound");
      audio.muted = false;
      audio.play().catch(()=>{});
      document.getElementById("overlay").style.display = "none";

      const evtSource = new EventSource("/events");
      evtSource.onmessage = (e) => {
        if (e.data === "motion") {
          const useVisual = document.getElementById("useVisualAlert").checked;
          const color = document.getElementById("alertColor").value;
          if (useVisual) {
            document.body.style.border = `10px solid ${color}`;
            setTimeout(() => document.body.style.border = "", 500);
          }
          if (!audio.muted) audio.play().catch(() => {});
        }
      };
    };

    document.getElementById("saveBtn").onclick = async () => {
      const base = await fetch("/api/config").then(r => r.json());
      const newCfg = {
        ...base,
        motion_threshold: parseInt(document.getElementById("motionThreshold").value),
        min_contour_area: parseInt(document.getElementById("minArea").value),
        config_reload_interval: parseInt(document.getElementById("reloadInt").value)
      };
      await fetch("/api/config", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(newCfg)
      });
      alert("保存しました");
    };


    document.getElementById("toggleSound").onchange = (e) => {
      document.getElementById("alertSound").muted = !e.target.checked;
    };

    document.getElementById("toggleVideo").onchange = (e) => {
      document.getElementById("streamView").src = e.target.checked ? "/stream" : "";
    };

    document.addEventListener("DOMContentLoaded", loadConfig);
  </script>
</body>
</html>
"""

# 以下、ルーティング等は前回と同様に維持
@app.route('/')
def index():
    return render_template_string(HTML, cfg=cfg)

@app.route('/stream')
def stream():
    return Response(stream_with_context(gen_frames()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/events')
def events():
    def generate():
        while True:
            msg = event_queue.get()
            yield f"data: {msg}\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/config', methods=['GET'])
def get_config():
    try:
        cfg = yaml.safe_load(open("config.yaml"))
        return cfg, 200
    except Exception as e:
        return {"error": "Cannot load config"}, 500

@app.route('/api/config', methods=['POST'])
def update_config():
    try:
        new_cfg = request.json
        for key in ["motion_threshold", "min_contour_area", "config_reload_interval"]:
            if key not in new_cfg:
                return {"error": f"{key} missing"}, 400
        with open("config.yaml", "w") as f:
            yaml.safe_dump(new_cfg, f)
        md.update_params(new_cfg["motion_threshold"], new_cfg["min_contour_area"])
        return {"status": "ok"}, 200
    except Exception as e:
        return {"error": "Cannot update config"}, 500

def gen_frames():
    global cfg, last_reload
    while True:
        if time.time() - last_reload > cfg["config_reload_interval"]:
            try:
                cfg = yaml.safe_load(open("config.yaml"))
                md.update_params(cfg["motion_threshold"], cfg["min_contour_area"])
                last_reload = time.time()
            except Exception as e:
                continue
        try:
            rgb = picam2.capture_array()
            frame = rgb[:, :, ::-1]
            motion, vis = md.detect(frame)
            if motion:
                event_queue.put("motion")
            ret, jpeg = cv2.imencode('.jpg', vis)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        except Exception:
            time.sleep(1)
            continue

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

