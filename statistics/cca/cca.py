import numpy as np
import pandas as pd
from sklearn.cross_decomposition import CCA
from scipy.stats import chi2

data = pd.read_excel("statistics/cca/health.xlsx").values
x = data[:, 0:3]
y = data[:, 3:6]
cca = CCA(n_components=3) # 取前 3 个典型变量
cca.fit(x, y)
u, v = cca.transform(x, y) # 得到变换后的典型变量

corr = [np.corrcoef(u[:, i], v[:, i])[0, 1] for i in [0, 1, 2]] # 相关系数
print("典型相关系数为：", corr)

# 假设检验
alpha = 0.05
def test(k: int):
    """
    进行第 k + 1 典型相关系数是否为 0 的检验。
    返回 True 时，表明不能拒绝原假设，系数为 0
    """
    n = data.shape[0]
    r = np.array(corr)
    p, q = 3, 3 # 设置 X 和 Y 的维数
    f = (p - k) * (q - k) # 自由度
    m = n - k - 1 - (p + q + 1) / 2
    Q = - m * np.log(np.prod(1 - (r[k:]) ** 2))
    chisq_alpha = chi2.ppf(1 - alpha, f)
    return Q, chisq_alpha, Q < chisq_alpha

print("检验统计量，临界值，接受", test(k=0))
