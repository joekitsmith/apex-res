from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ResWidget(QWidget):

    def setupUi(self, peakinterest, critical_Rs):
        
        self.setObjectName('ResWidget')
        self.resize(200, 400)

        self.setStyleSheet('background-color: (0.906, 0.906, 0.906)')

        self.maximise_button = QPushButton()
        self.maximise_button.setMouseTracking(True)
        self.maximise_button.setMinimumHeight(50)
        self.maximise_button.setText('Maximise resolution')
        button_font = QFont()
        button_font.setPointSize(12)
        button_font.setBold(True)
        self.maximise_button.setFont(button_font)

        self.resolution_label1 = QLabel()
        self.resolution_label1.setText('Peak %s resolution:' %(peakinterest))
        self.resolution_label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        res_label1_font = QFont()
        res_label1_font.setPointSize(11)
        self.resolution_label1.setFont(res_label1_font)

        self.resolution_label2 = QLabel()
        self.resolution_label2.setText('%s' %(round(critical_Rs[0],2)))
        self.resolution_label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        res_label2_font = QFont()
        res_label2_font.setPointSize(11)
        res_label2_font.setBold(True)
        self.resolution_label2.setFont(res_label2_font)

        gridLayout = QGridLayout(self)
        gridLayout.addWidget(self.maximise_button, 1, 1, 1, 1)
        gridLayout.addWidget(self.resolution_label1, 2, 1, 1, 1)
        gridLayout.addWidget(self.resolution_label2, 3, 1, 1, 1)