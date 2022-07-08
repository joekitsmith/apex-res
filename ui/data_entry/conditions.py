from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QGridLayout,
    QSizePolicy,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.parameters.names import ConditionParameterNames


class TableConditions(QWidget):
    def __init__(self, optimiser):
        super().__init__()

        self.optimiser = optimiser

        self._configure_layout()
        self._configure_font()

        self.add_conditions()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(20, 8, 10, 10)

    def _configure_font(self):
        self.font_label = QFont()
        self.font_label.setPointSize(9)

    def _create_label(self, text, font, alignment):
        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(alignment)
        return label

    def _create_input(self, name):
        field = QLineEdit()
        field.setObjectName(name)
        field.setFixedWidth(30)
        field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        field.setStyleSheet("""border: 1px solid red;""")
        return field

    def add_conditions(self):
        initial_label = self._create_label(
            ConditionParameterNames.PHI0,
            self.font_label,
            Qt.AlignRight | Qt.AlignVCenter,
        )
        final_label = self._create_label(
            ConditionParameterNames.PHIF,
            self.font_label,
            Qt.AlignRight | Qt.AlignVCenter,
        )

        self.initial_input = self._create_input(ConditionParameterNames.PHI0)
        self.final_input = self._create_input(ConditionParameterNames.PHIF)
        self.data = [self.initial_input, self.final_input]

        self.grid_layout.addWidget(initial_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(final_label, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.initial_input, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.final_input, 0, 3, 1, 1)

    def update_model(self, name):
        if name == ConditionParameterNames.PHI0:
            self.optimiser.b0 = self.initial_input.text()

        elif name == ConditionParameterNames.PHIF:
            self.optimiser.bf = self.final_input.text()
