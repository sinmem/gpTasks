import pandas as pd
import matplotlib.pyplot as plt


def getMax(sers):
    temp = list(sers)
    temp.pop(0)
    return max(temp)


def getIndex(sers, maxNum):
    temp = list(sers.index)
    j = 0
    flag = False
    for i in sers:
        if i != maxNum:
            j += 1
        else:
            flag = True
            break
    if flag:
        return temp[j]
    else:
        return "none"


percent_women = pd.read_csv(
    'F:/SWrk/gpTasks/Task3/percent-bachelors-degrees-women-usa.csv')
yearA = int(input("要查找哪一年女生最高的专业?\n"))
yearB = int(percent_women.iat[0, 0])
sers = pd.Series(percent_women.iloc[yearA - yearB])
mNu = getMax(sers)
key = getIndex(sers, mNu)
print('----------------------\n已查出%d年,女生最多的专业是%s\n\n正在分析历年来该专业生源变化情况' % (yearA,
                                                                         key))
if 'none' == key:
    print('-----------defeat-----------')
    print('\n-----------please check your input-----------\n')
else:
    print('-----------success-----------')
    plt.plot(
        percent_women['Year'],
        percent_women[key],
        c="purple",
        label='Women',
        ls="-.")
    plt.plot(
        percent_women['Year'],
        100 - percent_women[key],
        c="blue",
        label='Men',
        ls="-")
    plt.title('Percentage of ' + key + ' Degrees Awarded By Gender')
    plt.legend(loc='upper right')
    print('\n-----------please click to check-----------\n')
    plt.show()
