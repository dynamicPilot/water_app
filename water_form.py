"""
QWidget Class for water form method

"""
import re

from new_data_analisys import NewValueAnalysis

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QAction, QMessageBox, 
QLabel, QPushButton, QLineEdit, QInputDialog, QGridLayout, QApplication)

class WaterForm(QWidget):
    def __init__(self, data_class):
        super().__init__()
        #self.new_value_list = ['', 2020, 0, 0]
        self.data_class = data_class
        self.initUI()
        
    def initUI(self):

        month_label = QLabel('Set month: ')
        year_label = QLabel('Set year: ')
        hw_label = QLabel('Hot Water value: ')
        cw_label = QLabel('Cold Water value: ')

        self.month_list = QComboBox(self)
        self.month_list.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 'November', 'December'])
        self.month_list.activated[str].connect(self.month_activate)

        self.year_list = QComboBox(self)
        self.year_list.addItems(['2020', '2021', '2022', '2023', '2024', '2025'])
        self.year_list.activated[str].connect(self.year_activate)

        self.hw_edit = QLineEdit()
        self.cw_edit = QLineEdit()

        self.hw_btn = QPushButton('Add value', self)
        self.hw_btn.clicked.connect(self.show_dialog_for_hot)
        self.cw_btn = QPushButton('Add value', self)
        self.cw_btn.clicked.connect(self.show_dialog_for_cold)

        self.save_btn = QPushButton('Save data', self)

        v_layout = QVBoxLayout()
        header_label = QLabel('SET NEW VALUES', self, margin = 10)
        header_label.setStyleSheet("font: 14pt")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(header_label)

        grid = QGridLayout()
        grid.setSpacing(35)

        grid.addWidget(month_label, 1, 0)
        grid.addWidget(self.month_list, 1, 1)
        grid.addWidget(year_label, 1, 2)
        grid.addWidget(self.year_list, 1, 3)

        grid.addWidget(hw_label, 2, 0)
        grid.addWidget(self.hw_edit, 2, 1, 1, 2)
        grid.addWidget(self.hw_btn, 2, 3)

        grid.addWidget(cw_label, 3, 0)
        grid.addWidget(self.cw_edit, 3, 1, 1, 2)
        grid.addWidget(self.cw_btn, 3, 3)

        v_layout.addLayout(grid)
        v_layout.addStretch(1)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_values_to_data)
        v_layout.addLayout(h_box)
        self.setLayout(v_layout)

    def month_activate(self, text):
        self.data_class.new_value_list[0] = str(text)
        print(self.data_class.new_value_list)

    def year_activate(self, text):
        self.data_class.new_value_list[1] = int(text)
        print(self.data_class.new_value_list)

    def show_dialog_for_hot(self):
        mark = True
        while mark:
            value = self.show_win_dialog_for_hot()
            if value > self.data_class.last_hvs_value:
                mark = False
            elif value == -1:
                return
            else:
                mes_text = "Your value {:.3f} is incorrect. \nPlease, enter new value for hot water, which is more then {:.3f}.\nUse '.' as separator.".format(value, self.data_class.last_hvs_value)
                mes = QMessageBox()
                mes.setWindowTitle('Message')
                mes.setText(mes_text)
                mes.exec()

        self.hw_edit.setText(str(value))
        self.data_class.new_value_list[2] = value

    def show_dialog_for_cold(self):
        mark = True
        while mark:
            value = self.show_win_dialog_for_cold()
            if value > self.data_class.last_cvs_value:
                mark = False
            elif value == -1:
                return
            else:
                mes_text = "Your value {:.3f} is incorrect. \nPlease, enter new value for cold water, which is more then {:.3f}.\nUse '.' as separator.".format(value, self.data_class.last_cvs_value)
                mes = QMessageBox()
                mes.setWindowTitle('Message')
                mes.setText(mes_text)
                mes.exec()

        self.cw_edit.setText(str(value))
        self.data_class.new_value_list[3] = value

    # Show dialog window to input value
    def show_win_dialog_for_hot(self):
        text, ok = QInputDialog.getText(self, 'Input value',
            'Enter hot water counter value:')

        if ok:
            # Check incorrent input
            if len(re.findall(r"[^\d\.]", str(text))) > 0 or len(str(text)) == 0:
                value = 0.
            else:
                value = float(text)
            return value
        else:
            return -1
            
    # Show dialog window to input value
    def show_win_dialog_for_cold(self):
        text, ok = QInputDialog.getText(self, 'Input value',
            'Enter cold water counter value:')

        if ok:
            # Check incorrent input
            if len(re.findall(r"[^\d\.]", str(text))) > 0 or len(str(text)) == 0:
                value = 0.
            else:
                value = float(text)
            return value
        else:
            return -1
            
    def save_values_to_data(self):
        if len(self.data_class.new_value_list[0])>2 and self.data_class.new_value_list[2]>=self.data_class.last_hvs_value and self.data_class.new_value_list[3]>=self.data_class.last_cvs_value:
            self.data_class.add_data()
            self.new_data_analysis_window = NewValueAnalysis(self.data_class)
            self.new_data_analysis_window.show()
        else:
            mes_text = "Your valuesis incorrect.\nPlease, enter new values."
            mes = QMessageBox()
            mes.setWindowTitle('Message')
            mes.setText(mes_text)
            mes.exec()


