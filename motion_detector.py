# motion_detector.py

import cv2

class MotionDetector:
    def __init__(self, threshold=25, min_area=500):
        """
        threshold: 差分画像の二値化閾値
        min_area: 動体とみなす最小輪郭面積
        """
        self.threshold = threshold
        self.min_area = min_area
        self.prev_gray = None

    def update_params(self, threshold, min_area):
        """閾値パラメータを動的に更新"""
        self.threshold = threshold
        self.min_area = min_area

    def detect(self, frame):
        """
        frame: BGR カラー画像 (numpy.ndarray)
        戻り値: (motion: bool, vis_frame: numpy.ndarray)
        motion が True のとき動体検知。
        vis_frame はバウンディングボックスを描画したプレビュー用フレーム。
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is None:
            self.prev_gray = gray
            return False, frame

        # 差分→二値化
        diff = cv2.absdiff(self.prev_gray, gray)
        _, th = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)

        # 輪郭検出
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion = False
        vis = frame.copy()

        for cnt in contours:
            if cv2.contourArea(cnt) >= self.min_area:
                motion = True
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 0, 255), 2)

        self.prev_gray = gray
        return motion, vis

