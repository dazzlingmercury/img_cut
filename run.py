import sys
from 主界面功能 import Zhu_jie_mian
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    zhujiemian = Zhu_jie_mian()
    zhujiemian.show()
    sys.exit(app.exec_())

# import sys
#
# from PyQt5.QtWidgets import QApplication, QMainWindow
#
# import 布局
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     mainwindow = 布局.Ui_MainWindow()
#
#     mainwindow.show()
#     sys.exit(app.exec_())
