import pandas as pd
import sys

OUTPUT_DIR = "./public/csv/output/"
FILENAME = [
    "mri_cron_num.csv"
]

# cs読み込みに使用するクラス
class ReadCsv:
    def __init__(self, path):
        self.df =  pd.read_csv(path, header=0)

    def replace(self):
        for index, row in self.df.iterrows():
            replace_str = str("%02d" % index) + "_" + row["impact_id"]
            self.df.iloc[index, 1] = replace_str

if __name__ == "__main__":
    df_subject = ReadCsv(OUTPUT_DIR + FILENAME[0])
    df_subject.replace()
    df_main = df_subject.df
    df_main.to_csv(OUTPUT_DIR + 'mri_cron.csv', index=False)