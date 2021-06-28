import pandas as pd

class CsvOperation:
    def __init__(self, columns):
        self.DataFrame = pd.DataFrame(columns=columns)
    
    def add_Dataframe(self):
        pass

    def write_Dataframe(self, path):
        self.DataFrame.to_csv(path, index=False)

class AngleInfo(CsvOperation):
    def add_Dataframe(self, file_name, angle):
        self.DataFrame = self.DataFrame.append({'file_name': file_name, 'angle': angle}, ignore_index=True)

class TrialTimeInfo(CsvOperation):
    def add_Dataframe(self, file_name, trial_time):
        self.DataFrame = self.DataFrame.append({'file_name': file_name, 'trial_time': trial_time}, ignore_index=True)

class AnsTimeInfo(CsvOperation):
    def add_Dataframe(self, file_name, ans_time):
        self.DataFrame = self.DataFrame.append({'file_name': file_name, 'ans_time': ans_time}, ignore_index=True)

class AnsInfo(CsvOperation):
    def add_Dataframe(self, file_name, ans):
        self.DataFrame = self.DataFrame.append({'file_name': file_name, 'ans': ans}, ignore_index=True)