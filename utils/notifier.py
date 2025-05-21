# utils/notifier.py

import subprocess
import cv2

def notify_motion(frame, sound_file="/usr/share/sounds/alsa/Front_Center.wav", border_thickness=10):
    """
    動体検知時に呼び出す関数。
    - frame：OpenCV フレーム (BGR)
    - sound_file：再生する WAV ファイルパス
    - border_thickness：赤枠の太さ
    """
    # 画面を赤枠で囲む
    h, w = frame.shape[:2]
    alert_frame = frame.copy()
    cv2.rectangle(alert_frame, (0, 0), (w - 1, h - 1), (0, 0, 255), border_thickness)
    cv2.imshow("Alert", alert_frame)
    cv2.waitKey(500)
    cv2.destroyWindow("Alert")

    # 音を再生
    subprocess.Popen(["aplay", sound_file])

