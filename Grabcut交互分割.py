import numpy as np
import cv2

BLUE = [255, 0, 0]  # rectangle color
RED = [0, 0, 255]  # PR BG
GREEN = [0, 255, 0]  # PR FG
BLACK = [0, 0, 0]  # sure BG
WHITE = [255, 255, 255]  # sure FG

DRAW_BG = {'color': BLACK, 'val': 0}
DRAW_FG = {'color': WHITE, 'val': 1}
DRAW_PR_FG = {'color': GREEN, 'val': 3}
DRAW_PR_BG = {'color': RED, 'val': 2}

rect = (0, 0, 1, 1)
drawing = False  # flag for drawing curves
rectangle = False  # flag for drawing rect
rect_over = False  # flag to check if rect drawn
rect_or_mask = 100  # flag for selecting rect or mask mode
value = DRAW_FG  # drawing initialized to FG
thickness = 3  # brush thickness


def onmouse(event, x, y, flags, param):
    global img, img2, drawing, value, mask, rectangle, rect, rect_or_mask, ix, iy, rect_over

    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv2.rectangle(img, (ix, iy), (x, y), BLUE, 2)
            rect = (ix, iy, abs(ix - x), abs(iy - y))
            rect_or_mask = 0

    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv2.rectangle(img, (ix, iy), (x, y), BLUE, 2)
        rect = (ix, iy, abs(ix - x), abs(iy - y))
        rect_or_mask = 0

    if event == cv2.EVENT_LBUTTONDOWN:
        if rect_over == False:
            pass
        else:
            drawing = True
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)


def run(fname):
    filename = '{}'.format(fname)
    global img, img2, drawing, value, mask, rectangle, rect, rect_or_mask, ix, iy, rect_over
    img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
    img2 = img.copy()  # a copy of original image
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  # mask initialized to PR_BG
    output = np.zeros(img.shape, np.uint8)  # output image to be shown

    cv2.namedWindow('output')
    cv2.namedWindow('input')
    cv2.setMouseCallback('input', onmouse)
    cv2.moveWindow('input', img.shape[1] + 10, 90)

    while (1):

        cv2.imshow('output', output)
        cv2.imshow('input', img)
        k = 0xFF & cv2.waitKey(1)

        # key bindings
        if k == 27:  # esc to exit
            break
        elif k == ord('0'):  # BG drawing
            value = DRAW_BG
        elif k == ord('1'):  # FG drawing
            value = DRAW_FG
        elif k == ord('2'):  # PR_BG drawing
            value = DRAW_PR_BG
        elif k == ord('3'):  # PR_FG drawing
            value = DRAW_PR_FG
        elif k == ord('s'):  # save image
            cv2.imencode('.jpg', output)[1].tofile('linshi.jpg')  # 保存图片
        elif k == ord('r'):  # reset everything
            rect = (0, 0, 1, 1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            rect_over = False
            value = DRAW_FG
            img = img2.copy()
            mask = np.zeros(img.shape[:2], dtype=np.uint8)  # mask initialized to PR_BG
            output = np.zeros(img.shape, np.uint8)  # output image to be shown
        elif k == ord('n'):  # segment the image
            if (rect_or_mask == 0):  # grabcut with rect
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
                rect_or_mask = 1
            elif rect_or_mask == 1:  # grabcut with mask
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
        output = cv2.bitwise_and(img2, img2, mask=mask2)
