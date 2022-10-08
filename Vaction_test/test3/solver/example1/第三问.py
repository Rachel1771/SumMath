import numpy
import xlrd

file_location = "C:/Users/95870/Desktop/数学建模代码/a.xlsx"
data = xlrd.open_workbook(file_location)
sheet = data.sheet_by_index(1)
sheet2=data.sheet_by_index(0)
data_d=[[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]

file_location = "C:/Users/95870/Desktop/数学建模代码/b.xlsx"
data = xlrd.open_workbook(file_location)
sheet = data.sheet_by_index(0)
data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

file = "C:/Users/95870/Desktop/数学建模代码/e.xlsx"
data1 = xlrd.open_workbook(file)
sheet1 = data1.sheet_by_index(0)
data3_d = [[sheet1.cell_value(r,c) for c in range(sheet1.ncols)] for r in range(sheet1.nrows)]
sheet2 = data1.sheet_by_index(1)
data3_g = [[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]

file_location = "C:/Users/95870/Desktop/数学建模代码/f.xlsx"
data3_y = xlrd.open_workbook(file_location)
sheet = data3_y.sheet_by_index(0)
data3_y = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

#订货量算总数(402家企业240周总供应量)
list2 = numpy.zeros((402,2))

for i in range(0,402):
    sum=0
    for j in range(0,240):
        sum=sum+data_d[i+1][j+2]
    list2[i][0]=sum
    list2[i][1]=i+1
    
 #订货量排名   
for i in range (0,402):#排序
    for j in range(0,401-i):
        if list2[j][0]<list2[j+1][0]:
            (list2[j][0],list2[j+1][0])=(list2[j+1][0],list2[j][0])
            (list2[j][1],list2[j+1][1])=(list2[j+1][1],list2[j][1])  
                      
num=0
sum=0
for i in range(0,50):
    a=int(list2[i][1])
    if data_d[a][1]=='A':
        sum=sum+list2[i][0]/0.6
        num=num+1
        print(list2[i][1])
        if (sum/240) >28200:
            print('$',num+1,list2[i][1])
            break
 
for i in range(0,50):
    a=int(list2[i][1])
    if data_d[a][1]=='B':
        sum=sum+list2[i][0]/0.66
        num=num+1
        print(list2[i][1])
        if (sum/240) >28200:
            print('$',num+1,list2[i][1])
            break
        
for i in range(0,50):
    a=int(list2[i][1])
    if data_d[a][1]=='C':
        sum=sum+list2[i][0]/0.72
        num=num+1
        print(list2[i][1])
        if (sum/240) >28200:
            print('$',num,list2[i][1])
            break


list = numpy.zeros((8,2))
for i in range(0,8):
    sum0=0
    sum=0
    for j in range (0,240):
        if data[i+1][j+1]==0 : 
           sum0=sum0+1
        else :
            sum=sum+data[i+1][j+1]     
    sum=sum/(240-sum0)
    list[i][0]=sum
    list[i][1]=i+1
for i in range (0,8):
    for j in range(0,7-i):
        if list[j][0]>list[j+1][0]:
            (list[j][0],list[j+1][0])=(list[j+1][0],list[j][0])
            (list[j][1],list[j+1][1])=(list[j+1][1],list[j][1])
            
            


for i in range(0,8):
    print(list[i][0],list[i][1])

        
#第三问的32家          1
list_1 = numpy.zeros((32,239,4))#第三和第四是每个的差值（有正负那种）
a=b=c=0
for i in range(0,32):
    for j in range(0,239):
        a=data3_g[i+1][j+2]-data3_d[i+1][j+2]
        b=data3_g[i+1][j+3]-data3_d[i+1][j+3]
        list_1[i][j][2]=a
        list_1[i][j][3]=b
        if a>=0:
            a=a
        else:
            a=-a
        if b>=0:
            b=b
        else:
            b=-b
        c=(a+b)/2
        list_1[i][j][0]=c  #差值（除法）
        list_1[i][j][1]=j+1#周数
        
for k in range(0,32):        
    for i in range (0,239):
        for j in range(0,238-i):
            if list_1[k][j][0]>list_1[k][j+1][0]:
                (list_1[k][j][0],list_1[k][j+1][0])=(list_1[k][j+1][0],list_1[k][j][0])
                (list_1[k][j][1],list_1[k][j+1][1])=(list_1[k][j+1][1],list_1[k][j][1])
                (list_1[k][j][2],list_1[k][j+1][2])=(list_1[k][j+1][2],list_1[k][j][2])
                (list_1[k][j][3],list_1[k][j+1][3])=(list_1[k][j+1][3],list_1[k][j][3])
        
        
 #第三问的        2     
list_2 = numpy.zeros((32,12,3))
for i in range(0,32):
    for j in range(0,12):
        list_2[i][j][0]=-2
    
    

for i in range(0,32):
    #k=12 
    k=0
    for flag in range(0,50):
    #for k in range(0,12):
        b=0
        for j in range (0,12):
            #if list1[i][12-k][1]==list2[i][j][0]+1:
            if list_1[i][flag][1]==list_2[i][j][0]+1 or list_1[i][flag][1]==list_2[i][j][0]-1:
                b=1
                break
        if b==0:
            list_2[i][k][0]=list_1[i][flag][1]
            list_2[i][k][1]=list_1[i][flag][2]
            list_2[i][k][2]=list_1[i][flag][3]
            
            
            #list2[i][12-k][0]=list1[i][12-k][1]
            k=k+1
        if k==12:
            break       
        
 #第三问的         3       
list_3 = numpy.zeros((32,24))

for i in range(0,32):
    a=b=c=0
    for j in range (0,12):
        a=list_2[i][j][0]
        b=a+1
        c=int(a+2)
        list_3[i][j*2]=data3_d[i+1][c]
        k=k+1
        c=int(b+2)
        list_3[i][j*2+1]=data3_d[i+1][c] 
       
        
#第三问的       4
a=0
list_4= numpy.zeros(24)
for i in range(0,24):#列
    sum=0
    for j in range(0,32):#行
        a = data3_y[j+1][i+2]
        sum=sum+a
    list_4[i]=sum        
        
        
#第三问的        5    
for i in range(0,24):
    b=list_4[i]//6000
    if list_4[i]%6000 != 0:
        b=b+1
        #print(b)
    #print(list_4[i]/(6000*b))          
        
        
        
        
        
        
      