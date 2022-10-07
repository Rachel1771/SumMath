import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
sup = pd.read_csv('supplyer.csv')
sup.columns
sup_weeks_sum = sup.drop(['供应商ID', '材料分类'], axis=1).agg('sum')
sup_weeks_sum
plt.figure(figsize=[30,4])
plt.xticks(range(1,242,4))
plt.plot(range(1,241), sup_weeks_sum)

order = pd.read_csv('orders.csv')
order.columns
ord_weeks_sum = order.drop(['供应商ID', '材料分类'], axis=1).agg('sum')
ord_weeks_sum
plt.figure(figsize=[30,4],dpi=200)
plt.style.use('ggplot')
plt.xticks(range(1,242,4),fontsize=10)
plt.title('历史订货供货量', fontsize=20)
plt.plot(range(1,241), sup_weeks_sum, label='supply')
plt.plot(range(1,241), ord_weeks_sum, label='order')
# plt.bar(range(1,241), sup_weeks_sum, label='supply')
# plt.bar(range(1,241), ord_weeks_sum, label='order')
plt.legend(fontsize=15)
plt.savefig('历史订货供货量.jpg')
sup_agg_cat = sup.drop('供应商ID', axis=1).groupby('材料分类').agg('sum')
sup_agg_cat = sup_agg_cat.T
plt.figure(figsize=[30,4])
sns.lineplot(data=sup_agg_cat)
sns.heatmap(sup_agg_cat[['A','B','C']].corr(), cmap='rainbow')
(np.cov(sup_agg_cat['A'],sup_agg_cat['C'])[0,1],
np.cov(sup_agg_cat['A'],sup_agg_cat['B'])[0,1],
np.cov(sup_agg_cat['B'],sup_agg_cat['C'])[0,1])
ord_agg_cat = order.drop('供应商ID', axis=1).groupby('材料分类').agg('sum')
ord_agg_cat = ord_agg_cat.T
plt.figure(figsize=[30,4])
sns.lineplot(data=ord_agg_cat)
plt.savefig('ord_agg_cat.jpg')
ord_agg_cat.columns = ['orderA', 'orderB', 'orderC']
sup_agg_cat.columns = ['supplyA', 'supplyB', 'supplyC']
n_df = pd.concat([ord_agg_cat, sup_agg_cat], axis=1)
n_df
sns.pairplot(n_df)
plt.savefig('pair.jpg')
order = pd.read_csv('orders.csv')
sup = pd.read_csv('supplyer.csv')
order = order.drop([402,403], axis=0)
order
gap = sup.drop(['供应商ID', '材料分类'], axis=1)-order.drop(['供应商ID', '材料分类'], axis=1)
gap =gap.T
gap
gap_array = np.array(gap.sum(axis=1)).reshape(10,24).sum(axis=0)
plt.figure(figsize=[30,4])
plt.bar(x=range(24), height=np.array(gap.sum(axis=1)).reshape(10,24).sum(axis=0))
sup_week = np.array(sup.drop(['供应商ID', '材料分类'], axis=1).agg('sum'))
sup_week = sup_week.reshape(10,24).sum(axis=0)
sup_week
ratio = gap_array/sup_week
pd.DataFrame(ratio).to_csv('gap_ratio.csv')
a_1 = pd.read_csv('A_1.csv')

a_1 = a_1.drop(['mat','id'], axis=1)
a_1
i=0
for col in a_1.columns:
    a_1[col] = np.array(a_1[col]*(1-ratio[i]))
    i+=1
a_1.to_csv('A_1.csv', index=False)
binned_gap = gap.copy()
def binned(lis):
    return [-1 if x<0 else 0 for x in lis]
for col in binned_gap.columns:
    collis = binned_gap[col].values
    binned_gap[col] = binned(collis)
sns.distplot(binned_gap)

gap_ratio = gap / order.drop(['供应商ID', '材料分类'], axis=1).T

sns.distplot(gap_ratio)
ord_agg_cat
cat_sum = ord_agg_cat.agg('sum')
plt.bar(x=['A','B','C'],height=cat_sum.values/240,color=['darkcyan','darkblue','gray'])
plt.title('History Orders Count')
plt.savefig('History Orders Count.jpg')

