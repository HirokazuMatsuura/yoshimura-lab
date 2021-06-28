import pandas as pd
import os
import sys

header = {
    "Trial": [
        "id",
        "hand_x",
        "hand_y",
        "hand_z", 
        "head_x", 
        "head_y", 
        "head_z", 
        "target_x", 
        "target_y", 
        "target_z", 
        "ans", 
        "trial_time",
        "ans_time"],
    "TrialMeta": [
        "age",
        "sex",
        "file_name"
    ],
    "FileMeta": [
        "defined_angle",
        "defined_answer"
    ]
}

error_type_dict = {
    "Normally": "This file is Normally.",
    "NullValue": "This file has null value.",
    "MissingRow": "This file has missing rows."
}

# AbstractFactory
class AbstructCsvFactory:
    def __init__(self, csv_factory, read_path):
        self.factory = csv_factory
        self.path = read_path

    def test_csv(self):
        self.csv_array = pd.DataFrame()
        self.error_index = []
        self.error_type = error_type_dict["Normally"]
        self.csv_array = self.factory.read_csv(self.path)
        self.error_index, self.error_type = self.factory.check_csv(self.csv_array) 
        self.__print_error()

    def __print_error(self):
        print(self.error_type)
        if len(self.error_index) != 0:
            print("Error row is " + str(self.error_index))

    # createproduct
    def read_csv(self, read_path):
        return pd.read_csv(read_path)

    # createproduct
    def check_csv(self, csv_array):
        pass
    
    # createproduct
    # def write_csv(self, write_path="./"):
    #     pass

# ConcreteFactory
class CsvFactoryTrial(AbstructCsvFactory):
    def __init__(self):
        pass
    
    @classmethod
    def read_csv(cls, read_path):
        return cls.ReadTrial(read_path).read()
    
    @classmethod
    def check_csv(cls, csv_array):
        error = cls.CheckTrial(csv_array)
        error.error()
        return error.error_index, error.error_type
    
    class ReadTrial:
        def __init__(self, read_path):
            self.file_path = read_path
            self.names = header["Trial"]
        
        def read(self):
            return pd.read_csv(self.file_path, names=self.names)
    
    class CheckTrial:
        def __init__(self, csv_array):
            self.csv_array = csv_array
            self.error_index = []
            self.error_type = error_type_dict["Normally"]

        def error(self):
            if self.csv_array[self.csv_array["id"] == 107].empty:
                self.error_index.append(len(self.csv_array) - 1)
                self.error_type = error_type_dict["MissingRow"]
            elif(self.csv_array.isnull().values.sum() != 0):
                for index, row in enumerate(self.csv_array.isnull().any(axis=1).values, start=1):
                    if row == True:
                        self.error_index.append(index)
                self.error_type = error_type_dict["NullValue"]
            else:
                pass


# ConcreteFactory
class CsvFactoryTrialMeta(AbstructCsvFactory):
    def __init__(self):
        pass
    
    @classmethod
    def read_csv(cls, read_path):
        return cls.ReadTrial(read_path).read()
    
    @classmethod
    def check_csv(cls, csv_array):
        error = cls.CheckTrial(csv_array)
        error.error()
        return error.error_index, error.error_type
    
    class ReadTrial:
        def __init__(self, read_path):
            self.file_path = read_path
            self.names = header["TrialMeta"]
        
        def read(self):
            return pd.read_csv(self.file_path, names=self.names)
    
    class CheckTrial:
        def __init__(self, csv_array):
            self.csv_array = csv_array
            self.error_index = []
            self.error_type = error_type_dict["Normally"]

        def error(self):
            if self.csv_array.isnull().values.sum() != 0:
                for index, row in enumerate(self.csv_array.isnull().any(axis=1).values, start=1):
                    if row == True:
                        self.error_index.append(index)
                self.error_type = error_type_dict["NullValue"]
            else:
                pass

# ConcreteFactory
class CsvFactoryFileMeta(AbstructCsvFactory):
    def __init__(self):
        pass
    
    @classmethod
    def read_csv(cls, read_path):
        return cls.ReadTrial(read_path).read()
    
    @classmethod
    def check_csv(cls, csv_array):
        error = cls.CheckTrial(csv_array)
        error.error()
        return error.error_index, error.error_type

    class ReadTrial:
        def __init__(self, read_path):
            self.file_path = read_path
            self.names = header["FileMeta"]

        def read(self):
            return pd.read_csv(self.file_path, names=self.names)

    class CheckTrial:
        def __init__(self, csv_array):
            self.csv_array = csv_array
            self.error_index = []
            self.error_type = error_type_dict["Normally"]

        def error(self):
            if self.csv_array.isnull().values.sum() != 0:
                for index, row in enumerate(self.csv_array.isnull().any(axis=1).values, start=1):
                    if row == True:
                        self.error_index.append(index)
                self.error_type = error_type_dict["NullValue"]
            else:
                pass

def main():
    os.chdir("../../public/csv/dataset/20200908/")
    read_path = os.listdir()[0]
    factorytra = AbstructCsvFactory(CsvFactoryTrial(), read_path)
    factorytra.test_csv()

def csvtest(file_path):
    factorytra = AbstructCsvFactory(CsvFactoryTrial(), file_path)
    factorytra.test_csv()

if __name__ == "__main__":
    main()