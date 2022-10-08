import xlrd  
import numpy	
file_location = "C:/Users/95870/Desktop/数学建模代码/a.xlsx"
data = xlrd.open_workbook(file_location)
sheet = data.sheet_by_index(1)
sheet2=data.sheet_by_index(0)
data1 = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

file = "C:/Users/95870/Desktop/数学建模代码/c.xlsx"#37家供应商的表格
data2 = xlrd.open_workbook(file)
sheet1 = data2.sheet_by_index(0)
data_d = [[sheet1.cell_value(r,c) for c in range(sheet1.ncols)] for r in range(sheet1.nrows)]

sheet2 = data2.sheet_by_index(1)
data_g = [[sheet2.cell_value(r,c) for c in range(sheet2.ncols)] for r in range(sheet2.nrows)]


file_location = "C:/Users/95870/Desktop/数学建模代码/d.xlsx"#37家供应商的预计24周的供应量
data_y = xlrd.open_workbook(file_location)
sheet = data_y.sheet_by_index(0)
data_y = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]


#0.3%:240*28200*0.3%=20304(这个不是排名，是实际值)
list1 = numpy.zeros((402,2))#240周总共的
for i in range(0,402):
    sum=0
    for j in range(0,240):
        sum=sum+data1[i+1][j+2]
    list1[i][0]=sum
    list1[i][1]=i+1

for i in range (0,402):#排序
    for j in range(0,401-i):
        if list1[j][0]<list1[j+1][0]:
            (list1[j][0],list1[j+1][0])=(list1[j+1][0],list1[j][0])
            (list1[j][1],list1[j+1][1])=(list1[j+1][1],list1[j][1])
            
#0.3%:240*28200*0.3%=20304(这个不是排名，是实际值)               
qushu=0
for i in range (0,402):
    if list1[i][0]<20304:
        qushu=i+1
        break
    
print('选取',qushu,'家供应商')
for i in range(0,qushu):
    print(list1[i][1])    
    
    
    
#第二问的37家       1
list1 = numpy.zeros((37,239,4))#第三和第四是每个的差值（有正负那种）
a=b=c=0
for i in range(0,37):
    for j in range(0,239):
        a=data_g[i+1][j+2]-data_d[i+1][j+2]
        b=data_g[i+1][j+3]-data_d[i+1][j+3]
        list1[i][j][2]=a
        list1[i][j][3]=b
        if a>=0:
            a=a
        else:
            a=-a
        if b>=0:
            b=b
        else:
            b=-b
        c=(a+b)/2
        list1[i][j][0]=c  #差值（除法）
        list1[i][j][1]=j+1#周数
        
for k in range(0,37):        
    for i in range (0,239):
        for j in range(0,238-i):
            if list1[k][j][0]>list1[k][j+1][0]:
                (list1[k][j][0],list1[k][j+1][0])=(list1[k][j+1][0],list1[k][j][0])
                (list1[k][j][1],list1[k][j+1][1])=(list1[k][j+1][1],list1[k][j][1])
                (list1[k][j][2],list1[k][j+1][2])=(list1[k][j+1][2],list1[k][j][2])
                (list1[k][j][3],list1[k][j+1][3])=(list1[k][j+1][3],list1[k][j][3])
                
                
                
#24周的信息（供应商家数，周数，从哪儿挑出来的）第二问的       2
list2 = numpy.zeros((37,12,3))
for i in range(0,37):
    for j in range(0,12):
        list2[i][j][0]=-2
    
    

for i in range(0,37):
    #k=12 
    k=0
    for flag in range(0,50):
    #for k in range(0,12):
        b=0
        for j in range (0,12):
            #if list1[i][12-k][1]==list2[i][j][0]+1:
            if list1[i][flag][1]==list2[i][j][0]+1 or list1[i][flag][1]==list2[i][j][0]-1:
                b=1
                break
        if b==0:
            list2[i][k][0]=list1[i][flag][1]
            list2[i][k][1]=list1[i][flag][2]
            list2[i][k][2]=list1[i][flag][3]
            #list2[i][12-k][0]=list1[i][12-k][1]
            k=k+1
        if k==12:
            break                
                
                
                
 #第二问的        3
list3 = numpy.zeros((37,24))

for i in range(0,37):
    a=b=c=0
    for j in range (0,12):
        a=list2[i][j][0]
        b=a+1
        c=int(a+2)
        list3[i][j*2]=data_d[i+1][c]
        k=k+1
        c=int(b+2)
        list3[i][j*2+1]=data_d[i+1][c]               
    
            
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
                
                
#第二问的       4
a=0
list4= numpy.zeros(24)
for i in range(0,24):#列
    sum=0
    for j in range(0,37):#行
        a = data_y[j+1][i+2]
        sum=sum+a
    list4[i]=sum               
                
                

#第二问的       5

for i in range(0,24):
    b=list4[i]//6000
    if list4[i]%6000 != 0:
        b=b+1                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                