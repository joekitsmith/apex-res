import time
import numpy as np
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QStatusBar, QDockWidget, QWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QSlider, QPushButton, QSizePolicy, QStackedLayout

from MainWindow import RibbonToolBar, WindowWidget
from Chromatogram import ChromatogramWidget
from DataEntry import TwoGradOptimizeTable


start = time.process_time()

class ApexRes(WindowWidget):

    def __init__(self):
        super(ApexRes, self).__init__()

        self.setWindowTitle("Apex Res")
        self.showMaximized()
        self.configureToolBar()

        self.central_widget = QWidget(self)
        self.central_widget.setMouseTracking(True)
        
        self.stacked_layout = QStackedLayout(self.central_widget)
        self.addChromatogramWidget()
        
        self.setCentralWidget(self.central_widget)    
        
    def configureToolBar(self):
        
        ribbon_toolbar = RibbonToolBar(self)
        
        home_menu = ribbon_toolbar.addMenu('Home')
        chrom_group = ribbon_toolbar.addGroup('\nChromatogram\n\n', home_menu)
        chrom_group.button.clicked.connect(self.addChromatogramWidget)
        data_group = ribbon_toolbar.addGroup('\nData\nEntry\n\n', home_menu)
        data_group.button.clicked.connect(self.addDataEntryWidget)
        self.slider_check = ribbon_toolbar.addSliderChoiceWidget(home_menu)

        mode_menu = ribbon_toolbar.addMenu('Mode')
        ig2_group = ribbon_toolbar.addGroup('Isocratic\nto\nGradient\n\n2 runs', mode_menu)
        gg2_group = ribbon_toolbar.addGroup('Gradient\nto\nGradient\n\n2 runs', mode_menu)
        ig3_group = ribbon_toolbar.addGroup('Isocratic\nto\nGradient\n\n3 runs', mode_menu)
        gg3_group = ribbon_toolbar.addGroup('Gradient\nto\nGradient\n\n3 runs', mode_menu)
        ph3_group = ribbon_toolbar.addGroup('\npH\n\n\n3 runs', mode_menu)
        t2_group = ribbon_toolbar.addGroup('\nTemperature\n\n\n2 runs', mode_menu)
        gt4_group = ribbon_toolbar.addGroup('Gradient\nand\nTemperature\n\n4 runs', mode_menu)
        it4_group = ribbon_toolbar.addGroup('Isocratic\nand\nTemperature\n\n4 runs', mode_menu)
        gph6_group = ribbon_toolbar.addGroup('Gradient\nand\npH\n\n6 runs', mode_menu)
        iph6_group = ribbon_toolbar.addGroup('Isocratic\nand\npH\n\n6 runs', mode_menu)

        ins_menu = ribbon_toolbar.addMenu('Instrument')
        edit_ins_group = ribbon_toolbar.addGroup('\nEdit\nInstrument\n\n', ins_menu)
        
        self.addToolBar(ribbon_toolbar)
                
    def addChromatogramWidget(self):
        chromatogram_widget = ChromatogramWidget()
        self.stacked_layout.addWidget(chromatogram_widget)
        self.stacked_layout.setCurrentIndex(0)
        if self.slider_check.clayout.count() == 0:
            chromatogram_widget.initialiseSliderCheckBoxes(self.slider_check)
        chromatogram_widget.initialiseSliders()

    def addDataEntryWidget(self):
        data_widget = TwoGradOptimizeTable()
        self.stacked_layout.addWidget(data_widget)
        self.stacked_layout.setCurrentIndex(1)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = ApexRes()
    window.show()
    app.exec_()
    