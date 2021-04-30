import time
import numpy as np
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QStatusBar, QDockWidget, QWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QSlider, QPushButton, QSizePolicy

from MainWindow import RibbonToolBar, WindowWidget
from MethodOpt import TwoGradOptimize
from Chromatogram import FigCanvas
from Chromatogram import Parameters
from Chromatogram import Resolution
from Chromatogram import Sliders


start = time.process_time()

class Form(WindowWidget):

    def __init__(self):
        super(Form, self).__init__()

        self.setWindowTitle("Apex Res")
        self.showMaximized()
        self.configureToolBar()

        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

        self.fig1 = FigCanvas.CustomFigCanvas()
        self.fig1.drawChromatogram()
        self.gridLayout.addWidget(self.fig1, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setMouseTracking(True)
        
        self.initialiseData()
        self.addSliderWidget()
        self.addParameterWidget()
        self.addResolutionWidget()
        self.initialiseSliderCheckBoxes()
        self.initialiseSliders()
        self.configureLayout()
        
    def configureToolBar(self):
        
        ribbon_toolbar = RibbonToolBar(self)
        
        home_menu = ribbon_toolbar.addMenu('Home')
        data_group = ribbon_toolbar.addGroup('\nData\nEntry\n\n', home_menu)
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
        
    def initialiseData(self):
        self.instrument_params = ['Agilent 1260 Inifinity I', 'Phenomenex Gemini C18', 250, 4, 5, 2, 19000, 2.56, 3.05]
        self.method_params = [1, 15, 0.6, 1, 254, 15, 30]
        input_params = [8, 5]
        rawdata = [[[9.06,10.53],[326.5,259.6],[0.200,0.242]], [[9.597,10.98],[335,292.4],[0.181,0.231]], [[10.34,12.64],[4291,4291],[0.156,0.17]], [[10.78,13.2],[1528,1528],[0.143,0.19]], [[11.21,13.68],[34269,34269],[0.183,0.21]], [[12.52,15.72],[494.3,175.7],[0.204,0.249]], [[12.91, 16.24],[11562, 11562],[0.198, 0.24]], [[13.73,17.50],[983.5,1028.5],[0.214,0.332]]]
        self.tgo = TwoGradOptimize.TwoGradOptimize(self.instrument_params, self.method_params, input_params, rawdata)
        self.tgo.calculateParameters()
        self.tgo.generatePlot(self.fig1)

    def addSliderWidget(self):
        
        self.slider_widget = Sliders.SliderWidget(self.tgo)
        self.gridLayout.addWidget(self.slider_widget, 0, 1, 1, 1)
        self.slider_dict = self.slider_widget.slider_dict

    def addParameterWidget(self):
        self.pw = Parameters.ParamWidget()
        print(self.slider_dict)
        self.pw.addData(self.instrument_params, self.method_params, self.slider_dict)
        self.gridLayout.addWidget(self.pw, 1, 0, 1, 1)

    def addResolutionWidget(self):
        self.rw = Resolution.ResWidget()
        self.rw.setupUi(self.tgo.peakinterest, self.tgo.critical_Rs)
        self.gridLayout.addWidget(self.rw, 1, 1, 1, 1)
        self.rw.maximise_button.clicked.connect(self.maximise_res)

    def initialiseSliderCheckBoxes(self):
        
        b0 = self.slider_check.addSliderChoice('Initial % B')
        b0.stateChanged.connect(lambda:self.slider_widget.changeSlider(b0, 'b0'))
        b0.setChecked(True)
        
        bf = self.slider_check.addSliderChoice('Final % B')
        bf.stateChanged.connect(lambda:self.slider_widget.changeSlider(bf, 'bf'))
        bf.setChecked(True)
        
        tg = self.slider_check.addSliderChoice('Gradient time')
        tg.stateChanged.connect(lambda:self.slider_widget.changeSlider(tg, 'tg'))
        tg.setChecked(True)
        
        t0 = self.slider_check.addSliderChoice('Dead time')
        t0.stateChanged.connect(lambda:self.slider_widget.changeSlider(t0, 't0'))
        
        td = self.slider_check.addSliderChoice('Dwell time')
        td.stateChanged.connect(lambda:self.slider_widget.changeSlider(td, 'td'))
        
        flow = self.slider_check.addSliderChoice('Flow rate')
        flow.stateChanged.connect(lambda:self.slider_widget.changeSlider(flow, 'flow'))
        
        col_len = self.slider_check.addSliderChoice('Column length')
        col_len.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_len, 'col_len'))
        
        col_diam = self.slider_check.addSliderChoice('Column diameter')
        col_diam.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_diam, 'col_diam'))
        
        part_size = self.slider_check.addSliderChoice('Particle size')
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

        self.gridLayout.setRowStretch(0,2)
        self.gridLayout.setRowStretch(1,1)
        
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


        
        slider, slider_label = self.slider_dict[slider_name]
        
        if checkbox.isChecked() == True:
            count = self.gridLayout.count()/2
            row = (count-(count%3))/3 + 1
            if count < 3:
                self.gridLayout.addWidget(slider, 0, count, 1, 1, alignment=Qt.AlignHCenter)
                self.gridLayout.addWidget(slider_label, 1, count, 1, 1, alignment=Qt.AlignHCenter)
            else:
                self.gridLayout.addWidget(slider, row, count%3, 1, 1, alignment=Qt.AlignHCenter)
                self.gridLayout.addWidget(slider_label, row+1, count%3, 1, 1, alignment=Qt.AlignHCenter)
            slider.show()
            slider_label.show()
            
        else:
            count = self.gridLayout.count()/2
            self.gridLayout.removeWidget(slider)
            self.gridLayout.removeWidget(slider_label)
            slider.hide()
            slider_label.hide()         
        

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Form()
    form.show()
    app.exec_()
    