sup_sum = sup_agg_cat.agg('sum')
plt.bar(x=['A','B','C'],height=sup_sum.values/240,color=['darkcyan','darkblue','gray'])
plt.title('History Supply Count')
plt.savefig('History Supply Count.jpg')
plt.style.use('ggplot')
plt.figure(dpi = 200, figsize =[9,5] )
x_index = np.arange(3)   #柱的索引
x_data = ('A', 'B', 'C')
y1_data = cat_sum.values/240
y2_data = sup_sum.values/240
bar_width = 0.2  #定义一个数字代表每个独立柱的宽度
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
rects1 = plt.bar(x_index, y1_data, width=bar_width ,label='订单量')            #参数：左偏移、高度、柱宽、透明度、颜色、图例
rects2 = plt.bar(x_index + bar_width, y2_data, width=bar_width,label='供货量') #参数：左偏移、高度、柱宽、透明度、颜色、图例
plt.yticks(fontsize=10)   
plt.xticks(x_index + bar_width/2, x_data, fontsize=15)   
plt.legend()    
plt.title('历史周均订单量和供货量', fontsize = 20)
plt.tight_layout()  

plt.savefig('历史周均订单量和供货量.jpg')
plt.figure(figsize=[30,4])
plt.title('Gap-Time Curve')
sns.lineplot(x=range(240), y=abs(gap.T.sum()))
plt.savefig('Gap-Time Curve.jpg')
order_eqC = order.T
for col in order_eqC.columns:
    colu = order_eqC[col]
    cat = colu[1]
    if cat == 'A':
        order_eqC[col][2:] = colu[2:]*1.2
    elif cat == 'B':
        order_eqC[col][2:] = colu[2:]*1.091

order_eqC = order_eqC.T
order_eqC.to_csv('order_eqC.csv', index=False)
order_eqC.head()
supply_eqC = sup.T
for col in supply_eqC.columns:
    colu = supply_eqC[col]
    cat = colu[1]
    if cat == 'A':
        supply_eqC[col][2:] = colu[2:]*1.2
    elif cat == 'B':
        supply_eqC[col][2:] = colu[2:]*1.091

supply_eqC = supply_eqC.T
supply_eqC.to_csv('supply_eqC.csv', index=False)
supply_eqC.head()

avg_need_eqC = (2.82*10**4)*0.72

trans = pd.read_csv('trans.csv')
def replace0(x):
    if x == 0:
        return np.nan
    else:
        return x
    
notnull = 8*240 - trans.isnull().sum().sum()
avg_los = (trans.sum().values[1:].sum()/notnull)*0.01



plt.style.use('ggplot')
plt.figure(dpi=200)
need_array_eqC = np.array([avg_need_eqC for i in range(240)])
supply_eqC = pd.read_csv('supply_eqC.csv')
sup_weeks_sum_eqC = supply_eqC.drop(['供应商ID', '材料分类'], axis=1).agg('sum')
sup_weeks_sum_eqC = np.array(sup_weeks_sum_eqC.values*(1-avg_los))
plt.figure(figsize=[30,4])
plt.xticks(range(1,242,4),fontsize=10)

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.yticks(fontsize=10)   
plt.title('历史供求关系', fontsize = 20)
plt.bar(x=range(1,241), height=need_array_eqC, label='生产需求')
plt.bar(x=range(1,241), height=sup_weeks_sum_eqC, label='供货量')

plt.legend(fontsize = 15)

plt.savefig('历史供求关系.jpg')
plt.style.use('ggplot')
need_cum_eqC = need_array_eqC.cumsum()
sup_cum_eqC = sup_weeks_sum_eqC.cumsum()

plt.figure(figsize=[30,4],dpi=200)
plt.xticks(range(1,242,4))

plt.plot(range(1,241), need_cum_eqC,  label='累计生产需求')
plt.bar(x=range(1,241), height=sup_cum_eqC, color='gray',label='累计供货量')
plt.legend(fontsize=15)
plt.title('历史累计供求关系', fontsize=20)
plt.savefig('历史累计供求关系.jpg')
storage_eqC = sup_cum_eqC - need_cum_eqC + 2*avg_need_eqC

plt.figure(figsize=[30,4],dpi=200)
plt.xticks(range(1,242,4))
plt.bar(x=range(1,241), height=storage_eqC, label='storage_eqC', color='darkred')
plt.legend()
plt.title('storage_eqC')
plt.savefig('storage_eqC.jpg')
reshape_storage = storage_eqC.reshape(5,48)
annual_storage = [reshape_storage[:,i] for i in range(48)]

avg_annual_storage = [sum(i)/5 for i in annual_storage]



avg_annual_storage = np.array(avg_annual_storage)
avg_annual_storage += avg_need_eqC*2

plt.figure(figsize=[30,4],dpi=200)
plt.xticks(range(1,49))
plt.bar(x=range(1,49), height=avg_annual_storage, label='avg_annual_storage', color='darkred')
plt.legend()
plt.title('avg_annual_storage')
plt.savefig('avg_annual_storage.jpg')