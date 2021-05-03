from PyQt5 import QtCore, QtGui, QtWidgets

class ParamWidget(QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super(ParamWidget, self).__init__()
        
        self.setupUi()

    def setupUi(self):
        
        self.setObjectName('ParamWidget')

        gridLayout = QtWidgets.QGridLayout(self)

        self.setStyleSheet('background-color: (0.906, 0.906, 0.906)')

        self.label_title = QtWidgets.QLabel()
        self.label_title.setGeometry(QtCore.QRect(600, 0, 150 ,25))
        self.label_title.setText('Parameters')
        font14 = QtGui.QFont()
        font14.setBold(True)
        font14.setPointSize(14)
        self.label_title.setFont(font14)
        self.label_title.setAlignment(QtCore.Qt.AlignTop)

        self.label_instrument_title = QtWidgets.QLabel()
        self.label_instrument_title.setGeometry(QtCore.QRect(5, 40, 100, 50))
        self.label_instrument_title.setText('Instrument')
        font11 = QtGui.QFont()
        font11.setBold(True)
        font11.setPointSize(11)
        self.label_instrument_title.setFont(font11)
        self.label_instrument_title.setAlignment(QtCore.Qt.AlignTop)

        font9 = QtGui.QFont()
        font9.setPointSize(9)
        font9bold = QtGui.QFont()
        font9bold.setPointSize(9)
        font9bold.setBold(True)
        self.ins_name_label = QtWidgets.QLabel()
        self.col_name_label = QtWidgets.QLabel()
        self.col_length_label = QtWidgets.QLabel()
        self.col_diam_label = QtWidgets.QLabel()
        self.part_size_label = QtWidgets.QLabel()
        self.pore_diam_label = QtWidgets.QLabel()
        self.plate_num_label = QtWidgets.QLabel()
        self.dead_vol_label = QtWidgets.QLabel()
        self.dwell_vol_label = QtWidgets.QLabel()
        self.ins_name_field = QtWidgets.QLabel()
        self.col_name_field = QtWidgets.QLabel()
        self.col_length_field = QtWidgets.QLabel()
        self.col_diam_field = QtWidgets.QLabel()
        self.part_size_field = QtWidgets.QLabel()
        self.pore_diam_field = QtWidgets.QLabel()
        self.plate_num_field = QtWidgets.QLabel()
        self.dead_vol_field = QtWidgets.QLabel()
        self.dwell_vol_field = QtWidgets.QLabel()
        self.instrument_labels = [self.ins_name_label, self.col_name_label, self.col_length_label, self.col_diam_label, self.part_size_label, self.pore_diam_label, self.plate_num_label, self.dead_vol_label, self.dwell_vol_label]
        self.instrument_fields = [self.ins_name_field, self.col_name_field, self.col_length_field, self.col_diam_field, self.part_size_field, self.pore_diam_field, self.plate_num_field, self.dead_vol_field, self.dwell_vol_field]
        instrument_strings = ['Instrument name', 'Column name', 'Column length', 'Column diameter', 'Particle size', 'Pore diameter', 'Plate number', 'Dead volume', 'Dwell volume']
        for n, label in enumerate(self.instrument_labels):
            label.setGeometry(QtCore.QRect(5, 70+(n*21), 100, 50))
            label.setText(str(instrument_strings[n] + ':'))
            label.setFont(font9bold)
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.adjustSize()

            field = self.instrument_fields[n]
            label_end = label.width() + label.x()
            field.setGeometry(QtCore.QRect(label_end+5, 70+(n*21), 100, 50))
            field.setFont(font9)
            label.setAlignment(QtCore.Qt.AlignLeft)

        self.label_method_title = QtWidgets.QLabel()
        self.label_method_title.setGeometry(QtCore.QRect(280, 40, 100, 50))
        self.label_method_title.setText('Method')
        font11 = QtGui.QFont()
        font11.setBold(True)
        font11.setPointSize(11)
        self.label_method_title.setFont(font11)
        self.label_method_title.setAlignment(QtCore.Qt.AlignTop)

        self.flow_rate_label = QtWidgets.QLabel()
        self.tG_label = QtWidgets.QLabel()
        self.B0_label = QtWidgets.QLabel()
        self.Bf_label = QtWidgets.QLabel()
        self.UV_label = QtWidgets.QLabel()
        self.flow_rate_field = QtWidgets.QLabel()
        self.tG_field = QtWidgets.QLabel()
        self.B0_field = QtWidgets.QLabel()
        self.Bf_field = QtWidgets.QLabel()
        self.UV_field = QtWidgets.QLabel()
        self.method_labels = [self.flow_rate_label, self.tG_label, self.B0_label, self.Bf_label, self.UV_label]
        self.method_fields = [self.flow_rate_field, self.tG_field, self.B0_field, self.Bf_field, self.UV_field]
        method_strings = ['Flow rate', 'Gradient time', 'Initial'+' % ' +'organic', 'Final'+' % ' +'organic', 'UV']
        for n, label in enumerate(self.method_labels):
            label.setGeometry(QtCore.QRect(320, 70+(n*40), 100, 50))
            label.setText(str(method_strings[n] + ':'))
            label.setFont(font9bold)
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.adjustSize()

            field = self.method_fields[n]
            label_end = label.width() + label.x()
            field.setGeometry(QtCore.QRect(label_end+5, 70+(n*40), 100, 50))
            field.setFont(font9)
            label.setAlignment(QtCore.Qt.AlignLeft)

        self.line = QtWidgets.QFrame()
        self.line.setGeometry(QtCore.QRect(0, 30, 1200, 5))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line2 = QtWidgets.QFrame()
        self.line2.setGeometry(QtCore.QRect(300, 31, 5, 250))
        self.line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line3 = QtWidgets.QFrame()
        self.line3.setGeometry(QtCore.QRect(470, 31, 5, 250))
        self.line3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.label_peak_title = QtWidgets.QLabel()
        self.label_peak_title.setGeometry(QtCore.QRect(490, 40, 100, 50))
        self.label_peak_title.setText('Peak')
        font11 = QtGui.QFont()
        font11.setBold(True)
        font11.setPointSize(11)
        self.label_peak_title.setFont(font11)
        self.label_peak_title.setAlignment(QtCore.Qt.AlignTop)

        gridLayout.addWidget(self.label_title, 0,0,3,1)
        gridLayout.addWidget(self.label_instrument_title, 1,0,1,1)
        gridLayout.addWidget(self.ins_name_label, 2, 0, 1, 1)


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
            field.adjustSize()
            field_end.append(field.width() + field.x())
        
        max_end = max(field_end)
        self.line2.setGeometry(max_end+20, self.line2.y(), self.line2.width(), self.line2.height())

        for label in self.method_labels:
            label.setGeometry(max_end+35, label.y(), label.width(), label.height())
            label.adjustSize()
        self.label_method_title.setGeometry(max_end+35, self.label_method_title.y(), self.label_method_title.width(), self.label_method_title.height())

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
            field_end = self.method_labels[n].x() + self.method_labels[n].width()
            field.setGeometry(field_end+5, field.y(), field.width(), field.height())
            field.adjustSize()

        



