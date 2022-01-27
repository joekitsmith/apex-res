from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout


class ResolutionWidget(QWidget):
    def __init__(self, optimiser):
        super(ResolutionWidget, self).__init__()

        self.optimiser = optimiser

        self._configure()

    def update_resolution(self, optimiser):
        self.optimiser = optimiser

        self.value_label.setText("%s" % (round(self.optimiser.critical_res, 2)))


    def _configure(self):
        self.setObjectName("ResWidget")
        self.resize(200, 400)

        self.setStyleSheet("background-color: (0.906, 0.906, 0.906)")

        self._configure_layout()
        self._configure_fonts()

        self._add_text_label()
        self._add_value_label()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)

    def _configure_fonts(self):
        self.font_text = QFont()
        self.font_text.setPointSize(16)

        self.font_value = QFont()
        self.font_value.setPointSize(16)
        self.font_value.setBold(True)

    def _add_text_label(self):
        self.text_label = QLabel()
        self.text_label.setText(
            "Peak %s resolution:" % (self.optimiser.peak_of_interest)
        )
        self.text_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.text_label.setFont(self.font_text)
        self.grid_layout.addWidget(self.text_label, 0, 1, 1, 1)

    def _add_value_label(self):
        self.value_label = QLabel()
        self.value_label.setText("%s" % (round(self.optimiser.critical_res, 2)))
        self.value_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.value_label.setFont(self.font_value)
        self.grid_layout.addWidget(self.value_label, 1, 1, 1, 1)
