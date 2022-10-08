import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

pred_eqC = supply_eqC.drop(['供应商ID','材料分类'], axis=1).T

from fbprophet import Prophet
df = pd.read_csv('pred_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

pred_result = pd.DataFrame()
for col in pred_eqC.columns:
    print(col/402*100)
    y = pred_eqC[col].values
    df['y'] = y
    m = Prophet(
                yearly_seasonality=True
                )
    m.fit(df)
    future = m.make_future_dataframe(
                                    periods = 24,
                                    freq='W'
                                    )
    forecast = m.predict(future)
    result = forecast['yhat'][240:].values
    pred_result[col] = result
pred_result.to_csv('TSA_pred.csv')


df['y'] = pred_eqC[6].values
m = Prophet(yearly_seasonality=True)

m.fit(df)
future = m.make_future_dataframe(
                                periods = 24,
                                freq='W'
                                )

forecast = m.predict(future)
m.plot(forecast)

x = forecast['yhat'][240:].values


from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm


model = pm.auto_arima(df.y, start_p=1, start_q=1,
                    information_criterion='aic',
                    test='adf',       # use adftest to find optimal 'd'
                    max_p=4, max_q=4, # maximum p and q
                    m=24,              # frequency of series
                    d=None,           # let model determine 'd'
                    seasonal=True,   # No Seasonality
                    start_P=0, 
                    D=0, 
                    trace=True,
                    error_action='ignore',  
                    suppress_warnings=True, 
                    stepwise=True)

print(model.summary())

# Forecast
n_periods = 24
fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = np.arange(len(df.y), len(df.y)+n_periods)

# make series for plotting purpose
fc_series = pd.Series(fc, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.plot(df.y)
plt.plot(fc_series, color='darkgreen')
plt.fill_between(lower_series.index, 
                lower_series, 
                upper_series, 
                color='k', alpha=.15)

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
pred_result = pd.read_csv('TSA_decided.csv')
pred_result['id'] = pred_result['Unnamed: 0']+1

pred_result.set_index('id',inplace=True)
pred_result.drop('Unnamed: 0',axis=1, inplace=True)

pred_result
candidates = pd.read_csv('n_sup_decided.csv')
candidates['n_id'] = [int(x[1:]) for x in candidates['id'].values]
selected = candidates.loc[range(50)]
selected
selected.supply_amount.values.sum()/5
avg_need_eqC = (2.82*10**4)*0.72
'每周生产需求(eqC)：'+str((2.82*10**4)*0.72)
trans = pd.read_csv('trans.csv')
def replace0(x):
    if x == 0:
        return np.nan
    else:
        return x
    
notnull = 8*240 - trans.isnull().sum().sum()
avg_los = (trans.sum().values[1:].sum()/notnull)*0.01

'有运输时的平均货损率：'+str(avg_los)

selected_pred = pred_result.loc[selected['n_id'].values]
selected_pred
month_sup_50 = selected_pred.sum(axis=0)
month_sup_50.sum()
need_array_eqC = np.array([avg_need_eqC for i in range(24)])
plt.figure(figsize=[30,4])
plt.xticks(range(1,25))


plt.bar(x=range(1,25), height=month_sup_50, label='month_sup_50', color='darkred')
plt.bar(x=range(1,25), height=need_array_eqC, label='need_array_eqC', color='darkgray',alpha=0.7)

plt.legend()
plt.title('50 Need & Supply Barplot')
plt.savefig('50 Need & Supply Barplot.jpg')
selected_pred.sort_index(inplace=True)
selected_pred.to_csv('for_matlab.csv')
import numpy as np 
from scipy import optimize as op 
selected_pred = selected_pred.T

selected_pred
len(selected_pred)
selected_pred[3].sum()
for i in range(len(selected_pred)):
    if i<=22:
        selected_pred.iloc[i+1] = selected_pred.iloc[i+1] + selected_pred.iloc[i]
selected_pred
np.array(-selected_pred).shape
import cvxpy as cp

c = np.array([1 for i in range(50)])

a = np.array(selected_pred)

b = np.array([avg_need_eqC*i for i in range(1,25)])

x = cp.Variable(50,integer=True)

obj = cp.Minimize(c*x)

cons =[a*x>=b, x>=0, x<=1]

prob =cp.Problem(obj, cons)

prob.solve( solver='GLPK_MI', verbose=True)

print('opt_obj', prob.value)
print('opt_x', x.value)
selected_pred = selected_pred.T
selected_pred['opt_res'] = x.value
selected_pred
opt_res1_df = pd.DataFrame()
opt_res1_df['opt'] = x.value
opt_res1_df['id'] = selected_pred.index
opt_res1_df.to_csv('opt_res1_df.csv')
opt_res1_df
order_eqC = pd.read_csv('supply_eqC.csv')


order_eqC['id'] = [int(x[1:]) for x in order_eqC['供应商ID'].values]
selected_eqC = order_eqC.set_index('id').loc[opt_res1_df.id]
selected_eqC
selected_eqC = selected_eqC['材料分类']
selected_eqC
recat_selected = pd.concat([selected_eqC,pred_result.loc[opt_res1_df.id]], axis=1)
idx = recat_selected.index

recat_selected = recat_selected.set_index('材料分类')
recat_selected.loc['A'] = recat_selected.loc['A']/1.2
recat_selected.loc['B'] = recat_selected.loc['B']/1.091

recat_selected['id'] = idx
recat_selected
# recat_selected.to_csv('recat_selected_pred.csv')
n_selected = recat_selected.copy()
n_selected.loc['A'] = n_selected.loc['A']/0.6
n_selected.loc['B'] = n_selected.loc['B']/0.66
n_selected.loc['C'] = n_selected.loc['C']/0.72
n_selected['id'] = idx
n_selected['mat'] =n_selected.index
n_selected

n_selected['selected2'] = x.value
nn_selected = n_selected.set_index('selected2').loc[1]
nn_selected = nn_selected.set_index('mat')
nn_selected.sort_index(inplace=True)
nn_selected
nn_selected.to_csv('2_plan_data.csv')
a_temp = np.array(nn_selected.drop('id', axis=1)).T
a_temp.shape
len((list(a_temp[0,:]) + [0 for i in range(37*(23-0))]))
a_temp
aa_temp=[[0 for i in range(888)] for i in range(24)]
len(aa_temp[0])

for i in range(24):
    aa_temp[i] = (list(a_temp[i,:]) + [0 for i in range(37*(23-i))])
    aa_temp[i] = ([0 for i in range(37*(23-(23-i)))] + aa_temp[i])
len(aa_temp[0])
aaa_array = np.array(aa_temp)
aaa_array.shape
c_temp = np.array(nn_selected.drop('id', axis=1).loc['A']).flatten()*0.6*1.2
c_temp.shape
c_temp = np.append(c_temp, np.array(nn_selected.drop('id', axis=1).loc['B']).flatten()*0.66*1.1)
c_temp.shape
c_temp = np.append(c_temp, np.array(nn_selected.drop('id', axis=1).loc['C']).flatten()*0.72)
c_temp.shape
b = np.array([avg_need_eqC/0.72*1.01 for i in range(24)])
b
x_df = pd.DataFrame(aaa_array)
x_df.to_csv('a.csv')
x_df = pd.DataFrame(b)
x_df.to_csv('b.csv')
x_df = pd.DataFrame(c_temp)
x_df.to_csv('c.csv')
# c = c_temp

# a = aaa_array

# b = np.array([avg_need_eqC*1.01 for i in range(24)])

# x = cp.Variable(336,integer=True)

# obj = cp.Minimize(c*x)

# cons =[a*x>=b, 1>=x, x>=0]

# prob =cp.Problem(obj, cons)

# prob.solve( solver='GLPK_MI', verbose=True)

# print('opt_obj', prob.value)
# print('opt_x', x.value)
# x_df = pd.DataFrame(c)
# x_df.to_csv('for_matlab.csv')

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
res = pd.read_csv('2_oder_plan.csv')
res = np.array(res)
res.resize(24,37)
res = res.T
res = pd.DataFrame(res)
res
data = pd.read_csv('2_plan_data.csv')
data
res['id'] = data['id']
res.set_index('id', inplace=True)
res
sup14 = np.array(data.drop(['id','mat'], axis=1))
sup14.shape
supply_14 = res*sup14
supply_14.to_csv('supply14.csv')
supply_14
plot_sup = np.array(supply_14.sum(axis=0))


avg_need_eqC = (2.82*10**4)
'每周生产需求(eqC)：'+str((2.82*10**4))
need_array_eqC = np.array([avg_need_eqC for i in range(24)])

# plt.figure(figsize=[30,4])
# plt.xticks(range(1,25))

# plt.bar(x=range(1,25), height=need_array_eqC, label='need_eqC', color='darkgray')
# plt.bar(x=range(1,25), height=plot_sup, label='supply_eqC', color='darkred', alpha=0.6)

# plt.legend()
# plt.title('sup14')
# plt.savefig('sup14.jpg')
need_cum_eqC = need_array_eqC.cumsum()
sup_cum_eqC = plot_sup.cumsum()

plt.figure(figsize=[30,4],dpi=200)
plt.xticks(range(1,25))

# sns.lineplot(x=range(1,25), y=need_cum_eqC, label='need_cum_eqC', color='darkred')
plt.bar(x=range(1,25), height=sup_cum_eqC-need_cum_eqC+2*avg_need_eqC, label='sup_cum_eqC', color='darkred')
plt.legend()
# plt.title('Need & Supply Barplot(cumulative)')
# plt.savefig('Need & Supply Barplot(cumulative).jpg')
filler = pd.DataFrame(np.zeros([402,24]))
filler.set_index(np.arange(1,403))
for col in filler.columns:
    filler[col] = [np.nan for i in range(402)]
filler    

filler.loc[supply_14.index] = supply_14
filler.replace(0, np.nan,inplace = True)
filler.isnull().sum()


filler.to_csv('A_0.csv')

supply_14['mat'] = data['mat'].values
supply_14
calc_storage = supply_14.groupby('mat').agg('sum')
sup_eqP = calc_storage.loc['A']/0.6 + calc_storage.loc['B']/0.66 +calc_storage.loc['C']/0.72
sup_eqP
calc_price = supply_14.groupby('mat').agg('sum')
calc_price

calc_price = calc_price.sum(axis=1)
calc_price
opt_price = calc_price[0]*1.2 + calc_price[1]*1.1 + calc_price[2]
'预计未来订货费用：'+str(opt_price)
supply = pd.read_csv('supplyer.csv')
hist_price = np.array(supply.groupby('材料分类').agg('sum').sum(axis=1))
hist_price
hist_price = hist_price[0]*1.2 +hist_price[1]*1.1+hist_price[2]
hist_price
hist_calc = np.array(supply.groupby('材料分类').agg('sum'))
hist_calc.shape

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
plt.figure(dpi=200)
hist_plot_cum = hist_calc.cumsum()
sup_cum_eqP = sup_eqP.cumsum()
need_array_eqC = np.array([avg_need_eqC for i in range(24)])

plt.figure(figsize=[20,4])
plt.xticks(range(1,25))

# sns.lineplot(x=range(1,25), y=need_cum_eqC, label='need_cum_eqC', color='darkred')
plt.bar(x=range(1,25), height=hist_plot_cum-need_cum_eqC+2*avg_need_eqC, label='历史库存均值')
plt.bar(x=range(1,25), height=sup_cum_eqP-need_cum_eqC+2*avg_need_eqC, label='37家供应商计划订货库存', )
sns.lineplot(x=range(1,25), y=2*avg_need_eqC, label='安全库存线（2周产量）', color = 'red')
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('选定37家供应商后未来24周的库存与历史库存均值', fontsize = 20)

plt.legend(fontsize = 15)

plt.savefig('选定37家供应商后未来24周的库存与历史库存均值.jpg')

