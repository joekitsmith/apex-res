from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QGridLayout

from .functions import combine_field_and_value
from .names import (
    InstrumentParameterNames,
    MethodParameterNames,
    PeakParameterNames,
)


class ParametersGroupWidget(QWidget):
    def __init__(self, optimiser, label):
        super(ParametersGroupWidget, self).__init__()

        self.optimiser = optimiser
        self.label = label

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)

        if self.label == InstrumentParameterNames.INSTRUMENT:
            self.grid_layout.setContentsMargins(0, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(9)

        elif self.label == MethodParameterNames.METHOD:
            self.grid_layout.setContentsMargins(10, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(3)
            self.grid_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        else:
            self.grid_layout.setContentsMargins(10, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(3)
            self.grid_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def _add_header(self):

        instrument_label = QLabel()
        instrument_label.setText(self.label)
        instrument_label.setFont(self.font11)
        instrument_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        instrument_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(instrument_label, 0, 0, 1, 1)

    def _add_parameters(self):
        self._add_header()

        if self.label == ParameterNames.INSTRUMENT:
            names = InstrumentParameterNames
        elif self.label == ParameterNames.METHOD:
            names = MethodParameterNames
        else:
            names = PeakParameterNames

        for i, name, text in enumerate(names.__dict__.items()):
            field = QLabel()
            field.setText(str(text + ":"))
            field.setFont(self.font9bold)
            field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            field.adjustSize()

            value = QLabel()
            value.setText(getattr(self.optimiser, name.lower()))
            value.setFont(self.font9)
            value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

            h_layout = combine_field_and_value(field, value)

            self.grid_layout.addLayout(h_layout, i + 1, 0, 1, 1)
