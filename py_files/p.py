import requests, os, sys, ezgmail, glob
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot


class Image:
    def __init__(self):
        super().__init__()
    
    def len(self):
        self.y = self.x["photos"]
        len = 0
        flag = 0
        while flag == 0:
            try:
                r = self.y[len]
                len += 1
            except IndexError:
                flag = 1    
        return len

    def fetch(self, sol, camera, date):

        self.sol = sol
        self.camera = camera
        self.date = date
        self.site = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={self.sol}&camera={self.camera}&earth_date={self.date}&api_key='
        self.api_key = 'udQJJYU8Kr2NOjyZaAryKkQtWeu1FiuoGQCQ8zGz'
        self.rec = requests.get(self.site+self.api_key)
        self.list = []
        self.x = self.rec.json()

        for i in range(self.len()):
            image = self.y[i]["img_src"]
            path = f'/home/satvshr/Desktop/mars/{i}.png'
            download = requests.get(image)
            with open(path, 'wb') as f:
                f.write(download.content)

    def send_mail(self, recipients, subject, body):
        self.recieve = recipients
        self.sub = subject
        self.body = body
        path = '/home/satvshr/Desktop/mars/'
        list = []
        for file in os.listdir(path):
            list.append(path + file)
        for i in self.recieve:
            ezgmail.send(i, self.sub, self.body, list)

    def purge(self):
        path = '/home/satvshr/Desktop/mars/'
        for f in os.listdir(path):
            os.remove(path + f)

img = Image()
img.fetch()
img.send_mail(['satvmishi@gmail.com', 'satvshr1@gmail.com'], 'mars pics', 'Here are the pictures!')
img.purge()
