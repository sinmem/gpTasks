import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QDialog, QComboBox,
                             QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
                             QTextEdit, QVBoxLayout, QWidget)


class Example(QWidget):

    def _init_(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        combo = QComboBox(self)
        combo.addItem('Easy')
        combo.addItem('Normal')
        combo.addItem('Hard')

        combo.move(50, 50)

        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated(self, text):
        print(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex.show()
    sys.exit(app.exec_())