# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np

dataset_dir = './'

def hog_func():
    argv = sys.argv
    argc = len(argv)
    if (argc != 2):
        #引数がちゃんとあるかチェック
        #正しくなければメッセージを出力して終了
        print('Usage: python %s arg1' %argv[0])
        quit()
    # 画像の読み込み
    img_name = dataset_dir + argv[1]
    im = cv2.imread(img_name)
    #im = im[:, 450:, :]
    # HoG特徴量の計算
    hog = cv2.HOGDescriptor()
    # SVMによる人検出
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    winstride = np.array([5, 5])
    padding = np.array([4, 4])
    scale = 1.05
    finalthreshold = 1.0

    hogParams = {'winStride': tuple(winstride), 'padding': tuple(padding), 'scale': scale, 'finalThreshold': finalthreshold, 'useMeanshiftGrouping': True}
    
    # 人を検出した座標
    human, r = hog.detectMultiScale(im, **hogParams)
    print(len(human))

    # 長方形で人を囲う
    for (x, y, w, h) in human:
        cv2.rectangle(im, (x, y),(x+w, y+h),(0,50,255), 3)
        pickimg = im[x:x+w][:]
    # 人を検出した座標
    cv2.imshow("Human detection",im)
    # cv2.imshow("djak", pickimg)
    cv2.waitKey(0)
    # 画像保存
    out_file_name = "after" + argv[1]
    #cv2.imwrite(out_file_name,im)
    print("saved")


if __name__ == '__main__':
    hog_func()
