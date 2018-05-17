import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import scipy as sp
''' 均方误差根 '''


def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y)**2))


''' 与均值相比的优秀程度，介于[0~1]。0表示不如均值。1表示完美预测.这个版本的实现是参考scikit-learn官网文档  '''


def R2(y_test, y_true):
    return 1 - ((y_test - y_true)**2).sum() / (
        (y_true - y_true.mean())**2).sum()


''' 这是Conway&White《机器学习使用案例解析》里的版本 '''


def R22(y_test, y_true):
    y_mean = np.array(y_true)
    y_mean[:] = y_mean.mean()
    return 1 - rmse(y_test, y_true) / rmse(y_mean, y_true)


columns = [
    "mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration",
    "model year", "origin", "car name"
]
mpg_weight = ["mpg", "weight"]
data = pd.read_table(
    'F:/SWrk/gpTasks/Task4/auto-mpg.data',
    delim_whitespace=True,
    names=columns)
_y = data['mpg']
_x = data['weight']
x_ = np.array(_x)
y_ = np.array(_y)
clf = Pipeline([('poly', PolynomialFeatures(degree=1)),
                ('linear', LinearRegression(fit_intercept=False))])
clf.fit(x_[:, np.newaxis], y_)
y_test = clf.predict(x_[:, np.newaxis])
print('rmse: %f\nR2: %f\nR22: %f' %
      (rmse(y_test, y_), R2(y_test, y_), R22(y_test, y_)))
plt.plot(x_, y_test, linewidth=1, label="degree={}".format(1))
plt.xlim(1000, 6500)
plt.ylim(5, 45)
plt.legend()
plt.scatter(_x, _y, s=2)
plt.show()
