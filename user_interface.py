""" Module to build the grafic interface to interact with the user """
__authors__ = "Jordan Alwon"
__copyright__ = "Copyright 2020"

import sys
from PySide2 import QtWidgets, QtCore, QtGui
from CuQtWidgets.Entry import Entry
from CuQtWidgets.ContentArea import ContentArea
from CuQtWidgets.MonthOverview import MonthOverview
import data_interface

class MainWindow(QtWidgets.QMainWindow):
    entry_widget_is_shown = False
    entry_widget = None

    def __init__(self):
        super().__init__()

        self.data = data_interface.Database('Jordan')

        self.month_overview_widget = MonthOverview()

        screen_size= self.screen().size().height()
        self.content_area = ContentArea(self.data)
        self.content_area.setMaximumHeight(999)

        self.content_area.addClicked.connect(self.change_entry_widget_visibility)
        
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.month_overview_widget)
        self.layout.addWidget(self.content_area, stretch= 8)

        self.month_overview_widget.setMaximumWidth(230)
        self.month_overview_widget.setMinimumWidth(230)

        window_content = QtWidgets.QWidget()
        window_content.setLayout(self.layout)
        self.setCentralWidget(window_content)

    def change_entry_widget_visibility(self, is_add_widget=True):
        self.content_area.switch_button_state()
        if self.entry_widget_is_shown:
            self.entry_widget_is_shown= False
            self.layout.removeWidget(self.entry_widget)
            self.entry_widget.remove_widget()
        else:
            self.entry_widget_is_shown = True
            self.entry_widget = Entry(self.data.df['Work Date'], is_add_widget)
            self.layout.addWidget(self.entry_widget, stretch= 3)
            self.entry_widget.close_signal.connect(self.change_entry_widget_visibility)
            self.entry_widget.save_entry_signal.connect(self.data.add_entry)

        
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())
    
