"""
QWidget Class for show history method

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

class DisplayHistory(QMainWindow):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        #set menubar
        save_file = QAction('Save to excel', self)
        save_file.setStatusTip('Save table to excel format')
        save_file.triggered.connect(self.save_table_to_excel)

        quit_current_win = QAction('Quit history', self)
        quit_current_win.setStatusTip('Quit history window')
        quit_current_win.triggered.connect(self.close)

        quit_all = QAction('Quit app', self)
        quit_all.setStatusTip('Quit all windows')
        quit_all.triggered.connect(QApplication.quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(save_file)
        file_menu.addAction(quit_current_win)
        file_menu.addAction(quit_all)

        data_dict = self.data_class.create_dict_to_all_history()
        self.columns_name = data_dict['columns']
        self.data = data_dict['data']

        self.create_table()
        self.setCentralWidget(self.tableWidget)

        #set window params
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('All Data')
    
    def save_table_to_excel(self):
        self.data_class.save_data_to_excel()
        mes_text = "File was saved in: {}".format(self.data_class.file_save_path)
        mes = QMessageBox()
        mes.setWindowTitle('Message')
        mes.setText(mes_text)
        mes.exec()

    def create_table(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setColumnCount(len(self.columns_name))
        for i in range(len(self.data)):
            for j in range(len(self.columns_name)):
                if j > 1:
                    value_to_call = QTableWidgetItem('{:.3f}'.format(self.data[i][j]))
                else:
                    value_to_call = QTableWidgetItem(str(self.data[i][j]))
                self.tableWidget.setItem(i, j, value_to_call)
        self.tableWidget.setHorizontalHeaderLabels(self.columns_name)
        self.tableWidget.move(0,0)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)


    @QtCore.pyqtSlot()
    def on_click(self):
        pass
        #print("\n")
        #for currentQTableWidgetItem in self.tableWidget.selectedItems():
            #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
