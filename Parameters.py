from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QFrame, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont

class ParamWidget(QWidget):
    
    def __init__(self, *args, **kwargs):
        super(ParamWidget, self).__init__()
        
        self.instrument_layout = QGridLayout()
        self.method_layout = QGridLayout()
        self.peak_layout = QGridLayout()
        
        self.total_layout = QGridLayout(self)
        
        self.configureFonts()
        self.configureInstrumentParameters()
        self.configureMethodParameters()
        self.configurePeakParameters()
        
        self.setupUi()
        
    def setupUi(self):
        
        self.setObjectName('ParamWidget')

        self.setStyleSheet('background-color: (0.906, 0.906, 0.906)')

        label_title = QLabel()
        label_title.setText('Parameters')
        label_title.setFont(self.font14)
        label_title.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        label_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)

        vline1 = QFrame()
        vline1.setFrameShape(QFrame.VLine)
        vline1.setFrameShadow(QFrame.Sunken)
         
        vline2 = QFrame()
        vline2.setFrameShape(QFrame.VLine)
        vline2.setFrameShadow(QFrame.Sunken)
         
        total_layout = self.total_layout
        total_layout.setContentsMargins(20,10,20,20)
        total_layout.setSpacing(8)
        total_layout.addWidget(label_title, 0,0,1,5)
        total_layout.addWidget(hline, 1,0,1,5)
        total_layout.addLayout(self.instrument_layout, 2,0,1,1)
        total_layout.addWidget(vline1, 2,1,1,1)
        total_layout.addLayout(self.method_layout, 2,2,1,1)
        total_layout.addWidget(vline2, 2,3,1,1)
        total_layout.addLayout(self.peak_layout, 2,4,1,1)
        
        total_layout.setColumnStretch(0,3)
        total_layout.setColumnStretch(2,2)
        total_layout.setColumnStretch(4,12)

    def configureInstrumentParameters(self):
        
        ins_layout = self.instrument_layout
        ins_layout.setContentsMargins(0,10,15,2)
        ins_layout.setVerticalSpacing(9)
        
        instrument_label = QLabel()
        instrument_label.setText('Instrument')
        instrument_label.setFont(self.font11)
        instrument_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        instrument_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        ins_name_label = QLabel()
        col_name_label = QLabel()
        col_len_label = QLabel()
        col_diam_label = QLabel()
        part_size_label = QLabel()
        plate_num_label = QLabel()
        dead_vol_label = QLabel()
        dwell_vol_label = QLabel()
        self.ins_name_field = QLabel()
        self.col_name_field = QLabel()
        self.col_len_field = QLabel()
        self.col_diam_field = QLabel()
        self.part_size_field = QLabel()
        self.plate_num_field = QLabel()
        self.dead_vol_field = QLabel()
        self.dwell_vol_field = QLabel()
        instrument_labels = [ins_name_label, col_name_label, col_len_label, col_diam_label, part_size_label, plate_num_label, dead_vol_label, dwell_vol_label]
        self.instrument_fields = [self.ins_name_field, self.col_name_field, self.col_len_field, self.col_diam_field, self.part_size_field, self.plate_num_field, self.dead_vol_field, self.dwell_vol_field]
        instrument_strings = ['Instrument name', 'Column name', 'Column length', 'Column diameter', 'Particle size', 'Plate number', 'Dead volume', 'Dwell volume']
        for n, label in enumerate(instrument_labels):
            label.setText(str(instrument_strings[n] + ':'))
            label.setFont(self.font9bold)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            label.adjustSize()

            field = self.instrument_fields[n]
            field.setFont(self.font9)
            field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            
        
        ins_layout.addWidget(instrument_label, 0,0,1,1)
            
        for i, label in enumerate(instrument_labels):
            hlayout = QHBoxLayout()
            hlayout.setSpacing(5)
            field = self.instrument_fields[i]
            hlayout.addWidget(label, 0)
            hlayout.addWidget(field, 1)
            ins_layout.addLayout(hlayout, i+1,0,1,1)
              
    def configureMethodParameters(self):
        
        method_layout = self.method_layout
        method_layout.setContentsMargins(10,10,15,2)
        method_layout.setVerticalSpacing(3)
        method_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        method_label = QLabel()
        method_label.setText('Method')
        method_label.setFont(self.font11)
        method_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        method_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        flow_label = QLabel()
        tg_label = QLabel()
        b0_label = QLabel()
        bf_label = QLabel()
        uv_label = QLabel()
        self.flow_field = QLabel()
        self.tg_field = QLabel()
        self.b0_field = QLabel()
        self.bf_field = QLabel()
        self.uv_field = QLabel()
        method_labels = [flow_label, tg_label, b0_label, bf_label, uv_label]
        self.method_fields = [self.flow_field, self.tg_field, self.b0_field, self.bf_field, self.uv_field]
        method_strings = ['Flow rate', 'Gradient time', 'Initial'+' % ' +'organic', 'Final'+' % ' +'organic', 'UV']
        for n, label in enumerate(method_labels):
            label.setText(str(method_strings[n] + ':'))
            label.setFont(self.font9bold)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            label.adjustSize()

            field = self.method_fields[n]
            field.setFont(self.font9)
            field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            
        
        method_layout.addWidget(method_label, 0,0,1,1)
            
        for i, label in enumerate(method_labels):
            hlayout = QHBoxLayout()
            hlayout.setSpacing(5)
            field = self.method_fields[i]
            hlayout.addWidget(label, 0)
            hlayout.addWidget(field, 1)
            hlayout.setAlignment(Qt.AlignLeft| Qt.AlignTop)
            method_layout.addLayout(hlayout, i+1,0,1,1)

    def configurePeakParameters(self):
        
        peak_label = QLabel()
        peak_label.setText('Peaks')
        peak_label.setFont(self.font11)
        peak_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        peak_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        dev_label = QLabel()
        dev_label.setText("In development")
        dev_label.setFont(self.font9)
        dev_label.setAlignment(Qt.AlignTop)
        dev_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        peak_layout = self.peak_layout
        peak_layout.setContentsMargins(10,10,15,2)
        peak_layout.setVerticalSpacing(3)
        peak_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        peak_layout.addWidget(peak_label, 0,0,1,1)
        peak_layout.addWidget(dev_label, 1,0,1,1)

    def configureFonts(self):
        
        self.font9 = QFont()
        font9 = self.font9
        font9.setPointSize(9)
        
        self.font9bold = QFont()
        font9bold = self.font9bold
        font9bold.setPointSize(9)
        font9bold.setBold(True)
        
        self.font11 = QFont()
        font11 = self.font11
        font11.setBold(True)
        font11.setPointSize(11)
        
        self.font14 = QFont()
        font14 = self.font14
        font14.setBold(True)
        font14.setPointSize(14)

    def addData(self, instrument_params, method_params, slider_dict):

        slider_B0 = slider_dict['b0'][0]
        slider_Bf = slider_dict['bf'][0]
        slider_tG = slider_dict['tg'][0]
        

        field_end = []
        for n, field in enumerate(self.instrument_fields):
            string = str(instrument_params[n])
            if n == 2 or n == 3:
                string += 'mm'
            elif n == 4 or n == 5:
                string += 'um'
            elif n == 7 or n == 8:
                string += 's'
            field.setText(string)
            #field.adjustSize()
            #field_end.append(field.width() + field.x())
        
        #max_end = max(field_end)
        #self.line2.setGeometry(max_end+20, self.line2.y(), self.line2.width(), self.line2.height())

        #for label in self.method_labels:
        #    label.setGeometry(max_end+35, label.y(), label.width(), label.height())
        #    label.adjustSize()
        #self.label_method_title.setGeometry(max_end+35, self.label_method_title.y(), self.label_method_title.width(), self.label_method_title.height())

        for n, field in enumerate(self.method_fields):
            string = str(method_params[n])
            if n == 0:
                string += 'mL/min'
            elif n == 1:
                string = str(slider_tG.value())
                string += 'min'
            elif n == 2:
                string = str(slider_B0.value() / (slider_B0.res / 100))
                string += '%'
            elif n == 3:
                string = str(slider_Bf.value() / (slider_Bf.res / 100))
                string += '%'
            elif n == 4:
                string += 'nm'
            field.setText(string)
            #field_end = self.method_labels[n].x() + self.method_labels[n].width()
            #field.setGeometry(field_end+5, field.y(), field.width(), field.height())
            #field.adjustSize()

        



