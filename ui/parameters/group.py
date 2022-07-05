from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QGridLayout, QLineEdit

from typing import Union

import numpy as np

from .functions import combine_field_and_value
from .names import (
    ParameterGroupNames,
    InstrumentParameterNames,
    MethodParameterNames,
    ConditionParameterNames,
    PeakParameterNames,
)


class ParametersGroupWidget(QWidget):
    def __init__(self, optimiser, label):
        super(ParametersGroupWidget, self).__init__()

        self.optimiser = optimiser
        self.label = label

        self._configure()

        self._add_header()
        self._add_parameters()

    def _configure(self):
        self.setObjectName("ParametersGroupWidget")

        self._configure_layout()
        self._configure_font()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setAlignment(Qt.AlignTop)
        self.grid_layout.setVerticalSpacing(8)

    def _configure_font(self):
        self.font_title = QFont()
        self.font_title.setBold(True)
        self.font_title.setPointSize(13)

        self.font_field = QFont()
        self.font_field.setPointSize(11)
        self.font_field.setBold(True)

        self.font_value = QFont()
        self.font_value.setPointSize(11)

    def _add_header(self):
        title_label = QLabel()
        title_label.setText(self.label)
        title_label.setFont(self.font_title)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        title_label.setStyleSheet(
            """margin-bottom: 3px; border-top: 0px solid black; border-bottom: 1px solid black"""
        )
        title_label.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum
        )  # heading underline extends across
        self.grid_layout.addWidget(title_label, 0, 0, 1, 1)

    def _display_conditions(self, value, name):
        if isinstance(value, np.ndarray):
            value = value[0]

        if isinstance(value, (float, int, np.number)):
            is_condition = [
                True for attr in ConditionParameterNames.__dict__ if attr == name
            ]
            if is_condition:
                value = value * 100

                if abs(value - round(value, 1) < 0.05):
                    value = round(value)

        return value

    def _add_input(self, name):
        attr = [k for k, v in vars(self.names).items() if v == name]
        if attr:
            attr = attr[0]
        line_edit = QLineEdit()
        line_edit.setObjectName(name)
        value = getattr(self.optimiser, attr.lower())
        value = self._display_conditions(value, name)
        if value is not None:
            line_edit.setText(str(value))
        line_edit.setFont(self.font_value)
        line_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        return line_edit

    def _add_label(self, name):
        attr = [k for k, v in vars(self.names).items() if v == name]
        if attr:
            attr = attr[0]
        label = QLabel()
        label.setObjectName(name)
        value = getattr(self.optimiser, attr.lower())
        value = self._display_conditions(value, name)
        if value is not None:
            label.setText(str(value))
        label.setFont(self.font_value)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        return label

    def _add_parameters(self):
        self._add_header()

        if self.label == ParameterGroupNames.INSTRUMENT:
            self.names = InstrumentParameterNames
            self.t0_input = self._add_input(InstrumentParameterNames.T0)
            self.n_input = self._add_input(InstrumentParameterNames.N_EST)
            self.td_input = self._add_input(InstrumentParameterNames.TD)
            inputs = [
                self.t0_input,
                self.n_input,
                self.td_input,
            ]

        elif self.label == ParameterGroupNames.METHOD:
            self.names = MethodParameterNames
            self.tg_label = self._add_label(MethodParameterNames.TG_FINAL)
            self.phi0_label = self._add_label(MethodParameterNames.PHI0)
            self.phif_label = self._add_label(MethodParameterNames.PHIF)
            inputs = [
                self.tg_label,
                self.phi0_label,
                self.phif_label,
            ]

        else:
            self.names = {}

        self.parameters = inputs

        if self.names:
            count = 0
            for name, text in vars(self.names).items():
                if name[0] != "_":
                    field = QLabel()
                    field.setObjectName(name)
                    field.setText(str(text + ":"))
                    field.setFont(self.font_field)
                    field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                    h_layout = combine_field_and_value(field, inputs[count])

                    self.grid_layout.addLayout(h_layout, count + 1, 0, 1, 1)

                    count += 1
