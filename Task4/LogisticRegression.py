import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
'''
PS：逻辑回归是用来分类的！！！不是用来做线性回归的！
sigmoid 函数的反函数叫做 logit 函数，
这就是逻辑回归 logistic regression 的来历，跟逻辑没啥关系
'''


def getoriginBympg(test_Result):
    tempList = []
    for item in test_Result:
        if item[0] > item[1]:
            max = item[0]
            if max > item[2]:
                tempList.append(1)
            else:
                tempList.append(3)
        else:
            max = item[1]
            if max > item[2]:
                tempList.append(2)
            else:
                tempList.append(3)
    return tempList


def getz(aList, bList):
    Turea = 0
    for i in range(0, len(aList)):
        if aList[i] is bList[i]:
            Turea += 1
    return Turea * 100 / len(aList)


columns = [
    "mpg", "cylinders", "displacement", "horsepower", "weight", "acceleration",
    "model year", "origin", "car name"
]
mpg_origin = ["mpg", "origin"]
data = pd.read_table(
    'F:/SWrk/gpTasks/Task4/auto-mpg.data',
    delim_whitespace=True,
    names=columns)
# print(data[mpg_origin])
data = data[mpg_origin].sample(frac=1)
# 训练样本
train = data[:300]
# 测试样本
test = data[300:]
# print(data[300:])
_y = train['origin']
_x = train['mpg']
t_x = test['mpg']
x_ = np.array(_x)
y_ = np.array(_y)
t_x = np.array(t_x)
clf = LogisticRegression()
clf.fit(x_[:, np.newaxis], y_)
test_Result = clf.predict_proba(t_x[:, np.newaxis])
print(test_Result)
resultList = getoriginBympg(test_Result)
datas = {'mpg': test['mpg'], 'test': resultList, 'origin': test['origin']}
Result = pd.DataFrame(data=datas, columns=['mpg', 'test', 'origin'])
print(Result)
print("正确率:%.3f" % (getz(list(Result['origin']), list(Result['test']))), "%")
yy = range(0, len(test_Result))
plt.plot(
    yy, test_Result[:, 0], linewidth=1, label="degree={}".format(1), ls=':')
plt.plot(
    yy, test_Result[:, 1], linewidth=1, label="degree={}".format(2), ls='-.')
plt.plot(
    yy, test_Result[:, 2], linewidth=1, label="degree={}".format(3), ls='-')
plt.ylim(0, 1)
plt.legend()
plt.show()

# plt.plot(data['origin'], y_test, linewidth=1, label="degree={}".format(1))
# plt.xlim(0, 45)
# plt.ylim(0, 4)
# plt.legend()
# plt.scatter(_x, _y, s=2)
# plt.show()
# pd.DataFrame()
