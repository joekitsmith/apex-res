from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QStatusBar, QDockWidget, QWidget, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QSlider, QPushButton, QSizePolicy

class SliderWidget(QWidget):
    
    def __init__(self, tgo):
        super(SliderWidget, self).__init__()
        
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(30,0,30,0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setHorizontalSpacing(50)
        
        self.slider_dict = {}
        slider_list = ['b0', 'bf', 'tg', 't0', 'td', 'flow', 'col_len', 'col_diam', 'part_size']
        for slider in slider_list:
            self.createSlider(slider, tgo)
        
        self.setLayout(self.gridLayout)
        
    def createSlider(self, slider_name, tgo):
        
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
         
    def changeSlider(self, checkbox, slider_name):
        
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