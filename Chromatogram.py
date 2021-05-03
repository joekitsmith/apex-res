from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QStatusBar, QDockWidget, QWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QSlider, QPushButton, QSizePolicy

import numpy as np
from MainWindow import RibbonToolBar, WindowWidget
from TwoGradOptimize import TwoGradOptimize
from FigCanvas import CustomFigCanvas
from Parameters import ParamWidget
from Resolution import ResWidget
from Sliders import Slider, SliderWidget

class ChromatogramWidget(QWidget):
    
    def __init__(self):
        super(ChromatogramWidget, self).__init__()
        
        self.gridLayout = QGridLayout()
        
        self.drawChromatogram()
        self.initialiseData()
        self.addSliderWidget()
        self.addParameterWidget()
        self.addResolutionWidget()
        self.configureLayout()
        self.setLayout(self.gridLayout)
        
    def drawChromatogram(self):
        self.fig1 = CustomFigCanvas()
        self.fig1.drawChromatogram()
        self.gridLayout.addWidget(self.fig1, 0, 0, 1, 1)
        
    def initialiseData(self):
        self.instrument_params = ['Agilent 1260 Inifinity I', 'Phenomenex Gemini C18', 250, 4, 5, 2, 19000, 2.56, 3.05]
        self.method_params = [1, 15, 0.6, 1, 254, 15, 30]
        input_params = [8, 5]
        rawdata = [[[9.06,10.53],[326.5,259.6],[0.200,0.242]], [[9.597,10.98],[335,292.4],[0.181,0.231]], [[10.34,12.64],[4291,4291],[0.156,0.17]], [[10.78,13.2],[1528,1528],[0.143,0.19]], [[11.21,13.68],[34269,34269],[0.183,0.21]], [[12.52,15.72],[494.3,175.7],[0.204,0.249]], [[12.91, 16.24],[11562, 11562],[0.198, 0.24]], [[13.73,17.50],[983.5,1028.5],[0.214,0.332]]]
        self.tgo = TwoGradOptimize(self.instrument_params, self.method_params, input_params, rawdata)
        self.tgo.calculateParameters()
        self.tgo.generatePlot(self.fig1)
        
    def addSliderWidget(self):
        self.slider_widget = SliderWidget(self.tgo)
        self.gridLayout.addWidget(self.slider_widget, 0, 1, 1, 1)
        self.slider_dict = self.slider_widget.slider_dict
              
    def addParameterWidget(self):
        self.pw = ParamWidget()
        self.pw.addData(self.instrument_params, self.method_params, self.slider_dict)
        self.gridLayout.addWidget(self.pw, 1, 0, 1, 1)

    def addResolutionWidget(self):
        self.rw = ResWidget()
        self.rw.setupUi(self.tgo.peakinterest, self.tgo.critical_Rs)
        self.gridLayout.addWidget(self.rw, 1, 1, 1, 1)
        self.rw.maximise_button.clicked.connect(self.maximise_res)

    def initialiseSliderCheckBoxes(self, slider_check):
        
        b0 = slider_check.addSliderChoice('Initial % B')
        b0.stateChanged.connect(lambda:self.slider_widget.changeSlider(b0, 'b0'))
        b0.setChecked(True)
        
        bf = slider_check.addSliderChoice('Final % B')
        bf.stateChanged.connect(lambda:self.slider_widget.changeSlider(bf, 'bf'))
        bf.setChecked(True)
        
        tg = slider_check.addSliderChoice('Gradient time')
        tg.stateChanged.connect(lambda:self.slider_widget.changeSlider(tg, 'tg'))
        tg.setChecked(True)
        
        t0 = slider_check.addSliderChoice('Dead time')
        t0.stateChanged.connect(lambda:self.slider_widget.changeSlider(t0, 't0'))
        
        td = slider_check.addSliderChoice('Dwell time')
        td.stateChanged.connect(lambda:self.slider_widget.changeSlider(td, 'td'))
        
        flow = slider_check.addSliderChoice('Flow rate')
        flow.stateChanged.connect(lambda:self.slider_widget.changeSlider(flow, 'flow'))
        
        col_len = slider_check.addSliderChoice('Column length')
        col_len.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_len, 'col_len'))
        
        col_diam = slider_check.addSliderChoice('Column diameter')
        col_diam.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_diam, 'col_diam'))
        
        part_size = slider_check.addSliderChoice('Particle size')
        part_size.stateChanged.connect(lambda:self.slider_widget.changeSlider(part_size, 'part_size'))
        
        self.slider_choice_list = [b0, bf, tg, t0, td, flow, col_len, col_diam, part_size]
        
    def initialiseSliders(self):
        
        for slider_name, slider_values in self.slider_dict.items():
            if slider_name == 'b0':
                slider_values[0].valueChanged.connect(self.update_phi0)
            if slider_name == 'bf':
                slider_values[0].valueChanged.connect(self.update_phif)
            if slider_name == 'tg':
                slider_values[0].valueChanged.connect(self.update_tg)

    def configureLayout(self):
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setRowStretch(0,2)
        self.gridLayout.setRowStretch(1,1)
    
        
    ## Update functions
    
    def update_Ui(self):
        slider_b0 = self.slider_dict['b0'][0]
        slider_bf = self.slider_dict['bf'][0]
        slider_tg = self.slider_dict['tg'][0]
        self.pw.tG_field.setText(str(slider_tg.value()) + 'min')
        self.pw.B0_field.setText(str(slider_b0.value() / (slider_b0.res / 100)) + '%')
        self.pw.Bf_field.setText(str(slider_bf.value() / (slider_bf.res / 100)) + '%')
        self.pw.tG_field.adjustSize()
        self.pw.B0_field.adjustSize()
        self.pw.Bf_field.adjustSize()

        self.tgo.updatePlot(self.fig1)
        self.rw.resolution_label2.setText('%s' %(round(self.tgo.critical_Rs[0],2)))

    def update_phi0(self, val):
        print('test')
        slider_b0 = self.slider_dict['b0'][0]
        slider_bf = self.slider_dict['bf'][0]
        slider_tg = self.slider_dict['tg'][0]
        self.tgo.phi0 = np.array([val / slider_b0.res], dtype='float64')
        self.tgo.phif = np.array([slider_bf.value() / slider_bf.res], dtype='float64')
        self.tgo.tG_final = slider_tg.value()
        if self.tgo.phi0 > self.tgo.phif:
            self.tgo.phif = self.tgo.phi0
            slider_bf.setValue(self.tgo.phi0[0] * slider_bf.res)
        
        self.update_Ui()

    def update_phif(self, val):
        slider_b0 = self.slider_dict['b0'][0]
        slider_bf = self.slider_dict['bf'][0]
        slider_tg = self.slider_dict['tg'][0]
        self.tgo.phif = np.array([val / slider_bf.res], dtype='float64')
        self.tgo.phi0 = np.array([slider_b0.value() /  slider_b0.res], dtype='float64')
        self.tgo.tG_final = slider_tg.value()
        if self.tgo.phif < self.tgo.phi0:
            self.tgo.phi0 = self.tgo.phif
            slider_b0.setValue(self.tgo.phif[0] * slider_b0.res)

        self.update_Ui()

    def update_tg(self, val):
        slider_b0 = self.slider_dict['b0'][0]
        slider_bf = self.slider_dict['bf'][0]
        self.tgo.tG_final = val
        self.tgo.phi0 = np.array([slider_b0.value() / slider_b0.res], dtype='float64')
        self.tgo.phif = np.array([slider_bf.value() / slider_bf.res], dtype='float64')

        self.update_Ui()

    def maximise_res(self):
        slider_b0 = self.slider_dict['b0'][0]
        slider_bf = self.slider_dict['bf'][0]
        self.tgo.maximiseRes()
        slider_b0.setValue(self.tgo.phi0 * slider_b0.res)
        slider_bf.setValue(self.tgo.phif * slider_bf.res)
        self.rw.resolution_label2.setText('%s' %(round(self.tgo.critical_Rs[0],2)))

        self.update_Ui()
        
        
    ## Legacy functions
        
    def addDockWidgets(self):
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