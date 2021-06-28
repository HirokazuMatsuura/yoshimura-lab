import pandas as pd
import const as ct
import csv_basic as cb
import os

CSV_DIR = ct.CSV_DIR
CSV_HEADER = ct.CSV_HEADER
ANS_COLUMN = ct.ANS_COLUMN
COLUMN_NAME = ['file_name', 'ans']
SAVE_DIR = ct.OUTPUT_DIR
SAVE_FILENAME = ct.OUTPUT_FILENAME_ANS

# cs読み込みに使用するクラス
class ReadCsv:
    def read_csv(self, path, names):
        return pd.read_csv(path, names=names)

# pandasデータを読み込んで加工するために使用するクラス
class AbstructDataframe:
    def __init__(self, df, column):
        self.df = df[column]

class TrialDataframe(AbstructDataframe):
    def __init__(self, df, column=ANS_COLUMN):
        self.df = df[column]

    # trial_idを指定するとそれに対応したdfをindexを0から振り直して返す
    def extraction(self):
        df_ex = self.df.query('ans != 0').reset_index(drop=True)
        return df_ex

def not_xor(x, y):
    return int(not (x ^ y))

def not_xor_arr(x_arr, y_arr):
    return list(map(not_xor, x_arr, y_arr))


if __name__ == "__main__":
    ans_data = cb.AnsInfo(COLUMN_NAME)
    csv_filenames = os.listdir(CSV_DIR)
    origin_pd = ReadCsv()
    origin_arr = origin_pd.read_csv("./public/csv/meta/angle_correct.csv", ["angle", "ans"])['ans'].to_list()


    for csv_filename in csv_filenames:
        csv_file = ReadCsv()
        answers = TrialDataframe(csv_file.read_csv(CSV_DIR + csv_filename, CSV_HEADER))
        ans_arr = answers.extraction()['ans'].to_list()
        ans_arr = [(x - 1) for x in ans_arr]
        ans_sum = sum(not_xor_arr(ans_arr, origin_arr))
        ans_data.add_Dataframe(csv_filename, ans_sum)
    ans_data.write_Dataframe(SAVE_DIR + SAVE_FILENAME)