#!/bin/sh

cat train.txt

list=(`cat train_c.txt|xargs`)

for index in ${list[@]}
do
    python3 ./app/main/liner_regression.py ${index}
done