"""
QWidget Class for show_stats method

"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QAction, 
QScrollArea, QLabel, QGridLayout, QApplication, QTableWidget, QTableWidgetItem, QSizePolicy)
from PyQt5.QtGui import QPixmap

class TableStatsAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 100, 1000, 800)
        self.setWindowTitle('Table Statistics')

        gen_data_dict, year_data_dict, month_value_dict, month_cost_dict = self.data_class.create_dict_for_stats()
        gen_data_table = self.create_table(gen_data_dict)
        year_cold_water_data_table = self.create_table(year_data_dict['cold'])
        year_hot_water_data_table = self.create_table(year_data_dict['hot'])
        year_total_water_data_table = self.create_table(year_data_dict['total'])
        month_value_data_table = self.create_table(month_value_dict, 15)
        month_cost_data_table = self.create_table(month_cost_dict, 15)

        table_widget = QWidget()
        table_widget.setContentsMargins(0, 0, 0, 0)
        v_layout = QVBoxLayout()

        header_label = QLabel('<b>TABLE STATISTICS</b>', self, margin = 10)
        header_label.setStyleSheet("font: 18pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label)

        table_1_header_label = QLabel('<b>Average values</b>', self, margin = 4)
        table_1_header_label.setStyleSheet("font: 14pt")
        table_1_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_1_header_label)
        v_layout.addWidget(gen_data_table, alignment = QtCore.Qt.AlignCenter)

        table_2_header_label = QLabel('<b>Average values per years for cold water</b>', self, margin = 4)
        table_2_header_label.setStyleSheet("font: 14pt")
        table_2_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_2_header_label)

        v_layout.addWidget(year_cold_water_data_table, alignment = QtCore.Qt.AlignCenter)

        table_3_header_label = QLabel('<b>Average values per years for hot water</b>', self, margin = 4)
        table_3_header_label.setStyleSheet("font: 14pt")
        table_3_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_3_header_label)

        v_layout.addWidget(year_hot_water_data_table, alignment = QtCore.Qt.AlignCenter)

        table_4_header_label = QLabel('<b>Average values per years</b>', self, margin = 4)
        table_4_header_label.setStyleSheet("font: 14pt")
        table_4_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_4_header_label)

        v_layout.addWidget(year_total_water_data_table, alignment = QtCore.Qt.AlignCenter)

        table_5_header_label = QLabel('<b>Average values per every month</b>', self, margin = 4)
        table_5_header_label.setStyleSheet("font: 14pt")
        table_5_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_5_header_label)

        v_layout.addWidget(month_value_data_table, alignment = QtCore.Qt.AlignCenter)

        table_6_header_label = QLabel('<b>Average cost per every month</b>', self, margin = 4)
        table_6_header_label.setStyleSheet("font: 14pt")
        table_6_header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(table_6_header_label)

        v_layout.addWidget(month_cost_data_table, alignment = QtCore.Qt.AlignCenter)

        table_widget.setLayout(v_layout)
        
        scroll_area = QScrollArea()
        #scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        scroll_area.setWidget(table_widget)

        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll_area)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout) 


    def create_table(self, data_dict, gap = 0):
        columns_name = data_dict['columns']
        rows_name = data_dict['rows']
        data = data_dict['data']

        # Create table
        total_row_height = 0
        max_table_width = 950
        table_widget = QTableWidget()
        table_widget.setRowCount(len(rows_name))
        table_widget.setColumnCount(len(columns_name))
        for i in range(len(rows_name)):
            total_columns_width = 0
            for j in range(len(columns_name)):
                value_to_call = QTableWidgetItem('{:.3f}'.format(data[i][j]))
                value_to_call.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(i, j, value_to_call)
                total_columns_width += table_widget.columnWidth(j)
            total_row_height += table_widget.rowHeight(i)
        table_widget.setHorizontalHeaderLabels(columns_name)
        table_widget.setVerticalHeaderLabels(rows_name)
        total_row_height = total_row_height/(len(rows_name))*(len(rows_name)+1)+gap
        table_widget.setMaximumHeight(total_row_height+150)
        table_widget.setMinimumHeight(total_row_height)
        if total_columns_width > max_table_width-150:
            total_columns_width = max_table_width-150
        table_widget.setMinimumWidth(total_columns_width+150)
        table_widget.setMaximumWidth(total_columns_width+150)
        table_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #table_widget.resizeColumnsToContents()
        return table_widget


class GraphStatsAnalysis(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):
        
        #set window params
        self.setGeometry(300, 100, 1400, 800)
        self.setWindowTitle('Graph Statistics')
        self.path_to_graph_folder = self.data_class.path_to_graph_folder_stats
        self.data_class.create_graphs_for_stats()

        graph_widget = QWidget()
        v_layout = QVBoxLayout()

        header_label = QLabel('<b>GRAPH STATISTICS</b>', self, margin = 10)
        header_label.setStyleSheet("font: 18pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label, stretch = 2)

        point_labels = ['Current year cost per month', 'Average cost per every month', 'Average value per every month', 'Average cost per every year', 'Average value per every year']
        graph_names = [['current_cold_cost','current_hot_cost','current_total_cost'],
        ['month_cold_cost', 'month_hot_cost', 'month_total_cost'],
        ['month_cold_value', 'month_hot_value', 'month_total_value'],
        ['year_cold_cost', 'year_hot_cost', 'year_total_cost'],
        ['year_cold_value', 'year_hot_value', 'year_total_value']]

        for label, graph_list in zip(point_labels, graph_names):

            table_header_label = QLabel(f'<b>{label}</b>', self, margin = 4)
            table_header_label.setStyleSheet("font: 14pt")
            table_header_label.setAlignment(QtCore.Qt.AlignCenter)
            v_layout.addWidget(table_header_label, stretch = 1)
            
            table_h_box = QHBoxLayout()
            t1_bar_label = QLabel()
            t1_pixmap = QPixmap(f'{self.path_to_graph_folder}/{graph_list[0]}.png')
            t1_pixmap = t1_pixmap.scaledToHeight(205)
            t1_bar_label.setPixmap(t1_pixmap)
            t1_bar_label.setAlignment(QtCore.Qt.AlignCenter)
            table_h_box.addWidget(t1_bar_label)

            t2_bar_label = QLabel()
            t2_pixmap = QPixmap(f'{self.path_to_graph_folder}/{graph_list[1]}.png')
            t2_pixmap = t2_pixmap.scaledToHeight(205)
            t2_bar_label.setPixmap(t2_pixmap)
            t2_bar_label.setAlignment(QtCore.Qt.AlignCenter)
            table_h_box.addWidget(t2_bar_label)

            t3_bar_label = QLabel()
            t3_pixmap = QPixmap(f'{self.path_to_graph_folder}/{graph_list[2]}.png')
            t3_pixmap = t3_pixmap.scaledToHeight(205)
            t3_bar_label.setPixmap(t3_pixmap)
            t3_bar_label.setAlignment(QtCore.Qt.AlignCenter)
            table_h_box.addWidget(t3_bar_label)
            v_layout.addLayout(table_h_box)

        v_layout.addStretch()
        graph_widget.setLayout(v_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(graph_widget)

        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll_area)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout) 




