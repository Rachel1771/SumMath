# -*- coding: utf-8 -*-
import numpy
import xlrd

file_location = "C:/Users/95870/Desktop/数学建模代码/a.xlsx"
data = xlrd.open_workbook(file_location)
sheet = data.sheet_by_index(1)
sheet2=data.sheet_by_index(0)
data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
data1 = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
data_d=[[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]


list3 = numpy.zeros((240,3)) #分类看歌类每周的总值

for j in range(0,240):
    sum=0
    for i in range(0,402):
        if data1[i+1][1]=='A':
            sum=sum+data_d[i+1][j+2]
    list3[j][0]=sum

for j in range(0,240):
    sum=0
    for i in range(0,402):
        if data1[i+1][1]=='B':
            sum=sum+data_d[i+1][j+2]
    list3[j][1]=sum
        

for j in range(0,240):
    sum=0
    for i in range(0,402):
        if data1[i+1][1]=='C':
            sum=sum+data_d[i+1][j+2]
    list3[j][2]=sum

for i in range(1,6):
    sumA=sumB=sumC=0
    print(i)
    for j in range((i-1)*48,i*48) :
        sumA=sumA+list3[j][0]
        sumB=sumB+list3[j][1]
        sumC=sumC+list3[j][2]
    sumA=sumA/48
    sumB=sumB/48
    sumC=sumC/48
    print(sumA)
    print(sumB)
    print(sumC)
    print(sumA/0.6+sumB/0.66+sumC/0.72) 



    
    
file_location = "C:/Users/95870/Desktop/数学建模代码/a.xlsx"
data4 = xlrd.open_workbook(file_location)
sheet = data4.sheet_by_index(1)
sheet2=data4.sheet_by_index(0)
data4_g = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
data4_d=[[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]

file_location = "C:/Users/95870/Desktop/数学建模代码/g.xlsx"
data4_y = xlrd.open_workbook(file_location)
sheet = data4_y.sheet_by_index(0)
data4_y = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    
#第四问的402家       1                
list4_1 = numpy.zeros((402,239,4))#第三和第四是每个的差值（有正负那种）
a=b=c=0
for i in range(0,402):
    for j in range(0,239):
        a=data4_g[i+1][j+2]-data4_d[i+1][j+2]
        b=data4_g[i+1][j+3]-data4_d[i+1][j+3]
        list4_1[i][j][2]=a
        list4_1[i][j][3]=b
        if a>=0:
            a=a
        else:
            a=-a
        if b>=0:
            b=b
        else:
            b=-b
        c=(a+b)/2
        list4_1[i][j][0]=c  #差值（除法）
        list4_1[i][j][1]=j+1#周数
        
for k in range(0,402):        
    for i in range (0,239):
        for j in range(0,238-i):
            if list4_1[k][j][0]>list4_1[k][j+1][0]:
                (list4_1[k][j][0],list4_1[k][j+1][0])=(list4_1[k][j+1][0],list4_1[k][j][0])
                (list4_1[k][j][1],list4_1[k][j+1][1])=(list4_1[k][j+1][1],list4_1[k][j][1])
                (list4_1[k][j][2],list4_1[k][j+1][2])=(list4_1[k][j+1][2],list4_1[k][j][2])
                (list4_1[k][j][3],list4_1[k][j+1][3])=(list4_1[k][j+1][3],list4_1[k][j][3])   
                
                
                
 #第四问的        2      
list4_2 = numpy.zeros((402,12,3))
for i in range(0,402):
    for j in range(0,12):
        list4_2[i][j][0]=-2
    
    

for i in range(0,402):
    #k=12 
    k=0
    for flag in range(0,50):
    #for k in range(0,12):
        b=0
        for j in range (0,12):
            #if list1[i][12-k][1]==list2[i][j][0]+1:
            if list4_1[i][flag][1]==list4_2[i][j][0]+1 or list4_1[i][flag][1]==list4_2[i][j][0]-1:
                b=1
                break
        if b==0:
            list4_2[i][k][0]=list4_1[i][flag][1]
            list4_2[i][k][1]=list4_1[i][flag][2]
            list4_2[i][k][2]=list4_1[i][flag][3]
            #print(list4_2[i][k][0])
            
            #list2[i][12-k][0]=list1[i][12-k][1]
            k=k+1
        if k==12:
            break


#第四问的         3 
list4_3 = numpy.zeros((402,24))

for i in range(0,402):
    a=b=c=0
    for j in range (0,12):
        a=list4_2[i][j][0]
        b=a+1
        c=int(a+2)
        #print(c)
        list4_3[i][j*2]=data4_d[i+1][c]
        k=k+1
        c=int(b+2)
        #print(c)
        list4_3[i][j*2+1]=data4_d[i+1][c]
        
        
        
        
#第四问的        4
a=0
list4_4= numpy.zeros(24)
for i in range(0,24):#列
    sum=0
    for j in range(0,402):#行
        a = data4_y[j+1][i+2]
        sum=sum+a
    list4_4[i]=sum    
    
    
for i in range(0,24):
    b=list4_4[i]//6000
    if list4_4[i]%6000 != 0:
        b=b+1
        print(b,end="   ")
    print(list4_4[i]/(6000*b))      
    
    