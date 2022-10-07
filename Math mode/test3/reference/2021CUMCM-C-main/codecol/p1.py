import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
n_sup = pd.DataFrame()
n_sup['id'] = supply_eqC['供应商ID']
n_sup['supply_amount'] = supply_eqC.drop(['供应商ID','材料分类'], axis=1).sum(axis=1)
n_sup['avg_gap'] = gap.T.sum(axis=1).values/n_sup['supply_amount']

non_zero_count = []
for col in order_eqC.T.columns:
    array = np.array(order_eqC.T[col])
    zeros = np.zeros(len(array))
    not_zero = zeros!=array
    non_zero_count.append(not_zero.sum()-2)
supply_zero_count = []
for col in supply_eqC.T.columns:
    array = np.array(supply_eqC.T[col])
    zeros = np.zeros(len(array))
    is_zero = zeros==array
    supply_zero_count.append(is_zero.sum())
cnt=0
var = []
for col in supply_eqC.T.columns:
    array = np.array(supply_eqC.T[col])[2:]
    avg = array/non_zero_count[cnt]
    var.append(sum((array-avg)**3)/non_zero_count[cnt])
    # var.append(sum((array-avg))/non_zero_count[cnt])
    cnt += 1

n_sup['annul_var'] = var
n_sup['supply_zero_count'] =supply_zero_count
n_sup.to_csv('supply_features.csv', index=False)
import sklearn
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
x_train = n_sup.drop('id', axis=1)
sc = StandardScaler()
x_train_std = sc.fit_transform(x_train)
cov_matrix = np.cov(x_train_std.T)
eigen_val, eigen_vec = np.linalg.eig(cov_matrix)
eigen_val
plt.style.use('ggplot')
plt.figure(dpi = 200, figsize =[9,5] )

var_ratio = sorted(eigen_val/(eigen_val.sum()), reverse=True)
cum_var_ratio = np.cumsum(var_ratio)
plt.step(x = range(1,5), y = cum_var_ratio,
        label = '累计方差解释率')
plt.bar(x = range(1,5), height = var_ratio, color='darkcyan' ,
        label = '方差解释率')
plt.xticks([1,2,3,4], fontsize=10) 
plt.yticks(np.arange(0,1.1,0.1), fontsize=10)   

plt.title('主成分方差解释率',fontsize = 20)
plt.legend(loc = 'right',fontsize=15)
plt.savefig('主成分方差解释率.jpg')

eigen_pairs = [(np.abs(eigen_val[i]), 
                eigen_vec[:,i]) for i in range(len(eigen_val))]

eigen_pairs.sort(key=lambda k:k[0], reverse=True)
w = np.c_[eigen_pairs[0][1],eigen_pairs[1][1]]

x_train_pca = x_train_std.dot(w)

n_sup['pc'] = (x_train_pca[:,0]*var_ratio[0] + x_train_pca[:,1]*var_ratio[1])/(var_ratio[0]+var_ratio[1])
n_sup = n_sup.set_index('pc').sort_index()
n_sup.to_csv('n_sup.csv')