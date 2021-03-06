# ---------------------------------------------------------------------
# start    : 2017/09/24-
# filename : 1hLaterRain.py
# data     : 現在の雨量・気温・風速・湿度、１時間前の気温・風速・湿度
#            RaspberryPiから値を 取ってきたい
# memo     : 保存した学習モデル(./model/)を使って1時間後の雨量を予測、txtファイルで書き出し
# ---------------------------------------------------------------------

import pickle
import numpy as np
import pandas as pd
import os.path


#保存した機械学習モデルを使って予測値を算出
def loaded_mod(mod_name, MU, SE):

    #保存した機械学習モデルをロード
    loaded_mod = pickle.load(open(mod_name, 'rb'))

    #予測値算出
    rain_zscore = loaded_mod.predict(wether)

    #算出された値はZ-scoreなので値を元に戻す
    #雨量のZ-score(rain_zscore) = 予測雨量(rain_later) - 教師データの平均雨量(MU) / 教師データの標準偏差(SE)より
    rain_later = (rain_zscore * SE) + MU

    # 結果出力
    print('======1時間後の雨量======')
    print('         %.3f          ' % (rain_later))
    print('=========================')
    print('by ' + mod_name + '\n')

    # 結果書き出し
    f = open('./result/result.txt', 'w')
    f.write(str(int(rain_later[0])))
    f.close


if __name__ == '__main__':

    #気象情報を入力を受け取る
    rain = 30 #float(input("雨量："))
    temp = 24 #float(input("気温："))
    wind = 0.6 #float(input("風速："))
    humidity = 77 #float(input("湿度："))
    temp_ago = 30 #float(input("1時間前の気温："))
    wind_ago = 0.1 #float(input("1時間前の風速："))
    humidity_ago = 77 #float(input("1時間前の湿度："))
    print('\n')

    #ベクトル化（1次元配列だとWarningが出るので2次元配列にしておく）
    wether = np.array([[rain, temp, wind, humidity, (temp_ago - temp), (wind_ago - wind), (humidity_ago - humidity)]])

    #入力データの標準化
    #教師データ読み込み
    data_train = pd.read_csv('./kochi_train/input.csv')
    data_train = data_train.iloc[:, (len(data_train.columns)-7):len(data_train.columns)]

    #教師データの各気象情報の平均、標準偏差算出
    MU = list(data_train.mean())
    SE = list(data_train.std())

    #教師データの平均、標準偏差を使って入力データを標準化
    for i in range(7):
        wether[:, [i]] = (wether[:, [i]] - MU[i]) / SE[i]


    #機械学習モデルをロード
    #保存した機械学習モデルのファイル名を読み込む
    models = os.listdir('./model/')

    #model = [LinerRegression.sav, NeuralNetwork.sav, NeuralNetworkRegression.sav,
    #         RandomForestRegression.sav, RogisticRegression.sav]

    #for i in range(len(models)):
    #    mod_name = './model/' + models[i]
    #    保存した機械学習モデルを使って予測値を算出
    #    loaded_mod(mod_name, MU[0], SE[0])

    mod_name = './model/' + models[2]
    #NeuralNetworkRegression.savを使って予測値を算出
    loaded_mod(mod_name, MU[2], SE[2])
