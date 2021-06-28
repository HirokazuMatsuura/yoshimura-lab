# /ex-yoshimura/ 直下で実行してください

# the rule of naming
# class TestTest()
# method testTest()
# function test_test()
# varianle test_test
# const TEST_TEST

import os # pathの操作
import sys # ディレクトリに置いてあるファイルの操作
import csv # csvファイル加工
import numpy as np # 数学的処理
import pandas as pd # データの行列形式変換
from numpy import linalg as LA # 数学的処理
import matplotlib.pyplot as plt # グラフ描画
from sklearn import linear_model # 線形回帰
import csvtest as cts


class PathInfoClass:
    def __init__(self, path_name:str):
        self.path_name = path_name
        self.filename = os.path.basename(path_name)

class TrialInfo:
    def __init__(self, traial_id, age, sex, path_name, origin, end, target, ans, trial_time, ans_time):
        self.traial_id = traial_id
        self.age = age
        self.sex = sex
        self.path_name = path_name
        self.origin = origin
        self.end = end
        self.target = target
        self.ans = ans
        self.trial_time = trial_time
        self.ans_time = ans_time
        # angleを計算
        np_origin = np.array(origin)
        np_end = np.array(end)
        np_target = np.array(target)
        np_array_A = np_end - np_origin
        np_array_B = np_target - np_origin
        inner = np.inner(np_array_A, np_array_B)
        norm = LA.norm(np_array_A) * LA.norm(np_array_B)
        cos = inner / norm
        angle = np.rad2deg(np.arccos(np.clip(cos, -1.0, 1.0)))
        self.angle = angle

def file_path_list(path):
    pathlist = list()
    object_list = os.listdir(path)
    for dir in object_list:
        if not dir.startswith('.'):
            pathlist.append(path + dir)
    return pathlist

def get_all_file_paths(pathlist):
    filenames = list()
    for path in pathlist:
        for filename in os.listdir(path):
            path_class = PathInfoClass(path + "/" + filename)
            filenames.append(path_class)
    return filenames

# file情報を入手
def get_file_meta(file_path):
    meta_list = dict()
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            meta_list[row[2]] = [row[0], row[1]]
    return meta_list

# 個人ごとのcsvファイルを読み取り,filepath, trial_idを指定してorigin, end, target, trial_time, ans_timeの情報を入手 => classを返す
def get_trial_info(path_info, trial_id, meta_list):
    age = float(meta_list[path_info.filename][0])
    sex = meta_list[path_info.filename][1]
    path_name = path_info.path_name
    origin = list()
    end = list()
    target = list()
    ans = 0
    trial_time = 0
    ans_time = 0
    flag = 0
    with open(path_info.path_name) as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader, start=0):
            # 例外があればファイル名と行数を返す
            try:
                # castする str => float
                row = list(map(float, row))
            except ValueError:
                print(path_info.path_name)
                print(index)
                sys.exit()
            if row[0] == trial_id:
                if flag == 0:
                    flag = 1
                    origin.append(row[1])
                    origin.append(row[2])
                    origin.append(row[3])
                elif flag == 1:
                    if not row[7] == 0:
                        end.append(row[1])
                        end.append(row[2])
                        end.append(row[3])
                        target.append(row[7])
                        target.append(row[8])
                        target.append(row[9])
                        ans = row[10]
                        trial_time = row[11]
                        ans_time = row[12]
                        break
    trial_info = TrialInfo(trial_id, age, sex, path_name, origin, end, target, ans, trial_time, ans_time)
    return trial_info

def pandas_dataframe(x_array, y_array, label):
    df = pd.DataFrame({ label["x"]: x_array,
                        label["y"]: y_array})
    df = df.sort_values(label["x"])
    return df

def plot_graph(df, label, clf, trial_id, save_path):
    DIR = label["x"] + "-" + label["y"]
    TITLE = str(trial_id) + "_" + DIR
    df.plot.scatter(x=label["x"], y=label["y"], marker="o", color="red")
    plt.plot(df[[label["x"]]].values, clf.predict(df[[label["x"]]].values))
    plt.title(TITLE)
    plt.xlabel(label["x"])
    plt.ylabel(label["y"])
    # グリッド線を表示するならTrue
    plt.grid(True)
    plt.savefig(save_path + DIR + "/" + TITLE)
    # plt.show()

# 現状は自動でX, Yの変数が決まる
def def_variable(trial_list, label):
    x_value = list()
    y_value = list()
    for trial in trial_list:
        # if trial.sex == "F":
        #     x_value.append(trial.age)
        #     y_value.append(trial.ans_time)
        x_value.append(getattr(trial, label["x"]))
        y_value.append(getattr(trial, label["y"]))
    return x_value, y_value

# 線形回帰
def linear_regression(df, label):
    clf = linear_model.LinearRegression()
    try:
        clf.fit(df[[label["x"]]].values, df[label["y"]].values) # 予測モデルを作成
    except ValueError:
        print(df[label["x"]])
        print(df[label["y"]])
        sys.exit()
    return clf

if __name__ == "__main__":
    # 定数宣言
    TRIAL_ID = int(sys.argv[1])
    LABEL = {"x": "age", "y": "angle"}
    CSVFILE_META_PATH = "./public/csv/meta/out.csv"
    CSVFILE_DATA_PATH = "./public/csv/dataset/"
    SAVE_PATH = "./public/png/"

    pathlist = file_path_list(CSVFILE_DATA_PATH)
    csv_info = get_all_file_paths(pathlist)
    meta_list = get_file_meta(CSVFILE_META_PATH)
    for info in csv_info:
        print(info.path_name)
        cts.csvtest(info.path_name)
    sys.exit()

    trial_list = list()
    for part in csv_info:
        traial_info = get_trial_info(part, TRIAL_ID, meta_list)
        trial_list.append(traial_info)

    x_value, y_value = def_variable(trial_list, LABEL)
    df = pandas_dataframe(x_value, y_value, LABEL)

    # 線形回帰
    clf = linear_regression(df, LABEL)
    # グラフプロット
    plot_graph(df, LABEL, clf, TRIAL_ID, SAVE_PATH)