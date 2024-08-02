import os
import sys
import time

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import cv2.data
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
from queue import Queue

from .stream_thread import StreamThread


class DetectThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, in_buffer:Queue, parent=None):
        QThread.__init__(self, parent)
        self.status = False
        self.model = YOLO('yolov8n.pt')
        self.stream_thread:StreamThread = None
        self.in_buffer = in_buffer

    def setStreamThread(self, stream_thread:StreamThread):
        self.stream_thread = stream_thread
        self.stream_thread.updateFrame.connect(self.inference)

    def qimage_to_numpy(self, qimage: QImage) -> np.ndarray:
        # Ensure the QImage is in the format you need
        if qimage.format() != QImage.Format_RGB888:
            qimage = qimage.convertToFormat(QImage.Format_RGB888)
        
        # Get raw data from QImage
        width = qimage.width()
        height = qimage.height()
        stride = qimage.bytesPerLine()
        
        # Create a NumPy array from raw data
        ptr = qimage.bits()
        # ptr.setsize(height * stride)
        array = np.array(ptr).reshape(height, stride // 3, 3)  # Assuming 3 channels (RGB)
        
        return array
    
    def inference(self, image):
        # frame = self.qimage_to_numpy(image)

        results = self.model(frame)

        for result in results:
            for bb in result.boxes:
                x1,y1,x2,y2 = map(int, bb.xyxy[0])
                conf = bb.conf[0].item()
                cls_id = int(bb.cls[0].item())
                label = f'{self.model.names[cls_id]} {conf}'
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 4)
                cv2.putText(frame, label, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 4)

        h, w, ch = frame.shape
        print(h,w)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        annotated_frame = QImage(frame.data, w, h, ch*w, QImage.Format_RGB888)
        scaled_img = annotated_frame.scaled(1920, 1080, Qt.KeepAspectRatio)
        self.updateFrame.emit(scaled_img)


    def run(self):
        print('Trying')
        # self.cap = cv2.VideoCapture(self.link_cam)
        self.status = True
        # self.set_link_cam
        while self.status:
            try:
                if len(self.in_buffer) == 0:
                    continue

                frame = self.in_buffer.get()
                # results = self.model(frame)

                # for result in results:
                #     for bb in result.boxes:
                #         x1,y1,x2,y2 = map(int, bb.xyxy[0])
                #         conf = bb.conf[0].item()
                #         cls_id = int(bb.cls[0].item())
                #         label = f'{self.model.names[cls_id]} {conf}'
                #         cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 4)
                #         cv2.putText(frame, label, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 4)

                # h, w, ch = frame.shape
                # print(h,w)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # annotated_frame = QImage(frame.data, w, h, ch*w, QImage.Format_RGB888)
                # scaled_img = annotated_frame.scaled(1920, 1080, Qt.KeepAspectRatio)
                # self.updateFrame.emit(scaled_img)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                # frame = QImage(frame.data, w, h, ch*w, QImage.Format_RGB888)
                # self.updateFrame.emit(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                self.msleep(1)
                
            except Exception as e:
                print(e)
        # sys.exit(-1)

    def stop(self):
        print('Disconnect!')
        self.status = False
        self.cap.release()
        self.cap = None