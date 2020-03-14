"""
Main script

"""
import sys

from data_processing import DataProcessing
from new_data_analisys import NewValueAnalysis
from show_stats_class import TableStatsAnalysis, GraphStatsAnalysis
from water_form import WaterForm
from history_class import DisplayHistory
from settings_class import Settings
from show_prediction_class import Prediction

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow, QMessageBox, QApplication)
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_class = DataProcessing()
        self.initUI()
        
    def initUI(self):
        # set central widget
        self.c_widget = WaterForm(self.data_class)
        self.setCentralWidget(self.c_widget)
        self.create_toolbar()

        # set window params
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Water Data App')
        self.show()
    
    def create_toolbar(self):
        # Current month data
        current_month_action = QAction(QIcon('icons/month_data.png'), 'Month Data', self)
        current_month_action.setShortcut('Ctrl+M')
        current_month_action.setStatusTip('See Current Month')
        current_month_action.triggered.connect(self.show_current_month_data)
        toolbar = self.addToolBar('Month Data')
        toolbar.addAction(current_month_action)

        # See history
        history_action = QAction(QIcon('icons/history.png'), 'History', self)
        history_action.setShortcut('Ctrl+H')
        history_action.setStatusTip('See History')
        history_action.triggered.connect(self.show_history)
        toolbar = self.addToolBar('History')
        toolbar.addAction(history_action)

        # See stats table
        stats_table_action = QAction(QIcon('icons/stats_table.png'), 'Table Statistics', self)
        stats_table_action.setShortcut('Ctrl+T')
        stats_table_action.setStatusTip('See Table Statictics')
        stats_table_action.triggered.connect(self.show_stats_tables)
        toolbar = self.addToolBar('Table Statistics')
        toolbar.addAction(stats_table_action)

        # See stats graph
        stats_graph_action = QAction(QIcon('icons/stats_graph.png'), 'Graph Statistics', self)
        stats_graph_action.setShortcut('Ctrl+G')
        stats_graph_action.setStatusTip('See Graph Statictics')
        stats_graph_action.triggered.connect(self.show_stats_graph)
        toolbar = self.addToolBar('Graph Statistics')
        toolbar.addAction(stats_graph_action)

        # See forecast
        pred_action = QAction(QIcon('icons/f_cast.png'), 'Prediction', self)
        pred_action.setShortcut('Ctrl+P')
        pred_action.setStatusTip('See Prediction')
        pred_action.triggered.connect(self.show_prediction)
        toolbar = self.addToolBar('Prediction')
        toolbar.addAction(pred_action)

        # Settings
        settings_action = QAction(QIcon('icons/conf.png'), 'Settings', self)
        settings_action.setShortcut('Ctrl+S')
        settings_action.setStatusTip('See Settings')
        settings_action.triggered.connect(self.show_settings)
        toolbar = self.addToolBar('Settings')
        toolbar.addAction(settings_action)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show_history(self):
        self.display_history_window = DisplayHistory(self.data_class)
        self.display_history_window.show()

    def show_current_month_data(self):
        self.new_data_analysis_window = NewValueAnalysis(self.data_class)
        self.new_data_analysis_window.show()

    def show_settings(self):
        self.settings_window = Settings(self.data_class)
        self.settings_window.show()

    def show_stats_tables(self):
        self.stats_table_window = TableStatsAnalysis(self.data_class)
        self.stats_table_window.show()

    def show_prediction(self):
        self.predict_window = Prediction(self.data_class)
        self.predict_window.show()

    def show_stats_graph(self):
        self.stats_graph_window = GraphStatsAnalysis(self.data_class)
        self.stats_graph_window.show()
     

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


