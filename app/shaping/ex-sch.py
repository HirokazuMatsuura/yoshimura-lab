import csv
import os

def txtfileCreation(array):
    path = './filename.txt'
    f = open(path, 'w')
    for element in array:
        f.write("%s\n" % element)
    f.close()

def getItems(array):
    items = list()
    items.append(array[1].replace(' ', ''))
    items.append(array[2].replace(' ', ''))
    items.append(array[8].replace(' ', ''))
    return items

def deleteNullRow(array):
    new = list()
    for index, element in enumerate(array, start=0):
        if (element[2] is not None) & (len(element[2]) > 0) & (index != 0):
            new.append(element)
    return new

if __name__ == "__main__":
    with open('./ExperimentalSchedule1.csv') as f:
        reader = csv.reader(f)
        table = list()
        for index, row in enumerate(reader, start=0):
            table.append(getItems(row))
        table = deleteNullRow(table)
    txtfileCreation(table)

    with open('out.csv', 'w', encoding='utf-8', newline='') as f:
        dataWriter = csv.writer(f)
        for row in table:
            dataWriter.writerow(row)