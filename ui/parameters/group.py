from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QGridLayout

from .functions import combine_field_and_value
from .names import (
    ParameterGroupNames,
    InstrumentParameterNames,
    MethodParameterNames,
    PeakParameterNames,
)


class ParametersGroupWidget(QWidget):
    def __init__(self, optimiser, label):
        super(ParametersGroupWidget, self).__init__()

        self.optimiser = optimiser
        self.label = label

        self._configure_layout()
        self._configure_font()

        self._add_header()
        self._add_parameters()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)

        if self.label == ParameterGroupNames.INSTRUMENT:
            self.grid_layout.setContentsMargins(0, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(9)

        elif self.label == ParameterGroupNames.METHOD:
            self.grid_layout.setContentsMargins(10, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(3)
            self.grid_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        else:
            self.grid_layout.setContentsMargins(10, 10, 15, 2)
            self.grid_layout.setVerticalSpacing(3)
            self.grid_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def _configure_font(self):
        self.font_title = QFont()
        self.font_title.setBold(True)
        self.font_title.setPointSize(11)

        self.font_field = QFont()
        self.font_field.setPointSize(9)
        self.font_field.setBold(True)

        self.font_value = QFont()
        self.font_value.setPointSize(9)

    def _add_header(self):
        title_label = QLabel()
        title_label.setText(self.label)
        title_label.setFont(self.font_title)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(title_label, 0, 0, 1, 1)

    def _add_parameters(self):
        self._add_header()

        if self.label == ParameterGroupNames.INSTRUMENT:
            names = InstrumentParameterNames
        elif self.label == ParameterGroupNames.METHOD:
            names = MethodParameterNames
        else:
            names = {}

        if names:
            for i, (name, text) in enumerate(names.__dict__.items()):
                if name[0] != "_":
                    field = QLabel()
                    print(name)
                    print(type(text))
                    print(text)
                    field.setText(str(text + ":"))
                    field.setFont(self.font_field)
                    field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
                    field.adjustSize()

                    value = QLabel()
                    value.setText(str(getattr(self.optimiser, name.lower())))
                    value.setFont(self.font_value)
                    value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

                    h_layout = combine_field_and_value(field, value)

                    self.grid_layout.addLayout(h_layout, i + 1, 0, 1, 1)
