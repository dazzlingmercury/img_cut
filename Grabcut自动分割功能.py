import cv2
import numpy as np
import time


class Grabcut(object):
    def __init__(self):
        self.num = 1

    def run(self, file_name, checkBox, checkBox_2, checkBox_3, checkBox_4, s_file_name):
        img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
        a = 1 if checkBox_2 == True else 0
        b = 3 if checkBox_3 == True else 0
        c = 5 if checkBox_4 == True else 0
        d = a + b + c

        def zhong_zhi_lv_bo(image):
            image = cv2.medianBlur(image, 5)
            return image

        def shuang_bian_lv_bo(image):
            image = cv2.bilateralFilter(image, 9, 75, 75)
            return image

        def gao_si_lv_bo(image):
            image = cv2.GaussianBlur(image, (3, 3), 2)
            return image

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

        name = file_name.split('/')[-1]
        if d == 0:
            img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        elif d != 0:
            img1 = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)

        # 图像二维像素转换为一维
        data = img1.reshape((-1, 3))
        data = np.float32(data)

        # 定义中心 (type,max_iter,epsilon)
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # 设置标签
        flags = cv2.KMEANS_RANDOM_CENTERS

        # K-Means聚类 聚集成n类
        n = 15
        compactness, labels3, centers3 = cv2.kmeans(data, n, None, criteria, 10, flags)

        # 图像转换回uint8二维类型
        centers3 = np.uint8(centers3)
        res = centers3[labels3.flatten()]
        dst3 = res.reshape((img1.shape))

        cv2.imwrite("linshi.jpg", dst3)

        image = cv2.imread("linshi.jpg", 0)
        ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)  # 方法选择为THRESH_OTSU

        kenel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(thresh, kenel, iterations=5)  # 腐蚀

        kenel1 = np.ones((5, 5), np.uint8)
        dige_dilate = cv2.dilate(erosion, kenel1, iterations=5)  # 膨胀

        image, contours, _ = cv2.findContours(dige_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area = []
        for k in range(len(contours)):
            area.append(cv2.contourArea(contours[k]))
        max_idx = np.argmax(np.array(area))
        x, y, w, h = cv2.boundingRect(contours[max_idx])
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (x, y, w, h)  # 划定区域
        try:
            cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)  # 函数返回值为mask,bgdModel,fgdModel
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # 0和2做背景
            img = img * mask2[:, :, np.newaxis]  # 使用蒙板来获取前景区域
            if checkBox == True:
                cv2.imencode('.jpg', img)[1].tofile(s_file_name + '/{}'.format(name))
            else:
                cv2.imwrite('linshi.jpg', img)
            return name, img
        except:
            pass
