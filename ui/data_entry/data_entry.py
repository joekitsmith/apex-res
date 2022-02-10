from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
    QSizePolicy,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .header import TableHeader
from .analytes import TableAnalytes
from .checkbox import TableCheckboxes


class DataEntryWidget(QWidget):
    def __init__(self):
        super(DataEntryWidget, self).__init__()

        self.input_list = []
        self.total_analytes = 8

        self._configure_layout()
        self._configure_font()
        self._add_title_label()

        self.create_table()

    def create_table(self):
        header = TableHeader()
        analytes = TableAnalytes(self.total_analytes)

        self.grid_layout.addWidget(header, 1, 0, 1, 1)
        self.grid_layout.addWidget(analytes, 2, 0, 1, 1)

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 2, 0, 0)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(5)

    def _configure_font(self):
        self.font_title = QFont()
        self.font_title.setPointSize(14)
        self.font_title.setBold(True)

    def _add_title_label(self):
        title_label = QLabel()
        title_label.setText("DATA")
        title_label.setFont(self.font_title)
        title_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.grid_layout.addWidget(title_label, 0, 0, 1, 1)
