import numpy as np
import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy, QSlider, QLabel
from .functions import clear_layout

from .data_classes import SliderNames


class Slider(QSlider):
    def __init__(self, name, resolution, minimum, maximum, interval, initial_value):
        super(Slider, self).__init__()

        self.name = name
        self.resolution = resolution
        self.minimum = minimum
        self.maximum = maximum
        self.interval = interval
        self.initial_value = initial_value

        self._configure()

    def _configure(self):
        self.setMouseTracking(True)

        self.setRange(self.minimum, self.maximum)
        self.setValue(self.initial_value * self.resolution)

        self.setTickPosition(QSlider.TicksBothSides)
        self.setTickInterval(self.interval)


class SliderObject(QWidget):
    def __init__(self, optimiser, name):
        super(SliderObject, self).__init__()

        self.optimiser = optimiser
        self.name = name

        self._configure()

    def _configure(self):
        self.objectName = self.name

        self._configure_layout()
        self._configure_font()

        self._create_slider()
        self._add_tick_labels()

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)

        # self.grid_layout.setContentsMargins(0, 0, 0, 0)

    def _configure_font(self):
        self.font_label = QFont()
        self.font_label.setPointSize(8)

        self.font_title = QFont()
        self.font_title.setPointSize(10)

    def _add_tick_labels(self):
        value_range = np.arange(
            self.slider.minimum,
            self.slider.maximum + self.slider.interval,
            self.slider.interval,
        )[::-1]

        for i, value in enumerate(value_range):
            label = QLabel()
            if self.name == SliderNames.B0 or self.name == SliderNames.BF:
                abs_value = (value / self.slider.resolution) * 100
            else:
                abs_value = value / self.slider.resolution

            if abs_value.is_integer():
                abs_value = int(abs_value)
            else:
                abs_value = round(abs_value, 1)

            label.setText(f"{abs_value}")
            label.setFont(self.font_label)

            tick_number = len(value_range)
            if i < tick_number / 3:
                label.setAlignment(Qt.AlignRight | Qt.AlignTop)
            if i >= tick_number / 3 and i <= 2 * tick_number / 3:
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if i > 2 * tick_number / 3:
                label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

            label.setStyleSheet("margin-top: 2px;")

            self.grid_layout.addWidget(label, i, 0, 1, 1)

    def _create_slider(self):
        title_label = QLabel()
        title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        title_label.setFont(self.font_title)

        if self.name == SliderNames.B0:
            self.slider = Slider(
                name=SliderNames.B0,
                resolution=500,
                minimum=0,
                maximum=500,
                interval=100,
                initial_value=self.optimiser.phi0_init,
            )
            title_label.setText("Initial \n % B")

        elif self.name == SliderNames.BF:
            self.slider = Slider(
                name=SliderNames.BF,
                resolution=500,
                minimum=0,
                maximum=500,
                interval=100,
                initial_value=self.optimiser.phif_init,
            )
            title_label.setText("Final \n % B")

        elif self.name == SliderNames.TG:
            self.slider = Slider(
                name=SliderNames.TG,
                resolution=1,
                minimum=0,
                maximum=120,
                interval=20,
                initial_value=self.optimiser.tg1,
            )
            title_label.setText("Gradient \n time")

        # elif self.name == SliderNames.T0:
        #     self.slider = Slider(
        #         name=SliderNames.T0,
        #         resolution=1,
        #         minimum=0,
        #         maximum=5,
        #         interval=1,
        #         initial_value=self.optimiser.t0,
        #     )
        #     title_label.setText("Dead \n time")

        # elif self.name == SliderNames.TD:
        #     self.slider = Slider(
        #         name=SliderNames.TD,
        #         resolution=1,
        #         minimum=0,
        #         maximum=5,
        #         interval=1,
        #         initial_value=self.optimiser.td,
        #     )
        #     title_label.setText("Dwell \n time")

        # elif self.name == SliderNames.FLOW_RATE:
        #     self.slider = Slider(
        #         name=SliderNames.FLOW_RATE,
        #         resolution=1,
        #         minimum=0,
        #         maximum=5,
        #         interval=1,
        #         initial_value=self.optimiser.flow_rate,
        #     )

        #     title_label.setText("Flow \n rate")

        # elif self.name == SliderNames.COLUMN_LENGTH:
        #     self.slider = Slider(
        #         name=SliderNames.COLUMN_LENGTH,
        #         resolution=1,
        #         minimum=0,
        #         maximum=50,
        #         interval=10,
        #         initial_value=self.optimiser.column_length,
        #     )
        #     title_label.setText("Column \n length")

        # elif self.name == SliderNames.COLUMN_DIAMETER:
        #     self.slider = Slider(
        #         name=SliderNames.COLUMN_DIAMETER,
        #         resolution=1,
        #         minimum=0,
        #         maximum=5,
        #         interval=1,
        #         initial_value=self.optimiser.column_diameter,
        #     )
        #     title_label.setText("Column \n diameter")

        # elif self.name == SliderNames.PARTICLE_SIZE:
        #     self.slider = Slider(
        #         name=SliderNames.PARTICLE_SIZE,
        #         resolution=1,
        #         minimum=0,
        #         maximum=200,
        #         interval=40,
        #         initial_value=self.optimiser.particle_size,
        #     )
        #     title_label.setText("Particle \n size")

        self.ticks = (self.slider.maximum - self.slider.minimum) / self.slider.interval

        self.grid_layout.addWidget(self.slider, 0, 1, self.ticks + 1, 1)
        self.grid_layout.addWidget(title_label, self.ticks + 1, 0, 1, 2)


class SliderWidget(QWidget):
    def __init__(self, optimiser):
        super(SliderWidget, self).__init__()

        self.optimiser = optimiser

        self.sliders = {}

        self._configure()

    def update_slider(self, checkbox, name):
        if checkbox.isChecked():
            self.add_slider(name)

        else:
            self.delete_slider(name)

    def add_slider(self, name):
        slider_object = SliderObject(self.optimiser, name)
        self.sliders[name] = slider_object.slider

        count = self.grid_layout.count()
        row = int((count - (count % 3)) / 3)
        col = count % 3

        self.grid_layout.addWidget(
            slider_object, row, col, 1, 1, alignment=Qt.AlignHCenter
        )

    def delete_slider(self, name):
        del self.sliders[name]

        clear_layout(self.grid_layout)

        for name in self.sliders:
            self.add_slider(name)

    def _configure(self):
        self.setObjectName("SliderWidget")

        self._create_layout()

    def _create_layout(self):
        self.grid_layout = QGridLayout(self)

        # self.grid_layout.setContentsMargins(20, 0, 0, 0)
        # self.grid_layout.setVerticalSpacing(15)
        self.grid_layout.setHorizontalSpacing(25)
