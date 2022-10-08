import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
avg_need_eqC = (2.82*10**4)
'每周生产需求(eqC)：'+str((2.82*10**4))
tsa = pd.read_csv('TSA_decided.csv')
tsa['id'] = range(1,403)
tsa.drop('Unnamed: 0', axis=1, inplace=True)
tsa
supply = pd.read_csv('supplyer.csv')
tsa['mat'] = supply['材料分类']
tsa
tsa.set_index('mat', inplace=True)
tsa.sort_index(inplace=True)
idx = tsa.id
tsa
tsa.loc['A'] = tsa.loc['A']/1.2/0.6
tsa.loc['B'] = tsa.loc['B']/1.091/0.66
tsa.loc['C'] = tsa.loc['C']/0.72
tsa['id'] = idx
tsa
a_temp = np.array(tsa.drop('id', axis=1)).T
a_temp.shape
aa_temp=[[0 for i in range(9648)] for i in range(24)]


for i in range(24):
    aa_temp[i] = (list(a_temp[i,:]) + [0 for i in range(402*(23-i))])
    aa_temp[i] = ([0 for i in range(402*(23-(23-i)))] + aa_temp[i])
len(aa_temp[0])
aaa_array = np.array(aa_temp)
aaa_array.shape
c_temp = np.array(tsa.drop('id', axis=1).loc['A']).flatten()*0.6*95.4/0.4
c_temp.shape
c_temp = np.append(c_temp, np.array(tsa.drop('id', axis=1).loc['B']).flatten()*0.66*90.6/0.4)
c_temp.shape
c_temp = np.append(c_temp, np.array(tsa.drop('id', axis=1).loc['C']).flatten()*0.72*85.8/0.4)
c_temp.shape
b = np.array([avg_need_eqC*1.01 for i in range(24)])
x_df = pd.DataFrame(aaa_array)
x_df.to_csv('a1.csv')
x_df = pd.DataFrame(b)
x_df.to_csv('b1.csv')
x_df = pd.DataFrame(c_temp)
x_df.to_csv('c1.csv')
res = pd.read_csv('3_oder_plan.csv')
res = np.array(res)
res = res.reshape(24,402)
res = res.T
res = pd.DataFrame(res)
res
res['id'] = tsa['id'].values
res.set_index('id', inplace=True)
res
temp = np.array(tsa.drop('id', axis=1))
sup402 = res*temp
sup402['mat'] = tsa.index
sup402
sup_save = sup402.copy()
sup_save.sort_index(inplace=True)
sup_save.replace(0,np.nan,inplace=True)
sup_save.to_csv('A_1.csv')
agg = sup402.groupby('mat').agg('sum')
agg = agg.sum(axis=1)
agg
agg1 = tsa.groupby('mat').agg('sum')
agg1 = agg1.sum(axis=1)
agg1
opt_price = agg[0]*(57.6+9.8)+agg[1]*(52.8+9.8)+agg[2]*(48+9.8)
'单价和运费',opt_price
eqP = sup402.set_index('mat')
eqP.loc['A'] = eqP.loc['A']/0.6
eqP.loc['B'] = eqP.loc['B']/0.66
eqP.loc['C'] = eqP.loc['C']/0.72
eqP = eqP.sum(axis=0)
eqP 
supply = pd.read_csv('supplyer.csv')
hist_price = np.array(supply.groupby('材料分类').agg('sum').sum(axis=1))
hist_price
hist_price = hist_price[0]*(57.6+9.8) +hist_price[1]*(52.8+9.8)+hist_price[2]*(48+9.8)
hist_price = hist_price*0.1
hist_price
hist_calc = np.array(supply.groupby('材料分类').agg('sum'))
hist_calc[0,:] = hist_calc[0,:]/0.6
hist_calc[1,:] = hist_calc[1,:]/0.66
hist_calc[1,:] = hist_calc[1,:]/0.72
hist_calc.shape
hist_calc = hist_calc.sum(axis=0)

hist_calc.shape
hist_calc = np.array(hist_calc.reshape(10,24))
hist_calc = [hist_calc[:,i].mean() for i in range(24)]
hist_calc = np.array(hist_calc)
plt.style.use('ggplot')

hist_plot_cum = hist_calc.cumsum()
sup_cum_eqP = eqP.cumsum()
need_array_eqC = np.array([avg_need_eqC for i in range(24)])
need_cum_eqC = need_array_eqC.cumsum()

plt.figure(figsize=[20,4],dpi=200)
plt.xticks(range(1,25))
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
# sns.lineplot(x=range(1,25), y=need_cum_eqC, label='need_cum_eqC', color='darkred')
plt.bar(x=range(1,25), height=hist_plot_cum-need_cum_eqC+2*avg_need_eqC, label='历史库存均值')
plt.bar(x=range(1,25), height=sup_cum_eqP-need_cum_eqC+2*avg_need_eqC, label='订货计划库存')
# plt.bar(x=range(1,25), height=hist_plot_cum, label='hist_plot', color='darkgray')
# plt.bar(x=range(1,25), height=sup_cum_eqP, label='sup_cum_eqC', color='darkred')
sns.lineplot(x=range(1,25), y=2*avg_need_eqC, label='安全库存线（2周产量）', color='red')



plt.legend(fontsize=15)
plt.title('成本最低订货计划未来24周的库存与历史库存均值',fontsize=20)
plt.savefig('成本最低订货计划未来24周的库存与历史库存均值.jpg')
opt_storage = np.array(sup_cum_eqP-need_cum_eqC+2*avg_need_eqC)
hist_storage = np.array(hist_plot_cum-need_cum_eqC+2*avg_need_eqC)
hist_storage_price = 0
opt_storage_price = 0
for i in range(len(opt_storage)):
    if opt_storage[i]>0:
        opt_storage_price+=opt_storage[i]*28
    if hist_storage[i]>0:
        hist_storage_price+=hist_storage[i]*28
print('优化总价：',opt_storage_price+opt_price)
print('历史均价：',hist_storage_price+hist_price)
    
opt_storage_price
hist_storage_price
sup_cum_eqP
res = res.sort_index()
res
temp = np.array(tsa.drop('id', axis=1))
sup402 = res*temp
sup402
order_pred = pred*np.array(res)
smaller_than_sup = order_pred<sup402
smaller_than_sup
order_pred.shape
for col in smaller_than_sup.columns:
    array =  np.array(smaller_than_sup[col])
    for i in range(len(array)):
        if array[i]==True:
            order_pred[i,col] = np.array(sup402)[i,col]
order_pred
a_1 = order_pred*res
a_1.to_csv('A_1x.csv')  