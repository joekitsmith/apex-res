from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QSizePolicy, QGridLayout, QLabel, QFrame


class SliderCheckBox(QCheckBox):
    def __init__(self, name):
        super(SliderCheckBox, self).__init__()

        self.name = name

        self._configure()

    def _configure(self):

        self.setMouseTracking(True)

        self.setText(self.name)
        self.setStyleSheet("""QCheckBox { font-size: 10px;}""")
        self.setStyleSheet(
            """QCheckBox::indicator{ height: 10px;
                           width: 10px}"""
        )


class SliderCheckBoxWidget(QCheckBox):
    def __init__(self, optimiser):
        super(SliderCheckBoxWidget, self).__init__()

        self.optimiser = optimiser

        self.checkboxes = {}

        self._configure()

    def add_checkbox(self, name):
        self._create_checkbox(name)

        checkbox = self.checkboxes[name]

        count = self.checkbox_layout.count()
        if count < 3:
            self.checkbox_layout.addWidget(checkbox, count, 0, 1, 1)
            self.setFixedWidth(150)

        if count >= 3:
            cols = (count - (count % 3)) / 3
            self.checkbox_layout.addWidget(checkbox, count % 3, cols, 1, 1)
            self.setFixedWidth((cols + 1) * 150)

    def _configure(self):
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setMouseTracking(True)

        self._create_layout()
        self._add_label()

    def _create_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(10, 10, 3, 3)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setVerticalSpacing(1)

        self.checkbox_layout = QGridLayout()
        self.checkbox_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.checkbox_layout.setSpacing(3)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 5)

        self.grid_layout.addLayout(self.checkbox_layout, 0, 0, 2, 1)

    def _add_label(self):
        label = QLabel("Sliders")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.grid_layout.addWidget(label, 2, 0, 1, 1)

        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Raised)
        self.grid_layout.addWidget(line, 0, 1, 3, 1)

    def _create_checkbox(self, name):
        checkbox = SliderCheckBox(name)
        self.checkboxes[name] = checkbox
