import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QDialog,
        QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QTextEdit,
        QVBoxLayout, QWidget)

app = QApplication(sys.argv)
w = QWidget()
w.resize(250, 150)
w.move(300, 300)
w.setWindowTitle('简单窗口')
w.show()

sys.exit(app.exec_())