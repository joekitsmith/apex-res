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

        self.critical_value.setText("%s" % (round(self.optimiser.critical_res, 2)))
        self.total_value.setText("%s" % (round(self.optimiser.total_res, 2)))

    def _configure(self):
        self.setObjectName("ResolutionWidget")

        self._configure_layout()
        self._configure_fonts()

        self._add_total_text()
        self._add_total_value()
        self._add_critical_text()
        self._add_critical_value()

        self._add_title_label()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(10, 2, 0, 0)
        self.grid_layout.setVerticalSpacing(3)

    def _configure_fonts(self):
        self.font_text = QFont()
        self.font_text.setPointSize(13)

        self.font_value = QFont()
        self.font_value.setPointSize(16)
        self.font_value.setBold(True)

        self.font_title = QFont()
        self.font_title.setPointSize(14)
        self.font_title.setBold(True)

    def _add_critical_text(self):
        text_label = QLabel()
        text_label.setObjectName("CriticalResolutionText")
        text_label.setText("Peak %s resolution:" % (self.optimiser.peak_of_interest))
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(self.font_text)
        self.grid_layout.addWidget(text_label, 1, 0, 1, 1)

    def _add_critical_value(self):
        self.critical_value = QLabel()
        self.critical_value.setObjectName("CriticalResolutionValue")
        self.critical_value.setText("%s" % (round(self.optimiser.critical_res, 2)))
        self.critical_value.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.critical_value.setFont(self.font_value)
        self.grid_layout.addWidget(self.critical_value, 2, 0, 1, 1)

    def _add_total_text(self):
        text_label = QLabel()
        text_label.setObjectName("TotalResolutionText")
        text_label.setText("Total resolution:")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(self.font_text)
        self.grid_layout.addWidget(text_label, 1, 1, 1, 1)

    def _add_total_value(self):
        self.total_value = QLabel()
        self.total_value.setObjectName("TotalResolutionValue")
        self.total_value.setText("%s" % (round(self.optimiser.total_res, 2)))
        self.total_value.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.total_value.setFont(self.font_value)
        self.grid_layout.addWidget(self.total_value, 2, 1, 1, 1)

    def _add_title_label(self):
        self.title_label = QLabel()
        self.title_label.setObjectName("ResolutionTitle")
        self.title_label.setText("RESOLUTION")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.title_label.setFont(self.font_title)
        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 2)
