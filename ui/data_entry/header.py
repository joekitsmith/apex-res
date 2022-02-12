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
    def __init__(self):
        super(TableHeader, self).__init__()

        self._configure_layout()
        self._configure_font()

        self.create_header()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 8, 0, 10)

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

    def create_header(self):
        for n in range(2):
            run_label = self._create_label(
                "Run %s" % (str(n + 1)), self.font_run, Qt.AlignRight | Qt.AlignVCenter
            )
            tg_label = self._create_label(
                "Gradient time", self.font_tg, Qt.AlignRight | Qt.AlignVCenter
            )
            tg_input = QLineEdit()
            tg_input.setFixedWidth(30)
            tg_input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.grid_layout.addWidget(run_label, 0, 3 * n, 1, 1)
            self.grid_layout.addWidget(tg_label, 0, 3 * n + 1, 1, 1)
            self.grid_layout.addWidget(tg_input, 0, 3 * n + 2, 1, 1)
