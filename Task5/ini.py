import win32api
import win32gui
import time
import re
appPath = r'F:/winmine.exe'
win32api.ShellExecute(0, 'open', appPath, '', '', 1)
time.sleep(0.3)
# 起止坐标
x, y = [0, 0], [0, 0]
config = []
temp = open('F:/SWrk/gpTasks/Task5/conf.txt', "r", encoding="utf-8")
for item in temp:
    tlist = re.split(',|\\n', item)
    config.append(tlist)


def foo(hwnd, mouse):
    # 获取窗体左右上下坐标
    if win32gui.GetWindowText(hwnd) == '扫雷':
        x[0], y[0], x[1], y[1] = win32gui.GetWindowRect(hwnd)


win32gui.EnumWindows(foo, 0)
# 窗口大小
width = x[1] - x[0]
height = y[1] - y[0]
global row, col, lpx, lpy, mod
# 行列数
row = 0
col = 0
# 那某个脸的坐标,遮脸就被切割成9*9就好
lpx, lpy = 0, 0
# 模式
mod = ''
if config[0][0] == str(width):
    row = int(config[0][2])
    col = int(config[0][3])
    lpx, lpy = int(config[6][0]), int(config[6][1])
    mod = 'Easy'
elif config[1][0] == str(width):
    row = int(config[1][2])
    col = int(config[1][3])
    lpx, lpy = int(config[7][0]), int(config[7][1])
    mod = 'Normal'
elif config[2][0] == str(width):
    row = int(config[2][2])
    col = int(config[2][3])
    lpx, lpy = int(config[8][0]), int(config[8][1])
    mod = 'Hard'
blocksize = int(config[3][1])
# x偏移量
px = int(config[5][0])
# y偏移量
py = int(config[5][1])
