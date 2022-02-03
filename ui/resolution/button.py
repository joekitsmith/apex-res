from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton


class MaximiseResolutionButton(QPushButton):
    def _init__(self):
        super(MaximiseResolutionButton, self).__init()

        self._configure()

    def _configure(self):
        self.setObjectName("MaximiseResolution")

        self.setMouseTracking(True)
        self.setMinimumHeight(50)
        self.setText("Maximise resolution")

        button_font = QFont()
        button_font.setPointSize(12)
        button_font.setBold(True)
        self.setFont(button_font)
