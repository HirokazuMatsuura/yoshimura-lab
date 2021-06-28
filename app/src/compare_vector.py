import numpy as np
import numpy.linalg as LA
import pandas as pd
import math
import csv_basic as cb
import const as ct

import os
import sys

CSV_PATH = ct.CSV_PATH
CSV_HEADER = ct.CSV_HEADER
TRIAL_NUMBER = ct.TRIAL_NUMBER
DIVIDE_PARAMETER = ct.DIVIDE_PARAMETER
TRIAL_COLUMN = ct.TRIAL_COLUMN
CSV_DIR = ct.CSV_DIR
SAVE_DIR = ct.OUTPUT_DIR
SAVE_FILENAME = ct.OUTPUT_FILENAME
COLUMN_NAME = ['file_name', 'angle']

# cs読み込みに使用するクラス
class ReadCsv:
    def read_csv(self, path, names):
        return pd.read_csv(path, names=names)

# pandasデータを読み込んで加工するために使用するクラス
class AbstructDataframe:
    def __init__(self, df, column):
        self.df = df[column]

class TrialDataframe(AbstructDataframe):
    def __init__(self, df, column=TRIAL_COLUMN):
        self.df = df[column]

    # 始点分だけ全てのベクトルを移動させる
    def __normalization(self, df):
        start_point = pd.DataFrame({
                    "hand_x": [df.iloc[0,0]] * len(df),
                    "hand_y": [df.iloc[0,1]] * len(df),
                    "hand_z": [df.iloc[0,2]] * len(df),
                    "target_x": [df.iloc[0,0]] * len(df),
                    "target_y": [df.iloc[0,1]] * len(df),
                    "target_z": [df.iloc[0,2]] * len(df)
                    })
        return df - start_point

    # trial_idを指定するとそれに対応したdfをindexを0から振り直して返す
    def extraction(self, trial_id):
        df_ex = self.df.query('trial_id ==' + str(trial_id))
        df_ex_alignment = df_ex[["hand_x", "hand_y", "hand_z", "target_x", "target_y", "target_z"]].reset_index(drop=True)
        return self.__normalization(df_ex_alignment)

# 角度を求めるのに使用するクラス
class AbstructAngle:
    # dfはindexが0から振り直された状態を想定
    def __init__(self, df):
        self.df = df

    # 終点の座標を取得
    def end_point(self):
        pass

    # 距離を取得
    def distance(self):
        pass

    # DIVIDE_PARAMETERだけ割った値を取得
    def div_distance(self):
        pass

    # DIVIDE_PARAMETER距離と最も近い距離のindexを取得
    def search_nearest_point(self):
        pass

    # indexが与えられた時にその点の座標を取得
    def get_point(self):
        pass

    # 二つのベクトルの角度の差分を求める
    def comp_vector(self):
        pass

class Angle(AbstructAngle):
    def end_point(self):
        self.__end_point = self.df[["target_x", "target_y", "target_z"]].tail(1)
        self.__end_point_index = self.df.tail(1).index[0]

    def distance(self):
        np_arr = []
        norm = 0
        distance = []
        for k, v in self.df.iterrows():
            np_arr = np.array([v["hand_x"], v["hand_y"], v["hand_z"]])
            norm = LA.norm(np_arr)
            distance.append(norm)
        self.__distance_arr = distance

    def div_distance(self):
        self.__div_distance = self.__distance_arr[self.__end_point_index] * DIVIDE_PARAMETER

    # 最も近い値を返す
    def __get_nearest_value(self, arr, num):
        """
        概要: リストからある値に最も近い値を返却する関数
        @param arr: データ配列
        @param num: 対象値
        @return 対象値に最も近い値
        """
        # リスト要素と対象値の差分を計算し最小値のインデックスを取得
        return np.abs(np.asarray(arr) - num).argmin()

    def search_nearest_point(self):
        self.__trial_point_index = self.__get_nearest_value(self.__distance_arr, self.__div_distance)

    def get_point(self):
        self.__trial_point = self.df.iloc[self.__trial_point_index][["hand_x", "hand_y", "hand_z"]]

    # 2つのベクトルから角度を求めるprivateメソッド
    def __calc_2vec_angle(self, u, v):
        # pandas型からnumpy型に変換する
        u_np = u.values
        v_np = v.values

        i = np.inner(u_np, v_np)
        n = LA.norm(u) * LA.norm(v)

        c = i / n
        return np.rad2deg(np.arccos(np.clip(c, -1.0, 1.0)))

    def comp_vector(self):
        self.angle = self.__calc_2vec_angle(self.__end_point, self.__trial_point)[0]

class CalcAngle(Angle):
    def calc_angle(self):
        self.end_point()
        self.distance()
        self.div_distance()
        self.search_nearest_point()
        self.get_point()
        self.comp_vector()
        return self.angle

# 簡単な処理系
def angle_mean(arr):
    return math.sqrt(sum(arr) / len(arr))

def square(arr):
    return list(map(lambda x: x ** 2, arr))

def sub(x, y):
    return x - y

def sub_list(tr_arr, bs_arr):
    return square(list(map(sub, tr_arr, bs_arr)))

if __name__ == "__main__":
    angle_data = cb.AngleInfo(COLUMN_NAME)
    csv_filenames = os.listdir(CSV_DIR)
    origin_pd = ReadCsv()
    origin_arr = origin_pd.read_csv("./public/csv/meta/angle_correct.csv", ["angle", "ans"])['angle'].to_list()

    for csv_filename in csv_filenames:

        angle_arr = []
        mean = 0
        csv_file = ReadCsv()
        dataframe = TrialDataframe(csv_file.read_csv(CSV_DIR + csv_filename, CSV_HEADER))

        for idx in range(108):
            trial       = dataframe.extraction(idx)
            cal_angle   = CalcAngle(trial).calc_angle()
            angle_arr.append(cal_angle)

        mean = angle_mean(sub_list(angle_arr, origin_arr))
        print(mean)
        angle_data.add_Dataframe(csv_filename, mean)

    print(angle_data.DataFrame)
    angle_data.write_Dataframe(SAVE_DIR + SAVE_FILENAME)