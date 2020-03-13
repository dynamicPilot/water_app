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

class TableStatsAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 50, 1000, 1000)
        self.setWindowTitle('Table Statistics')

        gen_data_dict, year_data_dict, month_value_dict, month_cost_dict = self.data_class.create_dict_for_stats()
        gen_data_table = self.create_table(gen_data_dict)
        year_cold_water_data_table = self.create_table(year_data_dict['cold'])
        year_hot_water_data_table = self.create_table(year_data_dict['hot'])
        year_total_water_data_table = self.create_table(year_data_dict['total'])
        month_value_data_table = self.create_table(month_value_dict)
        month_cost_data_table = self.create_table(month_cost_dict)

        v_layout = QVBoxLayout()

        header_label = QLabel('<b>TABLE STATISTICS</b>', self, margin = 10)
        header_label.setStyleSheet("font: 18pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label, stretch = 2)

        table_1_header_label = QLabel('<b>Average values</b>', self, margin = 4)
        table_1_header_label.setStyleSheet("font: 14pt")
        table_1_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_1_header_label, stretch = 1)

        v_layout.addWidget(gen_data_table, stretch = 7)

        table_2_header_label = QLabel('<b>Average values per years for cold water</b>', self, margin = 4)
        table_2_header_label.setStyleSheet("font: 14pt")
        table_2_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_2_header_label, stretch = 1)

        v_layout.addWidget(year_cold_water_data_table, stretch = 4)

        table_3_header_label = QLabel('<b>Average values per years for hot water</b>', self, margin = 4)
        table_3_header_label.setStyleSheet("font: 14pt")
        table_3_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_3_header_label, stretch = 1)

        v_layout.addWidget(year_hot_water_data_table, stretch = 4)

        table_4_header_label = QLabel('<b>Average values per years</b>', self, margin = 4)
        table_4_header_label.setStyleSheet("font: 14pt")
        table_4_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_4_header_label, stretch = 1)

        v_layout.addWidget(year_total_water_data_table, stretch = 4)

        table_5_header_label = QLabel('<b>Average values per every month</b>', self, margin = 4)
        table_5_header_label.setStyleSheet("font: 14pt")
        table_5_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_5_header_label, stretch = 1)

        v_layout.addWidget(month_value_data_table, stretch = 6)

        table_6_header_label = QLabel('<b>Average cost per every month</b>', self, margin = 4)
        table_6_header_label.setStyleSheet("font: 14pt")
        table_6_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_6_header_label, stretch = 1)

        v_layout.addWidget(month_cost_data_table, stretch = 6)

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
                value_to_call.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(i, j, value_to_call)
        table_widget.setHorizontalHeaderLabels(columns_name)
        table_widget.setVerticalHeaderLabels(rows_name)
        return table_widget

class GraphStatsAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 100, 800, 800)
        self.setWindowTitle('Graph Statistics')



