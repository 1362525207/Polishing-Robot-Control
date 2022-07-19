#!/usr/bin/env python
# -*- coding: utf-8 -*-

def loadData(fileName):
    inFile = open(fileName, 'r')
    #以只读方式打开某filename文件,该py文件是为了进行nurbs仿真测试的
    #定义2个空的list，用来存放文件中的数据
    gyrox = []
    gyroy = []
    gyroz = []
    gyroa = []
    gyrob = []
    for line in inFile:
        trainingSet = line.split('\t')#对于上面数据每一行，按' '把数据分开，这里是分成两部分
        gyrox.append(float(trainingSet[0]))#第五部分，即文件中的第五列数据逐一添加到list gyrox中
        gyroy.append(float(trainingSet[1]))#第六部分，即文件中的第六列数据逐一添加到list gyroy中
        gyroz.append(float(trainingSet[2]))#第七部分，即文件中的第七列数据逐一添加到list gyroz中
        gyroa.append(float(trainingSet[3]))#第六部分，即文件中的第六列数据逐一添加到list gyroy中
        gyrob.append(float(trainingSet[4]))#第七部分，即文件中的第七列数据逐一添加到list gyroz中
    inFile.close()
    return ( gyrox, gyroy, gyroz, gyroa, gyrob)

file = "/home/mhq/mingurdf2/src/nurbs/sum.txt"
f = loadData(file)
print(f[0][2])
