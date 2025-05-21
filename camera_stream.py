# camera_stream.py
from picamera2 import Picamera2
import cv2
import yaml
import time
from motion_detector import MotionDetector
from utils.helpers import parse_resolution

def load_config(path="config.yaml"):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise RuntimeError(f"Failed to load config: {path} is empty or malformed")
    return cfg

def main():
    # 設定読み込み
    try:
        cfg = load_config()
    except Exception as e:
        print(f"[ERROR] failed to load config: {e}")
        return

    width, height = parse_resolution(cfg["resolution"])
    fps            = cfg["framerate"]
    preview        = cfg["preview_window"]
    reload_iv      = cfg["config_reload_interval"]

    # Picamera2 初期化（例外キャッチ）
    try:
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        picam2.configure(preview_config)
        picam2.start()
    except Exception as e:
        print(f"[ERROR] Failed to initialize Picamera2: {e}")
        return

    # 動体検知器初期化
    md = MotionDetector(
        threshold=cfg["motion_threshold"],
        min_area=cfg["min_contour_area"]
    )

    last_reload = time.time()

    try:
        while True:
            # 設定ファイル自動リロード
            if time.time() - last_reload > reload_iv:
                try:
                    cfg = load_config()
                    md.update_params(cfg["motion_threshold"], cfg["min_contour_area"])
                    last_reload = time.time()
                except Exception as e:
                    print(f"[WARN] failed to reload config: {e}")

            # フレーム取得（失敗時はログしてリトライ）
            try:
                rgb = picam2.capture_array()
                if rgb is None:
                    raise RuntimeError("capture_array returned None")
                frame = rgb[:, :, ::-1]  # RGB→BGR
            except Exception as e:
                print(f"[WARN] failed to capture frame: {e}. retrying...")
                time.sleep(1)
                continue

            # 動体検知
            try:
                motion, vis_frame = md.detect(frame)
            except Exception as e:
                print(f"[ERROR] motion detection failed: {e}")
                continue

            # プレビュー表示
            if preview:
                cv2.imshow("Preview", vis_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # 通知
            if motion:
                print("Motion detected!")
                from utils.notifier import notify_motion
                notify_motion(
                    vis_frame,
                    sound_file=cfg.get("alert_sound", "/usr/share/sounds/alsa/Front_Center.wav"),
                    border_thickness=cfg.get("alert_border", 10)
                )
    finally:
        # クリーンアップ
        try:
            picam2.stop()
        except Exception as e:
            print(f"[WARN] Error stopping Picamera2: {e}")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

