"""
QWidget Class for show settings method

"""
import config as c
import sys
import re

import pandas as pd

from data_processing import DataProcessing

import PyQt5 as puqt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QToolTip, QVBoxLayout, QHBoxLayout, QComboBox, QAction, 
qApp, QMainWindow, QMessageBox, QLabel, QPushButton, QLineEdit, QInputDialog, 
QTextEdit, QGridLayout, QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QPlainTextEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class Settings(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.config_path = 'config.py'
        self.initUI()
        
    def initUI(self):
        #set window params
        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('Settings')

        self.create_edit_widget()
      

    def create_edit_widget(self):
        pass
        