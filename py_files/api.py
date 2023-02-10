import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QTextEdit, QVBoxLayout, QLabel, QMainWindow, QFileDialog
from PySide6.QtGui import QIcon, QStandardItem, QPixmap
from PySide6 import QtUiTools, QtCore
import sys, os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
import sys, time
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QRadioButton
from PySide6.QtCore import  QThread
from PySide6.QtGui import QFont, QColor, QImage, QStandardItemModel, QStandardItem
import requests, os, sys, ezgmail, glob
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot

class Image:
    def __init__(self):
        super().__init__()
    
    def length(self):
        self.y = self.x["photos"]
        self.len = 0
        flag = 0
        while flag == 0:
            try:
                r = self.y[self.len]
                self.len += 1
            except IndexError:
                flag = 1   
        print(self.len) 
        return self.len

    def fetch(self, sol, camera, date):

        self.sol = sol
        self.camera = camera
        self.date = date
        self.site = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?camera={self.camera}&earth_date={self.date}&api_key='
        self.api_key = 'udQJJYU8Kr2NOjyZaAryKkQtWeu1FiuoGQCQ8zGz'
        print(self.site+self.api_key)
        self.rec = requests.get(self.site+self.api_key)
        self.list = []
        self.x = self.rec.json()

        for i in range(self.length()):
            image = self.y[i]["img_src"]
            path = f'/home/satvshr/Desktop/mars/{i}.png'
            download = requests.get(image)
            with open(path, 'wb') as f:
                f.write(download.content)

        self.path = '/home/satvshr/Desktop/mars/'
        self.lists = []
        self.index = 0
        self.total = 0
        for i in os.listdir(self.path):
            self.lists.append(self.path+i)
            self.total += 1
        print(self.lists)

    def send_mail(self, recipients, subject, body, attachment):
        self.final = recipients.split(',')
        print(self.final)
        self.sub = subject
        self.body = body
        self.attach = attachment
        self.path = '/home/satvshr/Desktop/mars/'
        list = []
        for file in os.listdir(self.path):
            list.append(self.path + file)
        #[x.encode('utf-8') for x in self.final]
        for i in self.final:
            ezgmail.send(i, self.sub, self.body, self.attach)

    def purge(self):
        path = '/home/satvshr/Desktop/mars/'
        for f in os.listdir(path):
            os.remove(path + f)

class MyApp(QMainWindow, QWidget, Image):
    def __init__(self):
        super().__init__()

        self.loader = QUiLoader()
        self.window = self.loader.load("page1.ui", None)

        self.window.setWindowTitle('NASA Image retriever')
        self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))

        self.button = self.window.fetch_button
        self.radio1 = self.window.curiosity
        self.radio2 = self.window.opportunity
        self.radio3 = self.window.spirit

        self.radio1.clicked.connect(self.choice)
        self.radio2.clicked.connect(self.choice)
        self.radio3.clicked.connect(self.choice)

        self.button.clicked.connect(self.magic)

    def choice(self):
        if self.radio1.isChecked():
            self.sol = "curiosity"
        if self.radio2.isChecked():
            self.sol = "opportunity"
        if self.radio3.isChecked():
            self.sol = "spirit"

    def magic(self):
        self.camera = self.window.camera_name.text()
        self.date = self.window.date_name.text()
        self.loader = QUiLoader()
        self.window = self.loader.load("page5.ui", None)
        self.window.setWindowTitle('NASA Image retriever')
        self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
        self.window.show()
        self.fetch(self.sol, self.camera, self.date)
        # for i in range(10):
        #     time.sleep(1)
        # check bugs
        counter = 0
        flag = 0
        while flag == 0:
            for i in os.listdir(self.path):
                counter += 1
                print(counter)
            if counter == self.len:
                    flag = 1
 
        print(self.sol, self.camera, self.date)

        self.window = self.loader.load("page2.ui", None)
        self.window.setWindowTitle('NASA Image retriever')
        self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
        self.window.show()


        self.display = self.window.label
        self.button1 = self.window.sendButton
        self.button2 = self.window.nextButton
        self.button3 = self.window.prevButton
        if len(self.lists) == 0:
            self.loader = QUiLoader()
            self.window = self.loader.load("page5.ui", None)
            self.window.setWindowTitle('NASA Image retriever')
            self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
            self.window.show()
        self.pixi = QPixmap(self.lists[0])
        self.window.label.setPixmap(self.pixi)

        self.button1.clicked.connect(self.send)
        self.button2.clicked.connect(self.next)
        self.button3.clicked.connect(self.prev)

    def next(self):
        if self.index < self.total-1:
            self.index += 1            
            self.pixi = QPixmap(self.lists[self.index])
            self.window.label.setPixmap(self.pixi)
    
    def prev(self):
        if self.index > 0:
            self.index -= 1
            self.pixi = QPixmap(self.lists[self.index])
            self.window.label.setPixmap(self.pixi)
            
    def send(self):
        self.loader = QUiLoader()
        self.window = self.loader.load("page3.ui", None)
        self.window.setWindowTitle('NASA Image retriever')
        self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
        self.window.show()

        self.button4 = self.window.mailButton
        self.button4.clicked.connect(self.submit)

    def submit(self):
            self.email = self.window.email_ids.toPlainText()
            self.sub = self.window.subject.toPlainText()
            self.body = self.window.body.toPlainText()
            self.loader = QUiLoader()
            self.window = self.loader.load("page6.ui", None)
            self.window.setWindowTitle('NASA Image retriever')
            self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
            self.window.show()
            self.attachments = []
            path = '/home/satvshr/Desktop/mars/'

            for f in os.listdir(path):
                self.attachments.append(path + f)
            self.send_mail(self.email, self.sub, self.body, self.attachments)

            self.loader = QUiLoader()
            self.window = self.loader.load("page4.ui", None)
            self.window.setWindowTitle('NASA Image retriever')
            self.window.setWindowIcon(QIcon('/home/satvshr/Downloads/nasa.jpg'))
            self.window.show()
            self.purge()

        # except:
        #     print("Email was not sent")




app = QtWidgets.QApplication([])
app.setStyleSheet('''
#Form1 {
  background-image: url(/home/satvshr/Desktop/env/wp2461890.jpg);
  background-repeat: no-repeat;
  background-position: center;
}
#Form3 > QLabel {
    color: white;
    background-color: black;
}
#Form3 {
  background-image: url(/home/satvshr/Desktop/env/_120526773_whatsubject.jpg);
  background-repeat: no-repeat;
  background-position: center;
}
#Form4 {
  background-image: url(/home/satvshr/Desktop/env/HD-wallpaper-nasa-logo-black-oled-nasa-logo-black-dark-oled.jpg);
  background-repeat: no-repeat;
  background-position: center;
}
#Form5 {
  background-image: url(/home/satvshr/Desktop/env/icons8-spam-100.png);
  background-repeat: no-repeat;
  background-position: center;
}
#Form6 {
  background-image: url(/home/satvshr/Desktop/env/icons8-spam-100.png);
  background-repeat: no-repeat;
  background-position: center;
}
''')
myapp = MyApp()
myapp.window.show()
sys.exit(app.exec())

