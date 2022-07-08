from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TableHeader(QWidget):
    def __init__(self, optimiser):
        super().__init__()

        self.optimiser = optimiser

        self._configure_layout()
        self._configure_font()

        self.create_header()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 8, 0, 10)
        self.grid_layout.setColumnStretch(0, 3)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)
        self.grid_layout.setColumnStretch(3, 1)
        self.grid_layout.setColumnStretch(4, 3)
        self.grid_layout.setColumnStretch(5, 1)

    def _configure_font(self):
        self.font_run = QFont()
        self.font_run.setPointSize(12)
        self.font_run.setBold(True)

        self.font_tg = QFont()
        self.font_tg.setPointSize(9)

    def _create_label(self, text, font, alignment):
        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(alignment)
        return label

    def _create_input(self, number):
        tg_input = QLineEdit()
        tg_input.setFixedWidth(30)
        tg_input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tg_input.setObjectName(f"tg{str(number)}")
        tg_input.setStyleSheet("""border: 1px solid red;""")
        return tg_input

    def create_header(self):
        self.tg1_input = self._create_input(1)
        self.tg2_input = self._create_input(2)
        tg_inputs = [self.tg1_input, self.tg2_input]
        self.data = tg_inputs

        for n in range(len(tg_inputs)):
            run_label = self._create_label(
                "Run %s" % (str(n + 1)), self.font_run, Qt.AlignRight | Qt.AlignVCenter
            )
            tg_label = self._create_label(
                "Gradient time", self.font_tg, Qt.AlignRight | Qt.AlignVCenter
            )
            spacer_label = QLabel()

            self.grid_layout.addWidget(run_label, 0, 4 * n, 1, 1)
            self.grid_layout.addWidget(tg_label, 0, 4 * n + 1, 1, 1)
            self.grid_layout.addWidget(tg_inputs[n], 0, 4 * n + 2, 1, 1)
            self.grid_layout.addWidget(spacer_label, 0, 4 * n + 3, 1, 1)

    def update_model(self, number):
        if number == 1:
            self.optimiser.tg1 = self.tg1_input.text()
        elif number == 2:
            self.optimiser.tg2 = self.tg2_input.text()
