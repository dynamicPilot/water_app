"""
QWidget Class for show_stats method

"""
import config as c
import sys
import re

import pandas as pd

from data_processing import DataProcessing

import PyQt5 as puqt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QAction, 
qApp, QMainWindow, QMessageBox, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, 
QApplication, QFileDialog, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class StatsAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 300, 850, 700)
        self.setWindowTitle('Statistics')

        gen_data_dict, year_data_dict = self.data_class.create_dict_for_stats()
        gen_data_table = self.create_table(gen_data_dict)
        year_cold_water_data_table = self.create_table(year_data_dict['cold'])
        year_hot_water_data_table = self.create_table(year_data_dict['hot'])
        year_total_water_data_table = self.create_table(year_data_dict['total'])

        v_layout = QVBoxLayout()
        inner_grid = QGridLayout()
        header_label = QLabel('<b>STATISTICS</b>', self, margin = 10)
        header_label.setStyleSheet("font: 18pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(header_label, 0, 0)

        table_1_header_label = QLabel('<b>Average values</b>', self, margin = 4)
        table_1_header_label.setStyleSheet("font: 14pt")
        table_1_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(table_1_header_label, 1, 0)

        inner_grid.addWidget(gen_data_table, 2, 0)

        table_2_header_label = QLabel('<b>Average values per years for cold water</b>', self, margin = 4)
        table_2_header_label.setStyleSheet("font: 14pt")
        table_2_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(table_2_header_label, 3, 0)

        inner_grid.addWidget(year_cold_water_data_table, 4, 0)

        table_3_header_label = QLabel('<b>Average values per years for hot water</b>', self, margin = 4)
        table_3_header_label.setStyleSheet("font: 14pt")
        table_3_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(table_3_header_label, 5, 0)

        inner_grid.addWidget(year_hot_water_data_table, 6, 0)

        table_4_header_label = QLabel('<b>Average values per years</b>', self, margin = 4)
        table_4_header_label.setStyleSheet("font: 14pt")
        table_4_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(table_4_header_label, 7, 0)

        inner_grid.addWidget(year_total_water_data_table, 8, 0)

        v_layout.addLayout(inner_grid)
        v_layout.addStretch()
        self.setLayout(v_layout)


    def create_table(self, data_dict):
        columns_name = data_dict['columns']
        rows_name = data_dict['rows']
        data = data_dict['data']

        # Create table
        table_widget = QTableWidget()
        table_widget.setRowCount(len(rows_name))
        table_widget.setColumnCount(len(columns_name))
        for i in range(len(rows_name)):
            for j in range(len(columns_name)):
                value_to_call = QTableWidgetItem('{:.3f}'.format(data[i][j]))
                table_widget.setItem(i, j, value_to_call)
        table_widget.setHorizontalHeaderLabels(columns_name)
        table_widget.setVerticalHeaderLabels(rows_name)
        #table_widget.move(0,0)
        return table_widget



