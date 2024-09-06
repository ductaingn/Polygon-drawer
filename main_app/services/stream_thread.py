import os
import sys
import time

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import cv2.data
# from ultralytics import YOLO
from collections import defaultdict
import numpy as np
from queue import Queue


class StreamThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = False
        self.frame_queue = Queue()
        self.link_cam = ''

    def set_link_cam(self, link):
        if self.link_cam != link:
            self.link_cam = link
            try:
                self.cap = cv2.VideoCapture(self.link_cam)
            except Exception as e:
                print(f'An error has occured with cv2.VideoCapture with link: {self.link_cam}')
                print(e)
                return
        self.status = True


    def run(self):
        print('Trying')
        while self.status:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("not ret")
                    continue

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.frame_queue.qsize() < 5:
                    self.frame_queue.put(frame)
                self.msleep(1)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
            except Exception as e:
                print(e)

    def stop(self):
        print('Disconnect!')
        self.status = False
        