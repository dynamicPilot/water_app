"""
QWidget Class for new data analysis method

"""
import config as c
import sys
import re
import os.path

import pandas as pd

from data_processing import DataProcessing

import PyQt5 as puqt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QToolTip, QVBoxLayout, QHBoxLayout, QComboBox, QAction, 
qApp, QMainWindow, QMessageBox, QLabel, QPushButton, QLineEdit, QInputDialog, 
QTextEdit, QGridLayout, QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QPlainTextEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class NewValueAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        self.result_dict = self.data_class.data_to_new_value_analysis()
        self.path_to_graph_folder = self.data_class.path_to_graph_folder_new_month
        self.data_class.create_graphs_to_new_value_analysis()

        cvs_delta_with_aver = (self.result_dict['delta_cvs'] - self.result_dict['cvs_aver'][0])/self.result_dict['cvs_aver'][0]
        hvs_delta_with_aver = (self.result_dict['delta_hvs'] - self.result_dict['hvs_aver'][0])/self.result_dict['hvs_aver'][0]
        total_delta_with_aver = (self.result_dict['total'] - self.result_dict['total_aver'])/self.result_dict['total_aver']
        cvs_delta_label = 'less' if cvs_delta_with_aver <= 0 else 'more'
        hvs_delta_label = 'less' if hvs_delta_with_aver <= 0 else 'more'
        total_delta_label = 'less' if total_delta_with_aver <= 0 else'more'

        v_layout = QVBoxLayout()
        inner_grid = QGridLayout()

        header_label = QLabel('<b>CURRENT MONTH DATA</b>', self, margin = 10)
        header_label.setStyleSheet("font: 18pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(header_label, 0, 0)
    
        month_year_label = QLabel('Month: <b>{}</b>, Year: <b>{}</b>.'.format(self.result_dict['month'], self.result_dict['year']), self)
        inner_grid.addWidget(month_year_label, 1, 0)
        value_label = QLabel('Current value for <b>COLD</b> water: {:.3f} m3, current value for <b>HOT</b> water: {:.3f} m3.'.format(self.result_dict['cvs'], self.result_dict['hvs']), self)
        inner_grid.addWidget(value_label, 2, 0)
        cost_label = QLabel('Cost for <b>COLD</b> water: {:.2f} rub/m3, cost for <b>HOT</b> water: {:.2f} rub/m3.'.format(self.data_class.cold_water_price, self.data_class.hot_water_price), self)
        inner_grid.addWidget(cost_label, 3, 0)

        short_1_label = QLabel('You should pay <b>{:.1f}</b> rub in total: <b>{:.1f}</b> rub for cold water and <b>{:.1f}</b> for hot.'.format(self.result_dict['total'],self.result_dict['price_cvs'],self.result_dict['price_hvs']), self, margin = 5)
        short_1_label.setStyleSheet("font: 13pt")
        inner_grid.addWidget(short_1_label, 4, 0)
        short_2_label = QLabel('This is by {:.1%} {} than average total ({:.2f} rub).'.format(abs(total_delta_with_aver), total_delta_label, self.result_dict['total_aver']), self)
        inner_grid.addWidget(short_2_label, 5, 0)
        short_3_label = QLabel('You should pay {} (by {:.1%}) for cold water and {} (by {:.1%}) for hot water.'.format(cvs_delta_label, abs(cvs_delta_with_aver), hvs_delta_label, abs(hvs_delta_with_aver)), self)
        inner_grid.addWidget(short_3_label, 6, 0)
        short_4_label = QLabel('See details for more info.')
        inner_grid.addWidget(short_4_label, 7, 0)

        long_header_label = QLabel('<b>DETAILS</b>', self, margin = 8)
        long_header_label.setStyleSheet("font: 16pt")
        long_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(long_header_label, 8, 0)
        
        total_header_label = QLabel('<b>TOTAL</b>', self, margin = 2)
        total_header_label.setStyleSheet('font: 14pt')
        total_header_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(total_header_label, 9, 0)

        total_cost_label = QLabel('Cost for <b>Total</b>: <b>{:.1f}</b> rub.'.format(self.result_dict['total']), self)
        total_cost_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(total_cost_label, 10, 0)

        total_cost_pred_label = QLabel('Predicted cost: {:.1f} rub, actial cost: {:.1f} rub.'.format(self.result_dict['price_hvs_pred'] + self.result_dict['price_cvs_pred'], self.result_dict['total']))
        total_cost_pred_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(total_cost_pred_label, 11, 0)

        total_bar_label = QLabel()
        total_pixmap = QPixmap(f'{self.path_to_graph_folder}/TOTAL.png')
        total_pixmap = total_pixmap.scaledToHeight(210)
        total_bar_label.setPixmap(total_pixmap)
        total_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        inner_grid.addWidget(total_bar_label, 12, 0)
        v_layout.addLayout(inner_grid)
        v_layout.addStretch(1)

        bot_inner_grid = QGridLayout()
        cold_header_label = QLabel('<b>COLD WATER</b>', self, margin = 0)
        cold_header_label.setStyleSheet('font: 14pt')
        cold_header_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(cold_header_label, 0, 0)

        cold_delta_label = QLabel('Delta for <b>COLD</b> water: <b>{:.3f}</b> m3.'.format(self.result_dict['delta_cvs']), self)
        cold_delta_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(cold_delta_label, 1, 0)

        cold_cost_label = QLabel('Cost for <b>COLD</b> water: <b>{:.1f}</b> rub.'.format(self.result_dict['price_cvs']))
        cold_cost_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(cold_cost_label, 2, 0)

        cold_cost_pred_label = QLabel('Predicted cost: {:.1f} rub, actial cost: {:.1f} rub.'.format(self.result_dict['price_cvs_pred'], self.result_dict['price_cvs']))
        cold_cost_pred_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(cold_cost_pred_label, 3, 0)

        cold_bar_label = QLabel()
        price_cvs_pixmap = QPixmap(f'{self.path_to_graph_folder}/PRICE_CVS.png')
        price_cvs_pixmap = price_cvs_pixmap.scaledToHeight(180)
        cold_bar_label.setPixmap(price_cvs_pixmap)
        cold_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(cold_bar_label, 4, 0)

        hot_header_label = QLabel('<b>HOT WATER</b>', self, margin = 2)
        hot_header_label.setStyleSheet('font: 14pt')
        hot_header_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(hot_header_label, 0, 1)

        hot_delta_label = QLabel('Delta for <b>HOT</b> water: <b>{:.3f}</b> m3.'.format(self.result_dict['delta_hvs']), self)
        hot_delta_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(hot_delta_label, 1, 1)

        hot_cost_label = QLabel('Cost for <b>HOT</b> water: <b>{:.1f}</b> rub.'.format(self.result_dict['price_hvs']))
        hot_cost_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(hot_cost_label, 2, 1)

        hot_cost_pred_label = QLabel('Predicted cost: {:.1f} rub, actial cost: {:.1f} rub.'.format(self.result_dict['price_hvs_pred'], self.result_dict['price_hvs']))
        hot_cost_pred_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(hot_cost_pred_label, 3, 1)

        hot_bar_label = QLabel()
        price_hvs_pixmap = QPixmap(f'{self.path_to_graph_folder}/PRICE_HVS.png')
        price_hvs_pixmap = price_hvs_pixmap.scaledToHeight(180)
        hot_bar_label.setPixmap(price_hvs_pixmap)
        hot_bar_label.setAlignment(QtCore.Qt.AlignCenter)
        bot_inner_grid.addWidget(hot_bar_label, 4, 1)

        space_label = QLabel('', self, margin = 4)
        bot_inner_grid.addWidget(space_label)

        v_layout.addLayout(bot_inner_grid)
        v_layout.addStretch(1)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        space_label = QLabel('', self, margin = 4)
        h_box.addWidget(space_label)
        self.quit_all_btn = QPushButton('Quit All', self)
        self.quit_all_btn.setStatusTip('Quit app')
        self.quit_all_btn.clicked.connect(QApplication.quit)
        h_box.addWidget(self.quit_all_btn)
        self.delete_btn = QPushButton('Delete data', self)
        self.delete_btn.clicked.connect(self.delete_data)
        h_box.addWidget(self.delete_btn)
        self.exit_btn = QPushButton('OK', self)
        self.exit_btn.clicked.connect(self.close)
        h_box.addWidget(self.exit_btn)
        v_layout.addLayout(h_box)
        v_layout.addStretch(1)

        self.setLayout(v_layout)

        #set window params
        self.setGeometry(300, 100, 850, 700)
        self.setWindowTitle('New Value Processing')

    def delete_data(self):
        self.data_class.delete_last_line_in_file()
        self.close()
