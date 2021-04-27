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


start = time.process_time()

class Form(WindowWidget):

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
        param = ribbon_toolbar.addSliderChoiceWidget(menu)
        
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
        self.configureLayout()

        b0 = param.addSliderChoice('Initial % B')
        b0.stateChanged.connect(lambda:self.slider_widget.changeSlider(b0, 'b0', self.tgo))
        b0.setChecked(True)
        bf = param.addSliderChoice('Final % B')
        bf.stateChanged.connect(lambda:self.slider_widget.changeSlider(bf, 'bf', self.tgo))
        bf.setChecked(True)
        tg = param.addSliderChoice('Gradient time')
        tg.stateChanged.connect(lambda:self.slider_widget.changeSlider(tg, 'tg', self.tgo))
        tg.setChecked(True)
        t0 = param.addSliderChoice('Dead time')
        t0.stateChanged.connect(lambda:self.slider_widget.changeSlider(t0, 't0', self.tgo))
        td = param.addSliderChoice('Dwell time')
        td.stateChanged.connect(lambda:self.slider_widget.changeSlider(td, 'td', self.tgo))
        flow = param.addSliderChoice('Flow rate')
        flow.stateChanged.connect(lambda:self.slider_widget.changeSlider(flow, 'flow', self.tgo))
        col_len = param.addSliderChoice('Column length')
        col_len.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_len, 'col_len', self.tgo))
        col_diam = param.addSliderChoice('Column diameter')
        col_diam.stateChanged.connect(lambda:self.slider_widget.changeSlider(col_diam, 'col_diam', self.tgo))
        part_size = param.addSliderChoice('Particle size')
        part_size.stateChanged.connect(lambda:self.slider_widget.changeSlider(part_size, 'part_size', self.tgo))
        self.slider_choice_list = [b0, bf, tg, t0, td, flow, col_len, col_diam, part_size]
        
        for slider_name, slider_values in self.slider_dict.items():
            if slider_name == 'b0':
                slider_values[0].valueChanged.connect(self.update_phi0)
            if slider_name == 'bf':
                slider_values[0].valueChanged.connect(self.update_phif)
            if slider_name == 'tg':
                slider_values[0].valueChanged.connect(self.update_tg)

        
    def initialiseData(self):
        self.instrument_params = ['Agilent 1260 Inifinity I', 'Phenomenex Gemini C18', 250, 4, 5, 2, 19000, 2.56, 3.05]
        self.method_params = [1, 15, 0.6, 1, 254, 15, 30]
        input_params = [8, 5]
        rawdata = [[[9.06,10.53],[326.5,259.6],[0.200,0.242]], [[9.597,10.98],[335,292.4],[0.181,0.231]], [[10.34,12.64],[4291,4291],[0.156,0.17]], [[10.78,13.2],[1528,1528],[0.143,0.19]], [[11.21,13.68],[34269,34269],[0.183,0.21]], [[12.52,15.72],[494.3,175.7],[0.204,0.249]], [[12.91, 16.24],[11562, 11562],[0.198, 0.24]], [[13.73,17.50],[983.5,1028.5],[0.214,0.332]]]
        self.tgo = TwoGradOptimize.TwoGradOptimize(self.instrument_params, self.method_params, input_params, rawdata)
        self.tgo.calculateParameters()
        self.tgo.generatePlot(self.fig1)

    def addSliderWidget(self):
        
        self.slider_widget = SliderWidget()
        self.gridLayout.addWidget(self.slider_widget, 0, 1, 1, 1)
        self.slider_dict = self.slider_widget.slider_dict

    def addParameterWidget(self):
        self.pw = Parameters.ParamWidget()
        self.pw.setupUi()
        #self.pw.addData(self.instrument_params, self.method_params, self.slider_list)
        self.gridLayout.addWidget(self.pw, 1, 0, 1, 1)

    def addResolutionWidget(self):
        self.rw = Resolution.ResWidget()
        self.rw.setupUi(self.tgo.peakinterest, self.tgo.critical_Rs)
        self.gridLayout.addWidget(self.rw, 1, 1, 1, 1)
        self.rw.maximise_button.clicked.connect(self.maximise_res)

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


class SliderWidget(QWidget):
    
    def __init__(self):
        super(SliderWidget, self).__init__()
        
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(30,0,30,0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setHorizontalSpacing(50)
        
        self.slider_dict = {}
        
        self.setLayout(self.gridLayout)
        
    def changeSlider(self, checkbox, slider_name, tgo):
        
        if checkbox.isChecked() == True:
        
            slider_label = QLabel()
            slider_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
            if slider_name == 'b0':
                slider = Slider(res=200, minimum=0, maximum=200, interval=10, value=tgo.phi0_init[0])
                slider_label.setText('Initial \n % B')
            
            if slider_name == 'bf':
                slider = Slider(res=200, minimum=0, maximum=200, interval=10, value=tgo.phif_init[0])
                slider_label.setText('Final \n % B')
            
            if slider_name == 'tg':
                slider = Slider(res=1, minimum=0, maximum=120, interval=10, value=tgo.tG1)
                slider_label.setText('Gradient \n time')
            
            if slider_name == 't0':
                slider = Slider(res=1, minimum=0, maximum=5, interval=0.1, value=tgo.t0)
                slider_label.setText('Dead \n time')
            
            if slider_name == 'td':
                slider = Slider(res=1, minimum=0, maximum=5, interval=0.1, value=tgo.td)
                slider_label.setText('Dwell \n time')
        
            if slider_name == 'flow':
                slider = Slider(res=1, minimum=0, maximum=5, interval=0.1, value=tgo.flow_rate)
                slider_label.setText('Flow \n rate')
            
            if slider_name == 'col_len':
                slider = Slider(res=1, minimum=0, maximum=50, interval=1, value=tgo.col_length)
                slider_label.setText('Column \n length')
            
            if slider_name == 'col_diam':
                slider = Slider(res=1, minimum=0, maximum=5, interval=0.1, value=tgo.col_diameter)
                slider_label.setText('Column \n diameter')
            
            if slider_name == 'part_size':
                slider = Slider(res=1, minimum=0, maximum=200, interval=5, value=tgo.particle_size)
                slider_label.setText('Particle \n size')
            
            self.slider_dict[slider_name] = (slider, slider_label)
            
            cols = self.gridLayout.columnCount()
            self.gridLayout.addWidget(slider, 0, (cols*2)+2, 1, 1, alignment=Qt.AlignHCenter)
            self.gridLayout.addWidget(slider_label, 1, (cols*2)+2, 1, 1, alignment=Qt.AlignHCenter)
            
        else:
            
            if len(self.slider_dict) > 0:
                slider, slider_label = self.slider_dict[slider_name]
                del self.slider_dict[slider_name]
                self.gridLayout.removeWidget(slider)
                self.gridLayout.removeWidget(slider_label)
        
            
        
class Slider(QSlider):

    def __init__(self, res, minimum, maximum, interval, value):
        super(Slider, self).__init__()

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
    