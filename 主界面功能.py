from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QGraphicsPixmapItem, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QIcon
from 要分割的图像功能 import Yao_fen_ge_de_tu_xiang
from 帮助文档界面功能 import Bang_zhu
from 主界面 import Ui_MainWindow


class Zhu_jie_mian(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Zhu_jie_mian, self).__init__()
        self.setupUi(self)
        self.fname = []
        self.open_daifenge = Yao_fen_ge_de_tu_xiang()
        self.open_bangzhu = Bang_zhu()
        self.bang_ding_xin_hao_cao()

    def bang_ding_xin_hao_cao(self):
        self.actiondakai.triggered.connect(self.da_kai)
        self.actionshiyong.triggered.connect(self.bang_zhu)

    def da_kai(self):
        self.open_daifenge.label.clear()
        self.open_daifenge.label_7.clear()
        self.open_daifenge.listWidget.clear()
        self.fname, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "/", "Image files(*.jpg *.png)")
        if len(self.fname) == 0:
            QMessageBox.information(self, "提示", "请选择图片")
        else:
            self.open_daifenge.show()
            for i in self.fname:
                self.open_daifenge.xian_shi_tu_xiang_wen_ben(i)

    def bang_zhu(self):
        self.open_bangzhu.show()
