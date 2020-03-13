"""
QWidget Class for prediction method

"""
import config as c
import sys
import re

import os.path

import pandas as pd

from data_processing import DataProcessing

import PyQt5 as puqt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QAction, 
qApp, QScrollArea, QMessageBox, QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, 
QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class Prediction(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 100, 800, 910)
        self.setWindowTitle('Graph Statistics')
        self.data_dict = self.data_class.create_content_for_prediction()
        self.path_to_graph_folder = self.data_class.path_to_graph_folder_pred

        graph_widget = QWidget()
        v_layout = QVBoxLayout()

        header_label = QLabel('<b>PREDICTED COST</b>', self, margin = 10)
        header_label.setStyleSheet("font: 16pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label)


        data_table = self.create_table()
        v_layout.addWidget(data_table, alignment = QtCore.Qt.AlignCenter)

        graph_header_label = QLabel('Predicted Cost per mont: bar plots', self, margin = 4)
        graph_header_label.setStyleSheet("font: 14pt")
        graph_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(graph_header_label)
            
        t1_bar_label = QLabel()
        t1_pixmap = QPixmap(f'{self.path_to_graph_folder}/current_total_cost.png')
        t1_pixmap = t1_pixmap.scaledToHeight(220)
        t1_bar_label.setPixmap(t1_pixmap)
        t1_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(t1_bar_label)


        t2_bar_label = QLabel()
        t2_pixmap = QPixmap(f'{self.path_to_graph_folder}/current_cold_cost.png')
        t2_pixmap = t2_pixmap.scaledToHeight(220)
        t2_bar_label.setPixmap(t2_pixmap)
        t2_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(t2_bar_label)

        t3_bar_label = QLabel()
        t3_pixmap = QPixmap(f'{self.path_to_graph_folder}/current_hot_cost.png')
        t3_pixmap = t3_pixmap.scaledToHeight(220)
        t3_bar_label.setPixmap(t3_pixmap)
        t3_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(t3_bar_label)
        v_layout.addStretch()
        graph_widget.setLayout(v_layout)
        
        scroll_area = QScrollArea()
        #scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(graph_widget)

        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll_area)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout)

    def create_table(self, gap = 0):
        columns_name = self.data_dict['month']
        rows_name = ['Predicted cost for cold water', 'Predicted cost for hot water', 'Predicted total cost for water']
        data = [self.data_dict['cold'], self.data_dict['hot'], self.data_dict['total']]

        # Create table
        total_row_height = 0
        table_widget = QTableWidget()
        table_widget.setRowCount(len(rows_name))
        table_widget.setColumnCount(len(columns_name))
        for i in range(len(rows_name)):
            total_columns_width = 0
            for j in range(len(columns_name)):
                value_to_call = QTableWidgetItem('{:.1f}'.format(data[i][j]))
                value_to_call.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(i, j, value_to_call)
                total_columns_width += table_widget.columnWidth(j)
            total_row_height += table_widget.rowHeight(i)

        table_widget.setHorizontalHeaderLabels(columns_name)
        table_widget.setVerticalHeaderLabels(rows_name)

        total_row_height = total_row_height/(len(rows_name))*(len(rows_name)+1)+gap
        table_widget.setMaximumHeight(total_row_height)
        table_widget.setMinimumHeight(total_row_height)
        table_widget.setMinimumWidth(total_columns_width+180)
        table_widget.setMaximumWidth(total_columns_width+180)
        table_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #table_widget.resizeColumnsToContents()
        return table_widget