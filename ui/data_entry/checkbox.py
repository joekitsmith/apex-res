from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TableCheckboxes(QWidget):
    def __init__(self, total_analytes):
        super(TableCheckboxes, self).__init__()

        self.total_analytes = total_analytes

        self._configure_layout()
        # self._add_title()

        self.add_checkboxes()

    def _configure_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def _create_checkbox(self):
        check = QCheckBox()
        return check

    def add_checkboxes(self):
        for n in range(0, self.total_analytes):
            check = self._create_checkbox()
            self.layout.addWidget(check, n)
