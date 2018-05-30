import sys
import sweeper
import json
import ini
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QBoxLayout,
                             QApplication, QComboBox, QPushButton, QMessageBox)
LEFT, ABOVE = range(2)
vDir = {}
vL = ['已玩次数', '胜场', '最大连胜', '最大连败', '当前连场', '胜率']


def get_view(gameFalg=True, dir={}):
    wstimes = int(dir['最大连胜'])
    bstimes = int(dir['最大连败'])
    nowr = int(dir['当前连场'])
    dir['已玩次数'] = str(int(dir['已玩次数']) + 1)
    if gameFalg:
        dir['胜场'] = str(int(dir['胜场']) + 1)
        nowr = (nowr + 1) if nowr > 0 else 1
        wstimes = max(wstimes, nowr)
    else:
        nowr = (nowr - 1) if nowr < 0 else -1
        bstimes = max(bstimes, -nowr)
    dir['最大连胜'] = str(wstimes)
    dir['最大连败'] = str(bstimes)
    dir['当前连场'] = str(nowr)
    dir['胜率'] = str(round(100 * int(dir['胜场']) / int(dir['已玩次数']), 2))
    return dir


# 初始化文件
def iniresource():
    global vDir
    for i in ['Easy', 'Normal', 'Hard']:
        tempDir = {}
        for j in vL:
            tempDir[j] = '0'
        vDir[i] = tempDir
    jsObj = json.dumps(vDir)
    with open('F:/SWrk/gpTasks/Task5/myresouce.json', "w") as ftemp:
        ftemp.write(jsObj)


class initlable(QWidget):
    def __init__(self, labelText="", position=LEFT, parent=None):
        super(initlable, self).__init__(parent)
        self.label = QLabel()
        self.label.setText(labelText)
        # self.lineEdit = QLineEdit()
        # self.label.setBuddy(self.lineEdit)
        layout = QBoxLayout(QBoxLayout.LeftToRight
                            if position == LEFT else QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        # layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class windo(QWidget):
    def __init__(self, varsDir={}, mod=''):
        super().__init__()
        self.vDir = varsDir
        # self.varsDir = varsDir[mod]
        self.mod = mod
        self.times = initlable()
        self.wintimes = initlable()
        self.wstimes = initlable()
        self.bstimes = initlable()
        self.nowr = initlable()
        self.winrate = initlable()
        self.setresult(varsDir[mod])
        self.resButton = QPushButton("重置数据")
        self.resButton.clicked.connect(self.reset)
        self.closeButton = QPushButton("关闭")
        self.closeButton.clicked.connect(QCoreApplication.instance().quit)
        combo = QComboBox(self)
        tL = ['Easy', 'Normal', 'Hard']
        for i in tL:
            combo.addItem(i)
        # 设置默认选中项
        combo.setCurrentText(mod)
        self.combo = combo
        self.combo.activated[str].connect(self.onActivated)
        self.initUI()

    def setresult(self, varsDir={}):
        self.times.label.setText('已玩次数: ' + varsDir["已玩次数"])
        self.wintimes.label.setText('胜场: ' + varsDir['胜场'])
        self.wstimes.label.setText('最大连胜: ' + varsDir['最大连胜'])
        self.bstimes.label.setText('最大连败: ' + varsDir['最大连败'])
        self.nowr.label.setText('当前连场: ' + varsDir['当前连场'])
        self.winrate.label.setText('胜率: ' + varsDir['胜率'] + '%')

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(9)

        grid.addWidget(self.combo, 1, 1)
        grid.addWidget(self.times, 2, 2)
        grid.addWidget(self.wintimes, 3, 2)
        grid.addWidget(self.wstimes, 4, 2)
        grid.addWidget(self.bstimes, 5, 2)
        grid.addWidget(self.nowr, 6, 2)
        grid.addWidget(self.winrate, 7, 2)

        empt = QLabel()
        grid.addWidget(empt, 8, 2)

        # grid.addWidget(okButton, 8, 0)
        grid.addWidget(self.resButton, 9, 1)
        grid.addWidget(self.closeButton, 9, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('扫雷数据统计')
        # self.show()

    def onActivated(self, text):
        self.mod = text
        self.setresult(self.vDir[text])

    def get_dir(self):
        return self.vDir

    def reset(self):
        tempdir = self.vDir[self.mod]
        # 改内部数据
        for item in tempdir:
            tempdir[item] = '0'
        # 改界面显示
        self.times.label.setText('已玩次数: 0')
        self.wintimes.label.setText('胜场: 0')
        self.wstimes.label.setText('最大连胜: 0')
        self.bstimes.label.setText('最大连败: 0')
        self.nowr.label.setText('当前连场: 0')
        self.winrate.label.setText('胜率: 0.0%')
        self.vDir[self.mod] = tempdir

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '提示信息', "您要退出吗?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    try:
        f = open('F:/SWrk/gpTasks/Task5/myresouce.json', "r", encoding="utf-8")
        vDir = json.load(f)
        f.close()
    except FileNotFoundError:
        print("FileNotFoundError")
        iniresource()
    varsDir = vDir[ini.mod]
    app = QApplication(sys.argv)
    gameFalg = sweeper.startgame()
    varsDir = get_view(gameFalg, varsDir)
    ex = windo(vDir, ini.mod)
    ex.show()
    app.exec_()
    vDir = ex.get_dir()
    jsObj = json.dumps(vDir)
    with open('F:/SWrk/gpTasks/Task5/myresouce.json', "w") as ftemp:
        ftemp.write(jsObj)
    # print(ex.times.label.text())
    # print(ex.times.label.text())
    # print(ex.wintimes.label.text())
    # print(ex.wstimes.label.text())
    # print(ex.bstimes.label.text())
    # print(ex.nowr.label.text())
    # print(ex.winrate.label.text())
    sys.exit()
