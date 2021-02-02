from PyQt5.QtWidgets import QMainWindow
from 帮助文档界面 import Ui_MainWindow


class Bang_zhu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Bang_zhu, self).__init__()
        self.setupUi(self)
