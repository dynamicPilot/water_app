"""
QWidget Class for show settings method

"""
import config
import re

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QAction, QMessageBox, QLabel, 
QPushButton, QLineEdit, QInputDialog, QGridLayout, QApplication, QFileDialog)

class Settings(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.config_path = 'config.py'
        self.initUI()
        
    def initUI(self):
        #set window params
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Settings')

        self.new_hot_water_price = None
        self.new_cold_water_price = None
        self.current_hot_water_price = self.data_class.hot_water_price
        self.current_cold_water_price = self.data_class.cold_water_price

        self.current_month_number_to_plot = self.data_class.month_number_to_plot
        self.new_month_number_to_plot = None
        
        self.current_data_path = self.data_class.data_path
        self.new_data_path = None

        self.current_file_save_path = self.data_class.file_save_path
        self.new_file_save_path = None

        v_layout = QVBoxLayout()
        header_label = QLabel('APP SETTINGS', self, margin = 10)
        header_label.setStyleSheet("font: 16pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label)

        grid = QGridLayout()
        grid.setSpacing(20)
        
        hw_label = QLabel('Hot water price: ')
        grid.addWidget(hw_label, 0, 0)

        self.hw_edit = QLineEdit()
        self.hw_edit.setText(str(self.current_hot_water_price))
        grid.addWidget(self.hw_edit, 0, 1, 1, 2)

        self.hw_btn = QPushButton('Change value', self)
        self.hw_btn.clicked.connect(self.show_dialog_for_hot)
        grid.addWidget(self.hw_btn, 0, 3)

        cw_label = QLabel('Cold water price: ')
        grid.addWidget(cw_label, 1, 0)

        self.cw_edit = QLineEdit()
        self.cw_edit.setText(str(self.current_cold_water_price))
        grid.addWidget(self.cw_edit, 1, 1, 1, 2)

        self.cw_btn = QPushButton('Change value', self)
        self.cw_btn.clicked.connect(self.show_dialog_for_cold)
        grid.addWidget(self.cw_btn, 1, 3)

        month_number_label = QLabel('Month number to plot: ')
        grid.addWidget(month_number_label, 2, 0)

        self.month_number_edit = QLineEdit()
        self.month_number_edit.setText(str(self.current_month_number_to_plot))
        grid.addWidget(self.month_number_edit, 2, 1, 1, 2)

        self.month_number_btn = QPushButton('Change value', self)
        self.month_number_btn.clicked.connect(self.show_dialog_for_month_number)
        grid.addWidget(self.month_number_btn, 2, 3)

        data_path_label = QLabel('Data file path: ')
        grid.addWidget(data_path_label, 3, 0)

        self.data_path_edit = QLineEdit()
        self.data_path_edit.setText(str(self.current_data_path))
        grid.addWidget(self.data_path_edit, 3, 1, 1, 2)

        self.data_path_btn = QPushButton('Change value', self)
        self.data_path_btn.clicked.connect(self.show_dialog_for_data_path)
        grid.addWidget(self.data_path_btn, 3, 3)

        file_save_path_label = QLabel('Save history file folder: ')
        grid.addWidget(file_save_path_label, 4, 0)

        self.file_save_path_edit = QLineEdit()
        self.file_save_path_edit.setText(str(self.current_file_save_path))
        grid.addWidget(self.file_save_path_edit, 4, 1, 1, 2)

        self.file_save_path_btn = QPushButton('Change value', self)
        self.file_save_path_btn.clicked.connect(self.show_dialog_for_file_save_folder)
        grid.addWidget(self.file_save_path_btn, 4, 3)

        v_layout.addLayout(grid)
        v_layout.addStretch(1)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        space_label = QLabel('', self, margin = 4)
        h_box.addWidget(space_label)

        self.quit_all_btn = QPushButton('Quit All', self)
        self.quit_all_btn.setStatusTip('Quit app')
        self.quit_all_btn.clicked.connect(QApplication.quit)
        h_box.addWidget(self.quit_all_btn)

        self.save_btn = QPushButton('Save changes', self)
        self.save_btn.clicked.connect(self.save_values_to_data)
        h_box.addWidget(self.save_btn)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.close)
        h_box.addWidget(self.cancel_btn)

        v_layout.addLayout(h_box)

        self.setLayout(v_layout)


    def show_dialog_for_hot(self):
        #self.show_dialog_for_value_input(self.hw_edit, self.new_hot_water_price,self.show_main_dialog_for_float, 'hot water price')
        mark = True
        tag = 'hot water price'
        while mark:
            value = self.show_main_dialog_for_float(tag)
            if value > 0:
                mark = False
            elif value == -1:
                return
            else:
                mes_text = "Your value is incorrect. \nPlease, enter new value for {}. \nUse '.' as separator.".format(tag)
                mes = QMessageBox()
                mes.setWindowTitle('Message')
                mes.setText(mes_text)
                mes.exec()
        self.hw_edit.setText(str(value))
        self.new_hot_water_price = value

    def show_dialog_for_cold(self):
        mark = True
        tag = 'cold water price'
        while mark:
            value = self.show_main_dialog_for_float(tag)
            if value > 0:
                mark = False
            elif value == -1:
                return
            else:
                mes_text = "Your value is incorrect. \nPlease, enter new value for {}. \nUse '.' as separator.".format(tag)
                mes = QMessageBox()
                mes.setWindowTitle('Message')
                mes.setText(mes_text)
                mes.exec()
        self.cw_edit.setText(str(value))
        self.new_cold_water_price = value

    def show_dialog_for_month_number(self):
        mark = True
        tag = 'month number to plot'
        while mark:
            value = self.show_main_dialog_for_int(tag)
            if value > 0:
                mark = False
            elif value == -1:
                return
            else:
                mes_text = "Your value is incorrect. \nPlease, enter new value for {}.".format(tag)
                mes = QMessageBox()
                mes.setWindowTitle('Message')
                mes.setText(mes_text)
                mes.exec()
        self.month_number_edit.setText(str(value))
        self.new_month_number_to_plot = value
   

    def show_dialog_for_data_path(self):
        file_name = QFileDialog.getOpenFileName(self, 'New file')[0]
        value = str(file_name)
        print(value)
        if len(value)>3:
            self.new_data_path = value
            self.data_path_edit.setText(value)

    def show_dialog_for_file_save_folder(self):
        file_name = QFileDialog.getExistingDirectory(self, 'New folder')[0]
        value = str(file_name)
        print(value)
        if len(value)>0:
            self.new_file_save_path = value
            self.self.file_save_path_edit.setText(value)


    def show_main_dialog_for_float(self, tag):
        text, ok = QInputDialog.getText(self, 'Input value',
            f'Enter {tag} value:')
        
        if ok:
            if len(re.findall(r"[^\d\.]", str(text))) > 0 or len(str(text)) == 0:
                value = 0.
            else:
                value = float(text)
            return value
        else:
            return -1

    def show_main_dialog_for_int(self, tag):
        text, ok = QInputDialog.getText(self, 'Input value',
            f'Enter {tag} value:')
        if ok:
            if len(re.findall(r"[^\d]", str(text))) > 0 or len(str(text)) == 0:
                value = 0
            else:
                value = int(text)
            return value
        else:
            return -1
            
    def save_values_to_data(self):
        new_values = {'file_save_path =': [self.new_file_save_path, self.current_file_save_path], 
        'data_path =': [self.new_data_path, self.current_data_path],
        'cold_water_price =': [self.new_cold_water_price, self.current_cold_water_price],
        'hot_water_price =': [self.new_hot_water_price, self.current_hot_water_price],
        'month_number_to_plot =': [self.new_month_number_to_plot, self.current_month_number_to_plot]}

        new_values_list = []
        for value in new_values.values():
            if value[0] is not None:
                new_values_list.append(value[0])
            else:
                new_values_list.append(value[1])
        #print(new_values_list)

        f = open(self.config_path, 'w')
        for key, var in new_values.items():
            to_write = ''
            if var[0] is not None:
                if key in ['file_save_path =', 'data_path =']:
                    to_write = f"'{var[0]}'"
                else:
                    to_write = f'{var[0]}'
            else:
                if key in ['file_save_path =', 'data_path =']:
                    to_write = f"'{var[1]}'"
                else:
                    to_write=f'{var[1]}'
            f.write(f'{key} {to_write}\n')
        f.close()
        self.data_class.update_const(new_values_list)
        mes_text = "All changes were saved."
        mes = QMessageBox()
        mes.setWindowTitle('Message')
        mes.setText(mes_text)
        mes.exec()
        self.close()

        
        
        


