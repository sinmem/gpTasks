import pandas as pd
import matplotlib.pyplot as plt
'分析计算机学科和数理统计专业的男女生生源变化趋势并可视化'
'Math and Statistics'
'Computer Science'
percent_women = pd.read_csv(
    'F:/SWrk/gpTasks/Task3/percent-bachelors-degrees-women-usa.csv')
plt.plot(
    percent_women['Year'],
    percent_women['Math and Statistics'],
    c="purple",
    label='Women',
    ls="-.")
plt.plot(
    percent_women['Year'],
    100 - percent_women['Math and Statistics'],
    c="blue",
    label='Men',
    ls="-")
plt.title('Percentage of Math and Statistics Degrees Awarded By Gender')
plt.legend(loc='upper right')
plt.show()
plt.plot(
    percent_women['Year'],
    percent_women['Computer Science'],
    c="red",
    label='Women',
    ls=":")
plt.plot(
    percent_women['Year'],
    100 - percent_women['Computer Science'],
    c="blue",
    label='Men',
    ls="-.")
plt.legend(loc='upper right')
plt.title('Percentage of Computer Science Degrees Awarded By Gender')
plt.show()
