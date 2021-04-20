import time
import numpy as np
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QStatusBar, QDockWidget, QWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QSlider, QPushButton

from MainWindow import RibbonToolBar, FramelessWindow
from MethodOpt import TwoGradOptimize
from Chromatogram import FigCanvas
from Chromatogram import Parameters
from Chromatogram import Resolution


start = time.process_time()

class Form(FramelessWindow):

    def __init__(self):
        super(Form, self).__init__()
        #self.resize(1920,1050)
        self.setWindowTitle("Apex Res")
        self.showMaximized()
        self.init_ui()
        

    def init_ui(self):

        ribbon_toolbar = RibbonToolBar(self)
        # ----------------------------------------------
        menu = ribbon_toolbar.addMenu('Home')
        group = ribbon_toolbar.addGroup('\nData\nEntry\n\n', menu)
        # -----------------------------------------
        menu = ribbon_toolbar.addMenu('Mode')
        group = ribbon_toolbar.addGroup('Isocratic\nto\nGradient\n\n2 runs', menu)
        group = ribbon_toolbar.addGroup('Gradient\nto\nGradient\n\n2 runs', menu)
        group = ribbon_toolbar.addGroup('Isocratic\nto\nGradient\n\n3 runs', menu)
        group = ribbon_toolbar.addGroup('Gradient\nto\nGradient\n\n3 runs', menu)
        group = ribbon_toolbar.addGroup('\npH\n\n\n3 runs', menu)
        group = ribbon_toolbar.addGroup('\nTemperature\n\n\n2 runs', menu)
        group = ribbon_toolbar.addGroup('Gradient\nand\nTemperature\n\n4 runs', menu)
        group = ribbon_toolbar.addGroup('Isocratic\nand\nTemperature\n\n4 runs', menu)
        group = ribbon_toolbar.addGroup('Gradient\nand\npH\n\n6 runs', menu)
        group = ribbon_toolbar.addGroup('Isocratic\nand\npH\n\n6 runs', menu)
        # ---------------------------------------------
        menu = ribbon_toolbar.addMenu('Instrument')
        group = ribbon_toolbar.addGroup('\nEdit\nInstrument\n\n', menu)


        ## Initialize layout

        self.setWindowIcon(QIcon('image/left.ico'))
        self.addToolBar(ribbon_toolbar)

        self.centralwidget = QWidget(self)
        gridLayout = QGridLayout(self.centralwidget)
        gridLayout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

        self.fig1 = FigCanvas.CustomFigCanvas()
        self.fig1.drawChromatogram()
        gridLayout.addWidget(self.fig1, 0, 0, 2, 1)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setMouseTracking(True)


        ## Initialize data

        instrument_params = ['Agilent 1260 Inifinity I', 'Phenomenex Gemini C18', 250, 4, 5, 2, 19000, 2.56, 3.05]
        method_params = [1, 15, 0.6, 1, 254, 15, 30]
        input_params = [8, 5]
        rawdata = [[[9.06,10.53],[326.5,259.6],[0.200,0.242]], [[9.597,10.98],[335,292.4],[0.181,0.231]], [[10.34,12.64],[4291,4291],[0.156,0.17]], [[10.78,13.2],[1528,1528],[0.143,0.19]], [[11.21,13.68],[34269,34269],[0.183,0.21]], [[12.52,15.72],[494.3,175.7],[0.204,0.249]], [[12.91, 16.24],[11562, 11562],[0.198, 0.24]], [[13.73,17.50],[983.5,1028.5],[0.214,0.332]]]
        self.tgo = TwoGradOptimize.TwoGradOptimize(instrument_params, method_params, input_params, rawdata)
        self.tgo.calculateParameters()
        self.tgo.generatePlot(self.fig1)


        ## Sliders

        self.slider_B0 = Slider(res=200, minimum=0, maximum=200, interval=10, value=self.tgo.phi0_init[0])
        self.slider_B0.valueChanged.connect(self.update_phi0)

        self.slider_Bf = Slider(res=200, minimum=0, maximum=200, interval=10, value=self.tgo.phif_init[0])
        self.slider_Bf.valueChanged.connect(self.update_phif)

        self.slider_tG = Slider(res=1, minimum=0, maximum=120, interval=10, value=self.tgo.tG1)
        self.slider_tG.valueChanged.connect(self.update_tG)

        slider_list = [self.slider_B0, self.slider_Bf, self.slider_tG]

        slider_B0_label = QLabel()
        slider_B0_label.setText('Initial \n % B')

        slider_Bf_label = QLabel()
        slider_Bf_label.setText('Final \n % B')

        slider_tG_label = QLabel()
        slider_tG_label.setText('Gradient \n time')


         ## Parameters

        self.pw = Parameters.ParamWidget()
        self.pw.setupUi()
        self.pw.addData(instrument_params, method_params, slider_list)
        gridLayout.addWidget(self.pw, 2, 0, 1, 5)

        
        ## Resolution

        self.rw = Resolution.ResWidget()
        self.rw.setupUi(self.tgo.peakinterest, self.tgo.critical_Rs)
        gridLayout.addWidget(self.rw, 2, 2, 1, 5)
        self.rw.maximise_button.clicked.connect(self.maximise_res)


        ## Layout

        gridLayout.addWidget(self.slider_B0, 0, 2, 1, 1)
        gridLayout.addWidget(self.slider_Bf, 0, 4, 1, 1)
        gridLayout.addWidget(self.slider_tG, 0, 6, 1, 1)
        gridLayout.addWidget(slider_B0_label, 1, 2, 1, 1)
        gridLayout.addWidget(slider_Bf_label, 1, 4, 1, 1)
        gridLayout.addWidget(slider_tG_label, 1, 6, 1, 1)
        gridLayout.setColumnMinimumWidth(1, 30)
        gridLayout.setColumnMinimumWidth(3, 50)
        gridLayout.setColumnMinimumWidth(5, 30)
        gridLayout.setColumnMinimumWidth(7, 30)

