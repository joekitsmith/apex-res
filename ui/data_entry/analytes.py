from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
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

from .checkbox import TableCheckboxes


class TableAnalytes(QWidget):
    def __init__(self, total_analytes):
        super(TableAnalytes, self).__init__()

        self.inputs = []
        self.total_analytes = total_analytes

        self._configure_layout()
        self._configure_font()

        self.add_header()
        self.add_analytes()
        self._add_checkboxes()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 5, 0)
        for n in range(4):
            self.grid_layout.setColumnStretch(n, 2)

    def _configure_font(self):
        self.font_analyte_label = QFont()
        self.font_analyte_label.setPointSize(11)
        self.font_analyte_label.setBold(True)

        self.font_peak_interest = QFont()
        self.font_peak_interest.setPointSize(9)

        self.font_tr = QFont()
        self.font_tr.setPointSize(9)

        self.font_area = QFont()
        self.font_area.setPointSize(9)

    def _create_analyte_label(self, n):
        label = QLabel()
        label.setText(str(n + 1))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(self.font_analyte_label)
        return label

    def _add_peak_of_interest_label(self):
        peak_interest_label = QLabel()
        peak_interest_label.setText("Peak of interest")
        peak_interest_label.setFont(self.font_peak_interest)

        self.grid_layout.addWidget(
            peak_interest_label, 0, 6, 1, 1, alignment=Qt.AlignCenter
        )

    def _add_checkboxes(self):
        checkboxes = TableCheckboxes(self.total_analytes)
        self.grid_layout.addWidget(
            checkboxes, 1, 6, self.total_analytes, 1, alignment=Qt.AlignCenter
        )

    def _create_input(self):
        input_field = QLineEdit()
        # input_field.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        return input_field

    def add_header(self):
        for n in range(2):
            tr_label = self._create_label(
                "tR", self.font_tr, Qt.AlignHCenter | Qt.AlignTop
            )
            area_label = self._create_label(
                "Area", self.font_area, Qt.AlignHCenter | Qt.AlignTop
            )
            self.grid_layout.addWidget(
                tr_label, 0, 2 * n, 1, 1, alignment=Qt.AlignCenter
            )
            self.grid_layout.addWidget(
                area_label, 0, 2 * n + 1, 1, 1, alignment=Qt.AlignCenter
            )

        self._add_peak_of_interest_label()

    def _create_label(self, text, font, alignment):
        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(alignment)
        return label

    def add_analytes(self):
        self._add_table()

    def _add_table(self):
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.horizontalHeader().hide()
        # self.table.verticalHeader().hide()

        for n in range(self.total_analytes):
            self.table.insertRow(n)
            for m in range(4):
                if n == 0:
                    self.table.insertColumn(m)

                item = QTableWidgetItem()
                self.table.setItem(n, m, QTableWidgetItem(item))

        self.grid_layout.addWidget(self.table, 1, 0, self.total_analytes, 4)
