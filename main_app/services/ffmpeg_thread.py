import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import cv2.data
from collections import defaultdict
import numpy as np
from queue import Queue
import ffmpeg
import subprocess


class StreamThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = False
        self.frame_queue = Queue()
        self.link_cam = ""
        self.process = None
        self.count = 0

    def set_link_cam(self, link):
        if self.link_cam != link:
            self.link_cam = link
            self.cap = cv2.VideoCapture(self.link_cam)
        self.status = True

    def run(self):
        print("Trying")
        try:
            # self.process = (
            #     ffmpeg.input(self.link_cam)
            #     .output("pipe:", format='rawvideo', pix_fmt="rgb24")
            #     .run_async(pipe_stdout=True, pipe_stderr=True)
            # )
            # self.process = subprocess.Popen(
            #     args= (
            #         "ffmpeg -r 15 -re -stream_loop -1 -f rawvideo -vcodec rawvideo -pix_fmt "
            #         f"rgb24 -s {1920}x{1080} -i {self.link_cam} pipe:0 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -b:v 8196k  ").split(),
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE,
            # )
            self.process = (
                ffmpeg
                .input(self.link_cam)
                .output("pipe:", format='rawvideo', pix_fmt='rgb24')
                .run_async(pipe_stdout=True)
            )

            while True:
                in_bytes = self.process.stdout.read(1920 * 1080 * 3)
                if not in_bytes:
                    self.stop()
                    break

                try:
                    frame_array = np.frombuffer(in_bytes, np.uint8).reshape(
                        (1920, 1080, 3)
                    )
                    if self.frame_queue.qsize() < 5:
                        self.frame_queue.put(frame_array)
                    self.msleep(1)
                except Exception as e:
                    print(f"Error processing frame: {e}")
                    break

        except Exception as e:
            print(f"Error in FFmpeg process: {e}")

    def stop(self):
        print("Disconnect!")
        self.status = False
        self.process.kill()
        self.process.wait(1)
