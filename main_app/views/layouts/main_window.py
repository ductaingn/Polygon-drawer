# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\ATIN\Polygon\resources\uis\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(465, 332)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.le_link_cam = QtWidgets.QLineEdit(self.centralwidget)
        self.le_link_cam.setObjectName("le_link_cam")
        self.gridLayout.addWidget(self.le_link_cam, 1, 1, 2, 1)
        self.lv_list_point = QtWidgets.QListView(self.centralwidget)
        self.lv_list_point.setObjectName("lv_list_point")
        self.gridLayout.addWidget(self.lv_list_point, 3, 1, 2, 1)
        self.btn_start_viewing = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_viewing.setObjectName("btn_start_viewing")
        self.gridLayout.addWidget(self.btn_start_viewing, 1, 2, 2, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 2, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 2, 1)
        self.btn_clear_polygon = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear_polygon.setObjectName("btn_clear_polygon")
        self.gridLayout.addWidget(self.btn_clear_polygon, 3, 2, 1, 1)
        self.btn_extract_polygon = QtWidgets.QPushButton(self.centralwidget)
        self.btn_extract_polygon.setObjectName("btn_extract_polygon")
        self.gridLayout.addWidget(self.btn_extract_polygon, 4, 2, 1, 1)
        self.stream_window = QtWidgets.QLabel(self.centralwidget)
        self.stream_window.setObjectName("stream_window")
        self.gridLayout.addWidget(self.stream_window, 0, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 465, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_start_viewing.setText(_translate("MainWindow", "Start viewing"))
        self.label_2.setText(_translate("MainWindow", "Link cam"))
        self.label_3.setText(_translate("MainWindow", "Points"))
        self.btn_clear_polygon.setText(_translate("MainWindow", "Clear Polygon"))
        self.btn_extract_polygon.setText(_translate("MainWindow", "Extract Polygon"))
        self.stream_window.setText(_translate("MainWindow", "No stream available"))
