import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QSlider, QMessageBox, QFileDialog
from 要分割的图像 import Ui_MainWindow
from 要分割的图像功能 import Yao_fen_ge_de_tu_xiang
import cv2


class Otsu(Yao_fen_ge_de_tu_xiang):
    file_name_list = []

    def zhong_zhi_lv_bo(self, image):
        image = cv2.medianBlur(image, 5)
        return image

    def shuang_bian_lv_bo(self, image):
        image = cv2.bilateralFilter(image, 9, 75, 75)
        return image

    def gao_si_lv_bo(self, image):
        image = cv2.GaussianBlur(image, (3, 3), 2)
        return image

    def xing_tai_xue(self):
        pass

    def bian_yuan_jian_ce(self):
        pass

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # 腐蚀图像
    eroded = cv2.erode(img, kernel)
    # 显示腐蚀后的图像
    cv2.imshow("Eroded Image", eroded);

    # 膨胀图像
    dilated = cv2.dilate(img, kernel)
