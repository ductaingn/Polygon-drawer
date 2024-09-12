from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QStandardItem, QStandardItemModel, QImage
from PyQt5.QtCore import QUrl, QObject, QCoreApplication, QTimer
from main_app.views.layouts.main_window import Ui_MainWindow

from ..services.stream_thread import StreamThread

# from ..services.ffmpeg_thread import StreamThread

# from ..services.detect_thread import DetectThread
from ..services.canvas import Canvas
import time

import os
import json


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        # self.updateStream
        self.ui.setupUi(self)
        self.setWindowTitle("Polygon Drawer")

        self.stream_thread = StreamThread()
        # self.detect_thread = DetectThread(in_buffer=self.stream_thread.frame_queue)
        # self.detect_thread.setStreamThread(self.stream_thread)
        # self.stream_thread.updateFrame.connect(self.setImage)

        self.ui.le_link_cam.setText(
            "rtsp://admin:atin%402022@192.168.1.231/profile1/media.smp"
        )
        self.ui.btn_start_viewing.clicked.connect(self.start_stream)
        self.ui.btn_extract_polygon.clicked.connect(self.extractPoints)
        self.ui.btn_clear_polygon.clicked.connect(self.clearPoints)

        self.ui.canvas = Canvas(
            parent=self.ui.centralwidget,
            size=(self.ui.stream_window.width(), self.ui.stream_window.height()),
        )

        self.ui.canvas.setGeometry(self.ui.stream_window.geometry())
        self.ui.canvas.setStyleSheet("background-color: transparent")
        self.ui.canvas.updateConvexHull.connect(self.setConvexHull)
        self.ui.canvas.raise_()

        self.convex_hull = []
        self.points = []

    def start_stream(self):
        print("Starting...")
        if self.stream_thread.status:
            self.stream_thread.requestInterruption()
            self.stream_thread.stop()
            time.sleep(1)
            # self.stream_thread.exit()
            # self.stream_thread.wait()
            # self.stream_thread = None
            # self.ui.stream_window.clear()

            # self.stream_thread = StreamThread()
            print("Start new thread")
            # self.stream_thread.updateFrame.connect(self.setImage)
            self.stream_thread.set_link_cam(self.ui.le_link_cam.text())
            # self.stream_thread.status = True
            self.stream_thread.start()

        else:
            self.stream_thread.set_link_cam(self.ui.le_link_cam.text())
            self.stream_thread.status = True
            self.stream_thread.start()

    def stop_stream(self):
        print("Finished!")
        self.stream_thread.stop()
        self.ui.stream_window.clear()
        self.stream_thread.updateFrame.disconnect(self.setImage)
        self.stream_thread = StreamThread()
        self.stream_thread.updateFrame.connect(self.setImage)

    def setConvexHull(self, convex_hull):
        self.convex_hull = convex_hull
        print(self.convex_hull)
        self.model = QStandardItemModel()
        self.ui.lv_list_point.setModel(self.model)
        for point in convex_hull:
            item = QStandardItem(f"{point}")
            self.model.appendRow(item)

    def paintEvent(self, event):
        self.ui.canvas.setGeometry(self.ui.stream_window.geometry())
        # print(self.stream_thread.frame_queue.qsize())
        if self.stream_thread.frame_queue.qsize() > 0:
            frame = self.stream_thread.frame_queue.get()
            # w, h, ch = frame.shape
            h, w, ch = frame.shape
            frame = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.ui.stream_window.setPixmap(QPixmap.fromImage(frame))
        time.sleep(0.01)
        self.update()

    def clearPoints(self):
        print("Clear polygon")
        self.ui.canvas.clear()
        self.model.clear()

    def extractPoints(self):
        path = os.getcwd()
        out = {
            "device_id": self.stream_thread.link_cam,
            "polygon": [list(p) for p in self.convex_hull],
            "state": "ON",
        }

        out_file = open(path + "\polygon.json", "w")
        json.dump(out, out_file)
        print("Extracted file at: ", path + "\polygon.json")
        out_file.close()

    def setImage(self, image):
        self.ui.stream_window.setPixmap(QPixmap.fromImage(image))
