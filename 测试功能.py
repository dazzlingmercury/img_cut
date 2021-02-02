import cv2
import numpy as np

file_name_list = ['image_0002.jpg']
save_file_name = 'D:\\图像分割开发'
for file_name in file_name_list:
    # 读取原始图像
    # 解决中文问题
    img0 = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)

    img = cv2.cvtColor(img0, cv2.COLOR_BGR2HSV)

    # 图像二维像素转换为一维
    data = img.reshape((-1, 3))
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
    dst3 = res.reshape((img.shape))

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

        cv2.grabCut(img0, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)  # 函数返回值为mask,bgdModel,fgdModel

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # 0和2做背景

        img = img0 * mask2[:, :, np.newaxis]  # 使用蒙板来获取前景区域
        cv2.imencode('.jpg', img)[1].tofile(save_file_name)
        # cv2.imwrite('linshi.jpg',img)
    except:
        print('1111111')
