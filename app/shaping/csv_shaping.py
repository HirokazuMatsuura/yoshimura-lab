# the rule of naming
# class TestTest()
# method testTest()
# function test_test()
# varianle test_test
# const TEST_TEST

import os
import sys
import csv
import numpy as np
from numpy import linalg as LA

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

def file_path_list():
    path = "./drive-download-20210407T140606Z-001/"
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

def remake_csvfile(filenames):
    remake = list()
    remake_path = list()
    for each in filenames:
        with open(each.path_name) as f:
            reader = csv.reader(f)
            length = 0
            for row in reader:
                length = len(row)
                break
            if length == 10:
                remake_path.append(each.path_name)
                part = list()
                for row in reader:
                    row[4:4] = ['0', '0', '0']
                    part.append(row)
                remake.append(part)
    for index, path in enumerate(remake_path, start=0):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(remake[index])

if __name__ == "__main__":
    trial_list = list()
    pathlist = file_path_list()
    csv_info = get_all_file_paths(pathlist)
    remake_csvfile(csv_info)
