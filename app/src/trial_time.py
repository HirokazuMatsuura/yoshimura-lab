import pandas as pd
import const as ct
import csv_basic as cb
import os

CSV_DIR = ct.CSV_DIR
CSV_HEADER = ct.CSV_HEADER
TRIAL_TIME_COLUMN = ct.TRIAL_TIME_COLUMN
COLUMN_NAME = ['file_name', 'trial_time']
SAVE_DIR = ct.OUTPUT_DIR
SAVE_FILENAME = ct.OUTPUT_FILENAME_TRIAL_TIME


# cs読み込みに使用するクラス
class ReadCsv:
    def read_csv(self, path, names):
        return pd.read_csv(path, names=names)

# pandasデータを読み込んで加工するために使用するクラス
class AbstructDataframe:
    def __init__(self, df, column):
        self.df = df[column]

class TrialDataframe(AbstructDataframe):
    def __init__(self, df, column=TRIAL_TIME_COLUMN):
        self.df = df[column]

    # trial_idを指定するとそれに対応したdfをindexを0から振り直して返す
    def extraction(self):
        df_ex = self.df.query('trial_time != 0').reset_index(drop=True)
        return df_ex

if __name__ == "__main__":
    trial_time_data = cb.TrialTimeInfo(COLUMN_NAME)
    csv_filenames = os.listdir(CSV_DIR)
    for csv_filename in csv_filenames:
        csv_file = ReadCsv()
        trial_times = TrialDataframe(csv_file.read_csv(CSV_DIR + csv_filename, CSV_HEADER))
        trial_time_data.add_Dataframe(csv_filename, trial_times.extraction().mean()["trial_time"])
    trial_time_data.write_Dataframe(SAVE_DIR + SAVE_FILENAME)