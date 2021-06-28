import pandas as pd

OUTPUT_DIR = "./public/csv/output/"
FILENAME = [
    "subject_data.csv",
    "angle.csv",
    "ans.csv",
    "ans_time.csv",
    "trial_time.csv",
    "mri_cron.csv"
]
# cs読み込みに使用するクラス
class ReadCsv:
    def __init__(self, path):
        self.df =  pd.read_csv(path, header=0)

if __name__ == "__main__":
    df_subject = ReadCsv(OUTPUT_DIR + FILENAME[0])
    df_angle = ReadCsv(OUTPUT_DIR + FILENAME[1])
    df_ans = ReadCsv(OUTPUT_DIR + FILENAME[2])
    df_ans_time = ReadCsv(OUTPUT_DIR + FILENAME[3])
    df_trial_time = ReadCsv(OUTPUT_DIR + FILENAME[4])
    df_mri_num = ReadCsv(OUTPUT_DIR + FILENAME[5])

    df_main = pd.merge(df_subject.df, df_angle.df, on='file_name', how='inner')
    df_main = pd.merge(df_main, df_ans.df, on='file_name', how='inner')
    df_main = pd.merge(df_main, df_ans_time.df, on='file_name', how='inner')
    df_main = pd.merge(df_main, df_trial_time.df, on='file_name', how='inner')
    df_main = pd.merge(df_main, df_mri_num.df, on='file_name', how='inner')

    df_main.to_csv(OUTPUT_DIR + 'result.csv', index=False)