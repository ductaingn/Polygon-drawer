import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal as Signal
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ..utils.convex_hull import graham_scan

class Canvas(QWidget):
    updateConvexHull = Signal(list)
    updatePoint = Signal(tuple)

    def __init__(self, size=(800,600), parent=None):
        super().__init__(parent)
        self.setFixedSize(size[0],size[1])
        self.image = QPixmap(self.size())
        self.image.fill(Qt.transparent)
        self.drawing = False
        self.last_point = QPoint()
        self.points = set()
        self.convex_hull = []

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.setRenderHint(QPainter.Antialiasing)
        canvas_painter.drawPixmap(self.rect(), self.image, self.image.rect())

    def clear(self):
        if len(self.points) > 0:
            self.image.fill(Qt.transparent)
            self.update()
            self.last_point = QPoint()
            self.points = set()
            self.convex_hull = []
        else:
            print('Empty hull!')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.points.add((self.last_point.x(), self.last_point.y()))
            
            painter = QPainter(self.image)
            pen = QPen(Qt.green, 4, Qt.SolidLine, Qt.RoundCap, Qt.MiterJoin)
            painter.setPen(pen)
            self.image.fill(Qt.transparent)
            
            # Draw all points
            # for point in self.points:
            #     painter.drawPoint(QPoint(point[0], point[1]))
            
            # Draw convex hull
            if len(self.points) > 2:
                hull = graham_scan(list(self.points))
                self.convex_hull = hull
                self.updateConvexHull.emit(self.convex_hull)

                polygon = [QPoint(p[0], p[1]) for p in hull]
                painter.setRenderHint(QPainter.Antialiasing)
                painter.drawPolygon(*polygon)

            elif len(self.points) <= 2:
                painter.drawPoint(QPoint(self.last_point))
                if len(self.points)==2:
                    painter.drawPolyline(*[QPoint(p[0],p[1]) for p in self.points])
            
            self.update()

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint App")
        self.setGeometry(100, 100, 800, 600)
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
