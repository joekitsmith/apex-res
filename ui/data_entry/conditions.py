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


class TableConditions(QWidget):
    def __init__(self):
        super(TableConditions, self).__init__()

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

    def _create_input(self):
        field = QLineEdit()
        field.setFixedWidth(30)
        field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        return field

    def add_conditions(self):
        initial_label = self._create_label(
            "Initial %B", self.font_label, Qt.AlignRight | Qt.AlignVCenter
        )
        final_label = self._create_label(
            "Final %B", self.font_label, Qt.AlignRight | Qt.AlignVCenter
        )

        initial_input = self._create_input()
        final_input = self._create_input()

        self.grid_layout.addWidget(initial_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(final_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(initial_input, 0, 1, 1, 1)
        self.grid_layout.addWidget(final_input, 1, 1, 1, 1)
