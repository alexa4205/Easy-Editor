import os
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
                            QLabel, QPushButton, QRadioButton, QGroupBox, QListWidget, QHBoxLayout, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image

app = QApplication([])
window = QWidget()
window.resize(1100, 900)
window.setWindowTitle("Simplistic")

btn_left = QPushButton("Лево")
btn_right = QPushButton('Право')
btn_mirror = QPushButton("Отзеркалить")
btn_sharpness = QPushButton("Резкость")
btn_BW = QPushButton("Ч/Б")
btn_save = QPushButton("Сохранить")
btn_undo = QPushButton("Назад")

layout_btn = QHBoxLayout()
layout_btn.addWidget(btn_left)
layout_btn.addWidget(btn_right)
layout_btn.addWidget(btn_mirror)
layout_btn.addWidget(btn_sharpness)
layout_btn.addWidget(btn_BW)
layout_btn.addWidget(btn_save)
layout_btn.addWidget(btn_undo)

label_image = QLabel("Здесь будет ваше изображение")
layout_right = QVBoxLayout()
layout_right.addWidget(label_image, 95)
layout_right.addLayout(layout_btn)

btn_open = QPushButton("Открывай")
listwidget_files = QListWidget()
layout_left = QVBoxLayout()
layout_left.addWidget(btn_open)
layout_left.addWidget(listwidget_files)

layout_main = QHBoxLayout()
layout_main.addLayout(layout_left, 20)
layout_main.addLayout(layout_right, 80)

window.setLayout(layout_main)
window.show()

workdir = ""
def Choose_dir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def Filter(files, extentions):
    result = []
    for filename in files:
        for i in extentions:
            if filename.endswith(i):
                result.append(filename)
    return result

def Show_file_namelist():
    extentions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    Choose_dir()
    result = Filter(os.listdir(workdir), extentions)
    listwidget_files.clear()
    for i in result:
        listwidget_files.addItem(i)

class Image_processor:
    def __init__(self):
        self.filename = None
        self.image = None
        self.save_dir = 'Simplistic_image/'

    def load_image(self, filename):
        self.filename = filename
        self.image = Image.open(os.path.join(workdir, filename))
    
    def show_image(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = listwidget_files.width(), listwidget_files.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        label_image.setPixmap(scaled_pixmap)
        label_image.setVisible(True)

    def save_image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        self.image.save(os.path.join(path, self.filename))
    
    def black_and_white(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)


workimage = Image_processor()
def Show_Choosen_Image():
    if listwidget_files.currentRow() >= 0:
        filename = listwidget_files.currentItem().text()
        workimage.load_image(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.show_image(image_path)

listwidget_files.currentRowChanged.connect(Show_Choosen_Image)
btn_open.clicked.connect(Show_file_namelist)
btn_BW.clicked.connect(workimage.black_and_white)


app.exec()