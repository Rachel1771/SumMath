

# 第一题

Goods ： 订货量和生产产品数

$W_i$：产品种类对应的每立方米产品需消耗对应种类的原材料 





$Goods_{i}$为Goods中第i个供货商（订货商）对应每一周的供货量
$$
Goods\_wight_{ij} = \frac{Goods_{ij}}{W_{ij}}
$$


计算各订货量$D_{i}$ 与供货商生产的产品数$S_i$的比率$R_{i}$：
$$
R_{i} = \frac{D_{i}}{S_{i}}
$$
$Goods_{i_{std}}$为$Goods\_wight_{i}$第i个供货商（订货商）对应的第j周的供货量的标准差。

$Goods_{i_{mean}}$为$Goods\_wight_{i}$中第i个供货商（订货商）对应的第j周的供货量的均值。

$Goods\_{cv}_{i_{mean}}$即为第i个供货商（订货商）对应的第j周的变异系数，公式定义如下
$$
Goods\_{cv}_{i_{mean}} =\frac{Goods_{i_{std}}}{Goods_{i_{mean}}}
$$


$Goods\_stab_{i}$为第i个供货商（订货商）对应的每一周的稳定指数：
$$
Goods\_stab_{i} = \frac{1}{Goods\_{cv}_{i_{mean}}+1}
$$


$Goods\_diff_{i}$为第i个供货商（订货商）对应的每一周的偏移指数：
$$
Goods\_diff = Goods\_stab\_sup_{i} - Goods\_stab\_ord_{i}
$$
$diff\_metric$为订货的稳定指数，
$$
diff\_metric =\frac{1}{\frac{\sum^{i}_{n=0}(\frac{Goods\_diff_{n}}{Goods\_diff_{n}})^2}{i}+1}
$$


$vacancy\_rate$供货商占有率，$data\_orger_{ij}$为供货商i第j周的供货数，$time_{total}$为总周数。
$$
order\_bool_{ij}=\left\{\begin{array}{llcl}

		True & data\_order_{ij}=0\\
		False & data\_order_{ij}\neq0

	\end{array} \right.
$$

$$
data\_order\_IdleI_i=\frac{\sum_{n=0}^j order\_bool_{in}}{time_{total}}
$$


$$
vacancy\_rate_i = 1-data\_order\_Idle_i
$$

$Default\_rate$供应商违约率,$Compliance\_{rate}$供应商守约率
$$
data\_order\_bool_{ij} =\left\{\begin{array}{llcl}

		True & data\_order_{ij}>0\\
		False & data\_order_{ij}\leq 0

	\end{array} \right.
$$


$$
data\_supply\_bool_{ij} =\left\{\begin{array}{llcl}

		True & data\_supply_{ij}=0\\
		False & data\_supply_{ij}\neq 0

	\end{array} \right.
$$

$$
data\_bool2_{ij} = =\left\{\begin{array}{llcl}

		True & data\_order\_bool_{ij}\&data\_supply\_bool_{ij}==True\\
		False & data\_order\_bool_{ij}\&data\_supply\_bool_{ij}==False

	\end{array} \right.
$$


$$
data\_order2\_bool_{ij} =\left\{\begin{array}{llcl}

		True & data\_order_{ij}\neq0\\
		False & data\_order_{ij}= 0

	\end{array} \right.
$$

$$
Default\_rate_i = \frac{\sum_{n=0}^i{data\_bool_{in}}}{\sum^i_{m=0}data\_order2\_bool_{im}}
$$

$$
Compliance\_{rate} = 1- Default\_rate
$$



$important\_freq$重要订单接收频次，其中$important\_freq$被初始化为全0的矩阵。
$$
max\_order_{i} =\{data\_order_{ij}|data\_order_{ij}∈argsort(data\_order_{ij}) \wedge 0\leq j\leq20\}
$$

$$
important\_freq_{i} =important\_freq_{ij} +1
\\
s.t.\ max\_order_{ij} ∈ max\_order_{i}
$$


segmentation_market_share为供应商i对应的市场份额，$market\_weight_t$为$data\_supply_i$对应材料分类的总市场份额：


$$
market\_weight_t = \sum_{n=0}^{i} data\_supple_{nt}
$$

$$
segmentation\_market\_share_i =  \frac{data\_supply_i}{market\_weight_t}
$$
n_components设为 ‘mle’ ，svd_solver 设为 ‘full’, 则使用Minka’s MLE方法来估计降维后特征的维度



# 第二题



$omega\_average_i$为第i个装运商的平均损耗率：
$$
amega\_average_i = \frac{\sum_{n=0}^j{amega_{in}}}{100\cdot j}\\
s.t. amega_{in}\neq0
$$
