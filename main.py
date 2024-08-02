import sys
import signal
from main_app.controllers.main_controller import MainWindow
from PyQt5 import QtWidgets

import os
os.environ['KMP_DUPLICATE_LIB_OB'] = " "

if __name__=="__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())