#        gridLayout.setRowMinimumHeight(1, 50)
#        gridLayout.setRowMinimumHeight(3, 5)
#        gridLayout.setRowMinimumHeight(4, 5)
#        gridLayout.setRowMinimumHeight(5, 160)

        ## Dock widgets
        
        dwLeftUpper = QDockWidget(self)
        dwLeftUpper.setMaximumWidth(400)
        dwLeftUpper.setMouseTracking(True)
        dwLeftUpper.setWindowTitle('Data Entry')
        dwLeftUpper.setMinimumHeight(500)  

        dwLeftBottom = QDockWidget(self)
        dwLeftBottom.setMouseTracking(True)
        dwLeftBottom.setWindowTitle('Resolution Map')
        dwLeftBottom.setMaximumWidth(400)   

        self.fig2 = FigCanvas.CustomFigCanvas()
        self.fig2.drawResMap()
        self.tgo.plotResMap(self.fig2)
        dwLeftBottom.setWidget(self.fig2)

        self.addDockWidget(Qt.LeftDockWidgetArea, dwLeftUpper)
        self.addDockWidget(Qt.LeftDockWidgetArea, dwLeftBottom)  

        ribbon_toolbar.installEventFilter(self)

        print(time.process_time() - start)

    ## Update functions

    def update_Ui(self):
        self.pw.tG_field.setText(str(self.slider_tG.value()) + 'min')
        self.pw.B0_field.setText(str(self.slider_B0.value() / (self.slider_B0.res / 100)) + '%')
        self.pw.Bf_field.setText(str(self.slider_Bf.value() / (self.slider_Bf.res / 100)) + '%')
        self.pw.tG_field.adjustSize()
        self.pw.B0_field.adjustSize()
        self.pw.Bf_field.adjustSize()

        self.tgo.updatePlot(self.fig1)
        self.rw.resolution_label2.setText('%s' %(round(self.tgo.critical_Rs[0],2)))

    def update_phi0(self, val):
        self.tgo.phi0 = np.array([val / self.slider_B0.res], dtype='float64')
        self.tgo.phif = np.array([self.slider_Bf.value() / self.slider_Bf.res], dtype='float64')
        self.tgo.tG_final = self.slider_tG.value()
        if self.tgo.phi0 > self.tgo.phif:
            self.tgo.phif = self.tgo.phi0
            self.slider_Bf.setValue(self.tgo.phi0[0] * self.slider_Bf.res)
        
        self.update_Ui()

    def update_phif(self, val):
        self.tgo.phif = np.array([val / self.slider_Bf.res], dtype='float64')
        self.tgo.phi0 = np.array([self.slider_B0.value() /  self.slider_B0.res], dtype='float64')
        self.tgo.tG_final = self.slider_tG.value()
        if self.tgo.phif < self.tgo.phi0:
            self.tgo.phi0 = self.tgo.phif
            self.slider_B0.setValue(self.tgo.phif[0] * self.slider_B0.res)

        self.update_Ui()

    def update_tG(self, val):
        self.tgo.tG_final = val
        self.tgo.phi0 = np.array([self.slider_B0.value() / self.slider_B0.res], dtype='float64')
        self.tgo.phif = np.array([self.slider_Bf.value() / self.slider_Bf.res], dtype='float64')

        self.update_Ui()

    def maximise_res(self):
        self.tgo.maximiseRes()
        self.slider_B0.setValue(self.tgo.phi0 * self.slider_B0.res)
        self.slider_Bf.setValue(self.tgo.phif * self.slider_Bf.res)
        self.rw.resolution_label2.setText('%s' %(round(self.tgo.critical_Rs[0],2)))

        self.update_Ui()


class Slider(QSlider):

    def __init__(self, res, minimum, maximum, interval, value):

        super().__init__()

        self.res = res
        self.minimum = minimum
        self.maximum = maximum

        self.setRange(minimum, maximum)
        self.setValue(value * res)
        self.setMouseTracking(True)
        self.setTickPosition(QSlider.TicksBothSides)
        self.setTickInterval(interval)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Form()
    form.show()
    app.exec_()
    