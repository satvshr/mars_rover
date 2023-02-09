import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QMainWindow, QFileDialog
from PySide6.QtGui import QIcon, QStandardItem, QPixmap
from PySide6 import QtUiTools, QtCore
import sys, os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView
from PySide6.QtCore import  Qt
from PySide6.QtGui import QFont, QColor, QImage, QStandardItemModel, QStandardItem

class StandardItem(QStandardItem):
    def __init__(self, txt='', image_path='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        if image_path:
            image = QImage(image_path)
            self.setData(image, Qt.DecorationRole)

class MyApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.path = '/home/satvshr/Desktop/mars/'
        self.lists = []
        self.index = 0
        self.total = 0
        for i in os.listdir(self.path):
            self.lists.append(self.path+i)
            self.total += 1
        print(self.lists)
        
        self.loader = QUiLoader()
        self.window = self.loader.load("page1.ui", None)

        self.window.setWindowTitle('NASA Image retriever')
        self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))

        self.button = self.window.fetch_button
        self.button.clicked.connect(self.magic)

    def magic(self):
        self.sol = self.window.sol_name.text()
        self.camera = self.window.camera_name.text()
        self.date = self.window.date_name.text()

        print(self.sol, self.camera, self.date)

        self.window = self.loader.load("page2.ui", None)
        self.window.show()

        self.display = self.window.label
        self.button1 = self.window.pushButton
        self.button2 = self.window.nextButton

        self.button2.clicked.connect(self.click)

    def click(self):
        self.pixi = QPixmap(self.lists[self.index])
        self.window.label.setPixmap(self.pixi)
        self.index += 1
        



#         viewer = view(treeView)
#         viewer.setCentralWidget(treeView)

# class view(QMainWindow):
#     def __init__(self, obj):
#         super().__init__()
#         self.setCentralWidget(obj)



app = QtWidgets.QApplication([])
# app.setStyleSheet('''
#     QWidget {
#         font-size: 25px;
#     }
#     QPushButton {
#         font-size: 20px;
#     }
# ''')
myapp = MyApp()
myapp.window.show()
sys.exit(app.exec())