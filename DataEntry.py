from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt

class DataEntryWidget(QWidget):
    def __init__(self):
        super(DataEntryWidget, self).__init__()
        
        self.setupUi()

    def setupUi(self):
        
        self.setObjectName('DataEntryWidget')

        self.setStyleSheet('background-color: (0.906, 0.906, 0.906)')
        
class TableWidget(QWidget):
    def __init__(self, run_index):
        super(TableWidget, self).__init__()
        
        self.input_list = []
        self.run_index = run_index
        
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20,15,30,30)
        self.layout.setSpacing(10)
        
        self.addRunHeader()
        
    def addRunHeader(self):
        for n in range(self.run_index):
            run_label = QLabel()
            run_label.setText("Run %s" %(str(n+1)))
            run_label.setStyleSheet('''QWidget {font-weight: bold; font-size: 18px}''')
            tg_label = QLabel()
            tg_label.setText("tG")
            tg_label.setStyleSheet('''QWidget {font-size: 16px}''')
            tg_input = QLineEdit()
            tr_label = QLabel()
            tr_label.setText("tR")
            tr_label.setStyleSheet('''QWidget {font-size: 16px}''')
            area_label = QLabel()
            area_label.setText("Area")
            area_label.setStyleSheet('''QWidget {font-size: 16px}''')
            label_list = [run_label, tr_label, area_label]
            for label in label_list:
                label.setAlignment(Qt.AlignCenter) 
            tg_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
            tg_input.setFixedWidth(50)         
            self.layout.addWidget(run_label, 0, 2*n+1, 1, 2)
            self.layout.addWidget(tg_label, 1, 2*n+1, 1, 1)
            self.layout.addWidget(tg_input, 1, 2*n+2, 1, 1)
            self.layout.addWidget(tr_label, 2, 2*n+1, 1, 1)
            self.layout.addWidget(area_label, 2, 2*n+2, 1, 1)
            
    def addAnalyteRow(self, total_analytes):
        for n in range(1, total_analytes+1):
            analyte_label = QLabel()
            analyte_label.setText(str(n))
            analyte_label.setFixedSize(50, 50)
            analyte_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(analyte_label, n+2, 0, 1, 1)
            for m in range(self.run_index):
                tr_input = QLineEdit()
                tr_input.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                self.layout.addWidget(tr_input, n+2, m*2+1, 1, 1)
                area_input = QLineEdit()
                area_input.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                self.layout.addWidget(area_input, n+2, m*2+2, 1, 1)
                self.input_list.append((tr_input, area_input))
        
    def addPeakInterestCheck(self, total_analytes):
        peak_interest_label = QLabel()
        peak_interest_label.setText('Peak\nof\ninterest')
        peak_interest_label.setAlignment(Qt.AlignCenter)
        peak_interest_label.setStyleSheet('''QWidget {font-size: 16px}''')
        cols = self.layout.columnCount()
        self.layout.addWidget(peak_interest_label, 0, cols, 3, 1)
        for n in range(1, total_analytes+1):
            check = QCheckBox()
            check.setStyleSheet('''QCheckBox {margin-left:50%; margin-right:50%;}''')
            self.layout.addWidget(check, n+2, cols, 1, 1)
        
        
class TwoGradOptimizeTable(DataEntryWidget):
    def __init__(self):
        super(TwoGradOptimizeTable, self).__init__()
        
        table = TableWidget(2)
        table.addAnalyteRow(9)
        table.addPeakInterestCheck(9)
            
        self.setLayout(table.layout)
            
        