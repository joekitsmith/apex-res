from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(root_dir))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QSizePolicy,
    QHBoxLayout,
    QFrame,
)

from .group import ParametersGroupWidget
from .names import (
    InstrumentParameterNames,
    MethodParameterNames,
    PeakParameterNames,
)


class ParametersWidget(QWidget):
    def __init__(self, optimiser):
        super(ParametersWidget, self).__init__()

        self.optimiser = optimiser

        self._configure()

    def add_parameters(self):
        instrument_parameters = ParametersGroupWidget(
            self.optimiser, InstrumentParameterNames.INSTRUMENT
        )
        method_parameters = ParametersGroupWidget(
            self.optimiser, MethodParameterNames.METHOD
        )
        peak_parameters = ParametersGroupWidget(
            self.optimiser, PeakParameterNames.PEAKS
        )

        self.layout.addWidget(instrument_parameters, 2, 0, 1, 1)
        self.layout.addWidget(method_parameters, 2, 2, 1, 1)
        self.layout.addWidget(peak_parameters, 2, 4, 1, 1)

    def _configure(self):
        self.setObjectName("Parameters")

        self.setStyleSheet("background-color: (0.906, 0.906, 0.906)")

        self._configure_layouts()
        self._configure_fonts()

        self._add_background()
        self._add_label()

    def _configure_layouts(self):
        self.layout = QGridLayout(self)

        self.layout.setContentsMargins(20, 10, 20, 20)
        self.layout.setSpacing(8)

        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(4, 12)

    def _configure_fonts(self):
        self.font_label = QFont()
        self.font_label.setBold(True)
        self.font_label.setPointSize(14)

    def _add_label(self):
        label_title = QLabel()
        label_title.setText("Parameters")
        label_title.setFont(self.font_label)
        label_title.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        label_title.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.layout.addWidget(label_title, 0, 0, 1, 5)

    def _add_background(self):
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)

        vline1 = QFrame()
        vline1.setFrameShape(QFrame.VLine)
        vline1.setFrameShadow(QFrame.Sunken)

        vline2 = QFrame()
        vline2.setFrameShape(QFrame.VLine)
        vline2.setFrameShadow(QFrame.Sunken)

        self.layout.addWidget(hline, 1, 0, 1, 5)
        self.layout.addWidget(vline1, 2, 1, 1, 1)
        self.layout.addWidget(vline2, 2, 3, 1, 1)
