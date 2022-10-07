import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sup = pd.read_csv('supplyer.csv')
sup
tsa = pd.read_csv('TSA_decided.csv')
tsa = tsa.drop('Unnamed: 0',axis=1)
tsa['mat'] = sup['材料分类']
tsa.set_index('mat',inplace=True)
tsa
tsa.loc['A'] = tsa.loc['A']/0.6
tsa.loc['B'] = tsa.loc['B']/0.66
tsa.loc['C'] = tsa.loc['C']/0.72

avg_sup = tsa.agg('sum')

avg_sup = np.array(avg_sup)
avg_sup
for i in range(23):
    avg_sup[i+1] = avg_sup[i+1] +avg_sup[i] 
    
avg_sup

pd.DataFrame(avg_sup).to_csv('bs.csv')
a_s = [i*1.5-2 for i in range(1,25)]
a_s[23] = 23*1.5
pd.DataFrame(a_s).to_csv('as.csv')

avg_need_eqC = (2.82*10**4)
'每周生产需求(eqC)：'+str((2.82*10**4))
avg_sup = tsa.agg('sum')

avg_sup
# hist_plot_cum = hist_calc.cumsum()
sup_cum_eqP = avg_sup.cumsum()
need_array_eqC = np.array([1.2*avg_need_eqC for i in range(24)])
need_cum_eqC = need_array_eqC.cumsum()

plt.figure(figsize=[30,4],dpi=200)
plt.xticks(range(1,25))

# sns.lineplot(x=range(1,25), y=need_cum_eqC, label='need_cum_eqC', color='darkred')
# plt.bar(x=range(1,25), height=hist_plot_cum-need_cum_eqC+2*avg_need_eqC, label='hist_plot', color='darkgray')
plt.bar(x=range(1,25), height=sup_cum_eqP-need_cum_eqC+2*avg_need_eqC, label='sup_cum_eqC', color='darkred')
# plt.bar(x=range(1,25), height=hist_plot_cum, label='hist_plot', color='darkgray')
# plt.bar(x=range(1,25), height=sup_cum_eqP, label='sup_cum_eqC', color='darkred')
sns.lineplot(x=range(1,25), y=2*avg_need_eqC, label='sup_cum_eqC', color='darkred')



plt.legend()
# plt.title('Need & Supply Barplot(cumulative)')
# plt.savefig('Need & Supply Barplot(cumulative).jpg')
supply = pd.read_csv('supplyer.csv')
tsa['mat'] = supply['材料分类'].values
tsa['id'] = np.arange(1,403)
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
aa_temp = np.array(aa_temp)
for i in range(23):
    aa_temp[i+1,:] = aa_temp[i,:]+aa_temp[i+1,:]
pd.DataFrame(aa_temp)
c_temp = np.array(tsa.drop('id', axis=1).loc['A']).flatten()*0.6*232.7
c_temp.shape
c_temp = np.append(c_temp, np.array(tsa.drop('id', axis=1).loc['B']).flatten()*0.66*221)
c_temp.shape
c_temp = np.append(c_temp, np.array(tsa.drop('id', axis=1).loc['C']).flatten()*0.72*209.3)
c_temp.shape
62.3-1500
ap = np.array([i-1 for i in range(24)]).reshape(24,1)
aa_temp.shape
aa_temp = np.hstack((aa_temp,ap))
x_df = pd.DataFrame(aa_temp)
x_df.to_csv('a3.csv')
x_df = pd.DataFrame(b)
x_df.to_csv('b3.csv')
x_df = pd.DataFrame(c_temp)
x_df.to_csv('c3.csv')

ratio = pd.read_csv('gap_ratio.csv')
ratio = np.array(ratio.drop('Unnamed: 0', axis=1))
a_2 = pd.read_csv('TSA_decided.csv')
a_2 = a_2.drop('Unnamed: 0', axis=1)

i=0
for col in a_2.columns:
    a_2[col] = np.array(a_2[col]*(1-ratio[i]))
    i+=1
a_2.to_csv('A_2.csv', index=False)