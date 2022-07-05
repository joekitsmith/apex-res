from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QSizePolicy, QGridLayout, QLabel, QFrame, QWidget

from .functions import clear_layout
from .data_classes import SliderNames


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


class SliderCheckBoxWidget(QWidget):
    def __init__(self, slider_widget, initial_sliders):
        super(SliderCheckBoxWidget, self).__init__()

        self.slider_widget = slider_widget
        self.initial_sliders = initial_sliders

        self.checkboxes = {}

        self._configure()

    def add_checkbox(self, name):
        self._create_checkbox(name)

        checkbox = self.checkboxes[name]
        if name in self.initial_sliders:
            checkbox.setChecked(True)

        else:
            checkbox.setEnabled(False)

        self._add_checkbox_to_layout(checkbox)

    def _create_checkbox(self, name):
        if name == SliderNames.B0:
            check_b0 = SliderCheckBox(name=SliderNames.B0)
            check_b0.stateChanged.connect(
                lambda: self.slider_widget.update_slider(check_b0, SliderNames.B0)
            )
            self.checkboxes[name] = check_b0

        elif name == SliderNames.BF:
            check_bf = SliderCheckBox(name=SliderNames.BF)
            check_bf.stateChanged.connect(
                lambda: self.slider_widget.update_slider(check_bf, SliderNames.BF)
            )
            self.checkboxes[name] = check_bf

        elif name == SliderNames.TG:
            check_tg = SliderCheckBox(name=SliderNames.TG)
            check_tg.stateChanged.connect(
                lambda: self.slider_widget.update_slider(check_tg, SliderNames.TG)
            )
            self.checkboxes[name] = check_tg

        elif name == SliderNames.T0:
            check_t0 = SliderCheckBox(name=SliderNames.T0)
            # check_t0.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(check_t0, SliderNames.T0)
            # )
            self.checkboxes[name] = check_t0

        elif name == SliderNames.TD:
            check_td = SliderCheckBox(name=SliderNames.TD)
            # check_td.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(check_td, SliderNames.TD)
            # )
            self.checkboxes[name] = check_td

        elif name == SliderNames.FLOW_RATE:
            check_flow = SliderCheckBox(name=SliderNames.FLOW_RATE)
            # check_flow.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(
            #         check_flow, SliderNames.FLOW_RATE
            #     )
            # )
            self.checkboxes[name] = check_flow

        elif name == SliderNames.COLUMN_LENGTH:
            check_col_len = SliderCheckBox(name=SliderNames.COLUMN_LENGTH)
            # check_col_len.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(
            #         check_col_len, SliderNames.COLUMN_LENGTH
            #     )
            # )
            self.checkboxes[name] = check_col_len

        elif name == SliderNames.COLUMN_DIAMETER:
            check_col_diam = SliderCheckBox(name=SliderNames.COLUMN_DIAMETER)
            # check_col_diam.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(
            #         check_col_diam, SliderNames.COLUMN_DIAMETER
            #     )
            # )
            self.checkboxes[name] = check_col_diam

        elif name == SliderNames.PARTICLE_SIZE:
            check_part_size = SliderCheckBox(name=SliderNames.PARTICLE_SIZE)
            # check_part_size.stateChanged.connect(
            #     lambda: self.slider_widget.update_slider(
            #         check_part_size, SliderNames.PARTICLE_SIZE
            #     )
            # )
            self.checkboxes[name] = check_part_size

        check = self.checkboxes[name]
        check.setFont(self.font_label)

    def _add_checkbox_to_layout(self, checkbox):
        total_checkboxes = len(self.checkboxes)

        count = self.checkbox_layout.count()
        if count < 3:
            self.checkbox_layout.addWidget(checkbox, total_checkboxes - 1, 0, 1, 1)

        elif count >= 3:
            cols = int((count - (count % 3)) / 3)
            self.checkbox_layout.addWidget(checkbox, count % 3, cols, 1, 1)

    def _configure(self):
        self.setObjectName("SliderCheckboxes")

        self.setMouseTracking(True)

        self._create_layout()
        self._configure_font()

    def _configure_font(self):
        self.font_label = QFont()
        self.font_label.setPointSize(11)

    def _create_layout(self):
        self.checkbox_layout = QGridLayout(self)
        self.checkbox_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.checkbox_layout.setVerticalSpacing(5)
        self.checkbox_layout.setHorizontalSpacing(20)
        self.checkbox_layout.setContentsMargins(0, 10, 0, 0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
