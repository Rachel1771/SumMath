# -*- coding: utf-8 -*-
import xlrd  	
file_location = "C:/Users/95870/Desktop/数学建模代码/a.xlsx"
data = xlrd.open_workbook(file_location)

sheet = data.sheet_by_index(1)
sheet2=data.sheet_by_index(0)



data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

#二维数组
import numpy
num_list = numpy.zeros((402,240))
for i in range(0,402):
    for j in range(0,240):
        num_list[i][j] = i+1



for k in range (240):
    for i in range (0,402):
        for j in range(0,401-i):
            if data[j+1][k+2]<data[j+2][k+2]:
                (data[j+1][k+2],data[j+2][k+2])=(data[j+2][k+2],data[j+1][k+2])
                (num_list[j][k],num_list[j+1][k])=(num_list[j+1][k],num_list[j][k])
    

#排名相同的同一个排名

y = numpy.zeros((402,240))
for i in range (0,240):
    a=1
    y[0][i]=1
    n=1
    for j in range(0,401):        
        if data[j+1][i+2]==data[j+2][i+2]:
            y[j+1][i]=y[j][i]
            n=n+1
        else :
            y[j+1][i]=a+n
            a=a+n
            n=1
            
list = numpy.zeros((402,2)) 
for k in range(1,403):
    sum=0.0 
    for i in range(0,402):
        for j in range (0,240):
            if num_list[i][j]==k:
               sum=sum+y[i][j]
    sum=sum/240        
    list[k-1][0]=sum
    list[k-1][1]=k

   
    
# 排序给出那50个（平均下来每周的）   
for i in range (0,402):
    for j in range(0,401-i):
        if list[j][0]>list[j+1][0]:
            (list[j][0],list[j+1][0])=(list[j+1][0],list[j][0])
            (list[j][1],list[j+1][1])=(list[j+1][1],list[j][1])
            
            
            
for i in range(0,50):
    print(list[i][1])