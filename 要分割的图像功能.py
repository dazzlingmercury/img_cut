from PyQt5.QtWidgets import QMainWindow, QSlider, QMessageBox,QFileDialog
from 要分割的图像 import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from Grabcut自动分割功能 import Grabcut
import cv2
import numpy as np
import Grabcut交互分割
from 帮助文档界面功能 import Bang_zhu
class Yao_fen_ge_de_tu_xiang(QMainWindow,Ui_MainWindow,QThread):
    def __init__(self):
        super(Yao_fen_ge_de_tu_xiang, self).__init__()
        self.setupUi(self)
        # self.total_name = []
        self.total_name = []
        self.image_name = []
        self.directory1 = ''
        self.s_image = ''
        self.open_bangzhu = Bang_zhu()


        # 调用函数
        self.she_zhi_yin_cang()
        self.bang_ding_xin_hao_cao()
        self.can_shu_xuan_ze_she_zhi()







    # 设置隐藏
    def she_zhi_yin_cang(self):
        self.label_7.setHidden(True)
        self.label.setHidden(True)
        self.comboBox.setHidden(True)
        self.comboBox_2.setHidden(True)
        self.label_5.setHidden(True)
        self.label_6.setHidden(True)

        self.label_8.setHidden(True)
        self.horizontalSlider.setHidden(True)
        self.lineEdit.setHidden(True)
        self.label_10.setHidden(True)
        self.label_11.setHidden(True)
        self.spinBox.setHidden(True)
        self.spinBox_2.setHidden(True)

        self.textBrowser.setHidden(True)




    # 绑定信号
    def bang_ding_xin_hao_cao(self):
        self.pushButton_3.clicked.connect(self.tian_jia)
        self.pushButton_5.clicked.connect(self.qing_kong)
        self.pushButton_6.clicked.connect(self.bao_cun_lu_jing)
        self.pushButton_4.clicked.connect(self.shan_chu)

        self.listWidget.itemClicked.connect(self.dian_ji_xian_shi_tu_pian)

        self.radioButton.toggled.connect(self.xian_shi_otsu)
        self.radioButton_3.toggled.connect(self.xian_shi_jian_dan_yu_zhi_fen_ge)
        self.radioButton_4.toggled.connect(self.xian_shi_grabcut)
        self.radioButton_5.toggled.connect(self.xian_shi_jiao_hu_grabcut)
        self.horizontalSlider.valueChanged.connect(self.hua_dong_hua_dong_tiao)
        self.pushButton.clicked.connect(self.kai_shi_fen_ge)
        self.checkBox_2.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_3.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_4.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_5.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_6.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_7.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox_8.stateChanged.connect(self.she_zhi_jin_yong_guan_xi)
        self.checkBox.stateChanged.connect(self.pi_liang_fen_ge)
        self.pushButton_2.clicked.connect(self.bao_cun_tu_xiang)
        self.actionshiyong.triggered.connect(self.bang_zhu)




    def bang_zhu(self):
        self.open_bangzhu.show()


    def bao_cun_tu_xiang(self):
        if self.checkBox.isChecked() == False:
            if len(self.s_image) == 0:
                QMessageBox.information(self, "提示", "您还没有要保存的图片")

            else:
                print(self.s_image)
                s_fname, ok2 =  QFileDialog.getSaveFileName(self, "保存图像", "/", "All Files (*);;Image files(*.jpg *.gif *.png)")
                print(s_fname)
                if len(s_fname) == 0:
                    QMessageBox.information(self, "提示", "未选择保存路径请重新保存")
                else:
                    cv2.imencode('.jpg', self.s_image)[1].tofile(s_fname)


    def she_zhi_jin_yong_guan_xi(self):

        a = 1 if self.checkBox_2.isChecked() == True else 0
        b = 1 if self.checkBox_3.isChecked() == True else 0
        c = 1 if self.checkBox_4.isChecked() == True else 0
        d = a+b+c
        if d == 2:
            if self.checkBox_2.isChecked() == False:
                self.checkBox_2.setEnabled(False)
            if self.checkBox_3.isChecked() == False:
                self.checkBox_3.setEnabled(False)
            if self.checkBox_4.isChecked() == False:
                self.checkBox_4.setEnabled(False)
        else:
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True)
        if self.checkBox_5.isChecked() == True or self.checkBox_6.isChecked() == True:
            self.checkBox_7.setEnabled(False)
            self.checkBox_8.setEnabled(False)
        elif self.checkBox_7.isChecked() == True:
            self.checkBox_5.setEnabled(False)
            self.checkBox_6.setEnabled(False)
            self.checkBox_8.setEnabled(False)
        elif self.checkBox_8.isChecked() == True:
            self.checkBox_5.setEnabled(False)
            self.checkBox_6.setEnabled(False)
            self.checkBox_7.setEnabled(False)
        else:
            self.checkBox_5.setEnabled(True)
            self.checkBox_6.setEnabled(True)
            self.checkBox_7.setEnabled(True)
            self.checkBox_8.setEnabled(True)


    def pi_liang_fen_ge(self):
        if self.checkBox.isChecked() == True:
            QMessageBox.information(self, "提示", "已启用批量分割")
            if len(self.directory1) == 0:
                QMessageBox.information(self, "提示", "您还未选择保存路径,请选择")
                self.directory1 = QFileDialog.getExistingDirectory(self, "请选择保存路径", "/")

            self.label.setHidden(True)
            self.label_7.setHidden(True)
            self.textBrowser.setHidden(False)
            self.total_name = []
            # 获取listwidget中条目数
            count = self.listWidget.count()
            # 遍历listwidget中的内容
            for i in range(count):
                self.total_name.append(self.listWidget.item(i).text())

        elif self.checkBox.isChecked() == False:
            self.textBrowser.setHidden(True)
            self.textBrowser.clear()



    # 点击显示图片
    def dian_ji_xian_shi_tu_pian(self,item):
        if self.checkBox.isChecked() == False:
            self.image_name = []
            self.label.setHidden(False)
            self.label.setPixmap(QPixmap(item.text()))
            self.image_name.append(item.text())



    # 显示图像路径
    def xian_shi_tu_xiang_wen_ben(self,fname):
        self.listWidget.addItem('{}'.format(fname))
    # 添加图片
    def tian_jia(self):
        self.total_name = []
        self.fname, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "/", "Image files(*.jpg *.png)")

        for i in self.fname:
            self.listWidget.addItem('{}'.format(i))
        # 获取listwidget中条目数
        count = self.listWidget.count()
        # 遍历listwidget中的内容
        for i in range(count):
            self.total_name.append(self.listWidget.item(i).text())
    # 选择保存路径
    def bao_cun_lu_jing(self):
        if  self.listWidget.count() == 0:
            QMessageBox.information(self, "提示", "请选择要分割的图片")
        else:

            # QMessageBox.information(self, "提示", "请选择保存路径")
            self.directory1 = QFileDialog.getExistingDirectory(self, "请选择保存路径", "/")




    # 清空
    def qing_kong(self):
        self.total_name = []
        self.listWidget.clear()
        # 获取listwidget中条目数
        count = self.listWidget.count()
        # 遍历listwidget中的内容
        for i in range(count):
            self.total_name.append(self.listWidget.item(i).text())
    # 删除
    def shan_chu(self):
        self.total_name = []
        # 获取当前选择的数据
        item = self.listWidget.currentItem()
        # 获取选择的行数
        a = self.listWidget.row(item)
        # 删除选中行数
        self.listWidget.takeItem(a)
        # 获取listwidget中条目数
        count = self.listWidget.count()
        # 遍历listwidget中的内容
        for i in range(count):
            self.total_name.append(self.listWidget.item(i).text())

    # 参数默认设置
    def can_shu_xuan_ze_she_zhi(self):
        # 设置滑动条参数
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setValue(127)
        self.lineEdit.setText('127')
        # 设置不可编辑
        self.lineEdit.setFocusPolicy(Qt.NoFocus)

        self.spinBox.setMaximum(1000)
        self.spinBox_2.setMaximum(1000)
        self.spinBox.setMinimum(0)
        self.spinBox_2.setMinimum(0)
        self.spinBox.setValue(200)
        self.spinBox_2.setValue(100)

    # 滑动条
    def hua_dong_hua_dong_tiao(self):
        self.lineEdit.setText(str(self.horizontalSlider.value()))







    def xian_shi_otsu(self):
        if self.radioButton.isChecked() == False:
            # 设置隐藏
            self.checkBox_2.setHidden(True)
            self.checkBox_3.setHidden(True)
            self.checkBox_4.setHidden(True)
            self.checkBox_5.setHidden(True)
            self.checkBox_6.setHidden(True)
            self.checkBox_7.setHidden(True)
            self.checkBox_8.setHidden(True)


            # 取消选中
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_9.setChecked(False)
            self.checkBox.setChecked(False)
            # 设置隐藏
            self.label_3.setHidden(True)
            self.label_4.setHidden(True)
            self.comboBox.setHidden(True)
            self.comboBox_2.setHidden(True)
            self.label_5.setHidden(True)
            self.label_6.setHidden(True)

            self.label_10.setHidden(True)
            self.label_11.setHidden(True)
            self.spinBox.setHidden(True)
            self.spinBox_2.setHidden(True)
            self.label_9.setHidden(True)
            self.checkBox_9.setHidden(True)



        else:
            self.checkBox_2.setHidden(False)
            self.checkBox_3.setHidden(False)
            self.checkBox_4.setHidden(False)
            self.checkBox_5.setHidden(False)
            self.checkBox_6.setHidden(False)
            self.checkBox_7.setHidden(False)
            self.checkBox_8.setHidden(False)
            self.label_3.setHidden(False)
            self.label_4.setHidden(False)

            self.comboBox.setHidden(True)
            self.comboBox_2.setHidden(True)
            self.label_5.setHidden(True)
            self.label_6.setHidden(True)

            self.checkBox_9.setHidden(False)
            self.label_9.setHidden(False)

    def xian_shi_jian_dan_yu_zhi_fen_ge(self):
        if self.radioButton_3.isChecked() == True:
            self.label_8.setHidden(False)
            self.horizontalSlider.setHidden(False)
            self.lineEdit.setHidden(False)

            self.checkBox_2.setHidden(False)
            self.checkBox_3.setHidden(False)
            self.checkBox_4.setHidden(False)
            self.checkBox_5.setHidden(False)
            self.checkBox_6.setHidden(False)
            self.checkBox_7.setHidden(False)
            self.checkBox_8.setHidden(False)

            self.label_3.setHidden(False)
            self.label_4.setHidden(False)

            self.checkBox_9.setHidden(False)
            self.label_8.setHidden(False)
            self.label_9.setHidden(False)

        else:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_9.setChecked(False)

            self.checkBox.setChecked(False)

            self.label_8.setHidden(True)
            self.horizontalSlider.setHidden(True)
            self.lineEdit.setHidden(True)

            self.checkBox_2.setHidden(True)
            self.checkBox_3.setHidden(True)
            self.checkBox_4.setHidden(True)
            self.checkBox_5.setHidden(True)
            self.checkBox_6.setHidden(True)
            self.checkBox_7.setHidden(True)
            self.checkBox_8.setHidden(True)

            self.label_3.setHidden(True)
            self.label_4.setHidden(True)

            self.label_5.setHidden(True)
            self.label_6.setHidden(True)
            self.comboBox.setHidden(True)
            self.comboBox_2.setHidden(True)
            self.checkBox_9.setHidden(True)
            self.label_10.setHidden(True)
            self.label_11.setHidden(True)
            self.spinBox.setHidden(True)
            self.spinBox_2.setHidden(True)
            self.label_9.setHidden(True)

    def xian_shi_grabcut(self):
        if self.radioButton_4.isChecked() == True:
            self.checkBox_2.setHidden(False)
            self.checkBox_3.setHidden(False)
            self.checkBox_4.setHidden(False)
            self.label_3.setHidden(False)
        else:
            self.checkBox_2.setHidden(True)
            self.checkBox_3.setHidden(True)
            self.checkBox_4.setHidden(True)
            self.label_3.setHidden(True)

            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox.setChecked(False)

    def xian_shi_jiao_hu_grabcut(self):
        if self.radioButton_5.isChecked() == True:

            self.label_2.setHidden(True)
            self.checkBox.setHidden(True)


        else:

            self.label_2.setHidden(False)
            self.checkBox.setHidden(False)
            self.checkBox.setChecked(False)

    def kai_shi_fen_ge(self):

        if self.checkBox.isChecked() == True:
            image_name = self.total_name

        elif self.checkBox.isChecked() == False:
            image_name = self.image_name

        if self.radioButton.isChecked() == True:
            for i in image_name:
                self.s_image = self.otsu_and_quanju_shi_xian(i,int(self.comboBox.currentText()),int(self.comboBox_2.currentText()))
            self.label_7.setPixmap(QPixmap('linshi.jpg'))
            if self.checkBox.isChecked() == False:
                self.label_7.setHidden(False)

        if self.radioButton_3.isChecked() == True:
            for i in image_name:
                self.s_image = self.otsu_and_quanju_shi_xian(i, int(self.comboBox.currentText()),int(self.comboBox_2.currentText()))

            self.label_7.setPixmap(QPixmap('linshi.jpg'))
            if self.checkBox.isChecked() == False:
                self.label_7.setHidden(False)


        if self.radioButton_4.isChecked() == True:
            grabcut = Grabcut()
            for file_name in image_name:
                a ,self.s_image= grabcut.run(file_name,self.checkBox.isChecked(),self.checkBox_2.isChecked(),self.checkBox_3.isChecked(),self.checkBox_4.isChecked(),self.directory1)
                self.textBrowser.append(a)
            self.label_7.setPixmap(QPixmap('linshi.jpg'))
            if self.checkBox.isChecked() == False:
                self.label_7.setHidden(False)

        if self.radioButton_5.isChecked() == True:
            Grabcut交互分割.run(self.image_name[0])
            cv2.destroyAllWindows()

    def otsu_and_quanju_shi_xian(self,file_name,ci_shu_1,ci_shu_2):
        a = 1 if self.checkBox_2.isChecked() == True else 0
        b = 3 if self.checkBox_3.isChecked() == True else 0
        c = 5 if self.checkBox_4.isChecked() == True else 0
        a1 = 1 if self.checkBox_5.isChecked() == True else 0
        b1 = 3 if self.checkBox_6.isChecked() == True else 0
        c1 = 5 if self.checkBox_7.isChecked() == True else 0
        d1 = 7 if self.checkBox_8.isChecked() == True else 0

        d = a+b+c
        e1 = a1+b1+c1+d1

        def zhong_zhi_lv_bo(image):
            image = cv2.medianBlur(image, 5)
            return image

        def shuang_bian_lv_bo(image):
            image = cv2.bilateralFilter(image, 9, 75, 75)
            return image

        def gao_si_lv_bo(image):
            image = cv2.GaussianBlur(image, (3, 3), 2)
            return image
        def fu_shi(image,ci_shu_1):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            image = cv2.erode(image, kernel,ci_shu_1)
            return image
        def peng_zhang(image,ci_shu_2):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            image = cv2.dilate(image, kernel,ci_shu_2)
            return image
        def kai_cao_zuo(image):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
            return image
        def bi_cao_zuo(image):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            return image

        # for file_name in file_name_list:
        name = file_name.split('/')[-1]
        img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
        if d == 1:
            img0 = zhong_zhi_lv_bo(img)
        elif d == 3:
            img0 = shuang_bian_lv_bo(img)
        elif d == 5:
            img0 = gao_si_lv_bo(img)
        elif d == 4:
            img0 = zhong_zhi_lv_bo(img)
            img0 = shuang_bian_lv_bo(img0)
        elif d == 6:
            img0 = zhong_zhi_lv_bo(img)
            img0 = gao_si_lv_bo(img0)
        elif d == 8:
            img0 = shuang_bian_lv_bo(img)
            img0 = gao_si_lv_bo(img0)
        else:
            pass
        if self.checkBox_2.isChecked() == True or self.checkBox_3.isChecked() == True or self.checkBox_4.isChecked() == True:
            gray = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        if self.radioButton.isChecked() == True:
            ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  # 方法选择为THRESH_OTSU
        else:
            ret1, th1 = cv2.threshold(gray, int(self.lineEdit.text()), 255, cv2.THRESH_BINARY)
        if e1 == 1:
            th1 = fu_shi(th1,ci_shu_1)
        elif e1 == 3:
            th1 = peng_zhang(th1,ci_shu_2)
        elif e1 == 5:
            th1 = kai_cao_zuo(th1)
        elif e1 == 7:
            th1 = bi_cao_zuo(th1)
        elif e1 == 4:
            th1 = fu_shi(th1,ci_shu_1)
            th1 = peng_zhang(th1,ci_shu_2)
        else:
            pass
        # canny = cv2.Canny(blur, 50, 150)
        image = cv2.bitwise_and(img, img, mask=th1)
        cv2.imwrite('linshi.jpg', image)

        if self.checkBox.isChecked() == True:
            cv2.imencode('.jpg', image)[1].tofile(self.directory1+'/{}'.format(name))
            self.textBrowser.append('{}分割完成'.format(file_name))  # 文本框逐条添加数据
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        return image





