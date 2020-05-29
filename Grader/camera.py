#  Copyright (c) 2020. Anish Govind
#  https://github.com/anishg24

import cv2

from api.python_scripts.scanner import Scanner


class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        # self.isOpen = self.cap.isOpened()
        self.scanner = Scanner()

    def __del__(self):
        self.cap.release()

    def get_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            original, warped, processed, score = self.scanner.process_frame(frame)
            ret, jpeg = cv2.imencode('.jpg', warped)
            return jpeg.tobytes(), processed, score
        else:
            return None
