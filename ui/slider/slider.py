from PyQt5.QtCore import Qt
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
        self.objectName = self.name
        self.setMouseTracking(True)

        self.setRange(self.minimum, self.maximum)
        self.setValue(self.initial_value * self.resolution)

        self.setTickPosition(QSlider.TicksBothSides)
        self.setTickInterval(self.interval)


class SliderWidget(QWidget):
    def __init__(self, optimiser):
        super(SliderWidget, self).__init__()

        self.optimiser = optimiser

        self.sliders = {}

        self._configure()

    def add_slider(self, name):
        self._create_slider(name)

        slider, slider_label = self.sliders[name]

        count = self.grid_layout.count() / 2
        row = (2 * count - (count % 3)) / 3 + 1

        if count < 3:
            self.grid_layout.addWidget(
                slider, 0, count, 1, 1, alignment=Qt.AlignHCenter
            )
            self.grid_layout.addWidget(
                slider_label, 1, count, 1, 1, alignment=Qt.AlignHCenter
            )
        else:
            self.grid_layout.addWidget(
                slider, row, count % 3, 1, 1, alignment=Qt.AlignHCenter
            )
            self.grid_layout.addWidget(
                slider_label, row + 1, count % 3, 1, 1, alignment=Qt.AlignHCenter
            )

    def delete_slider(self, name):
        del self.sliders[name]

        clear_layout(self.grid_layout)

        for name in self.sliders:
            self.add_slider(name)

    def _configure(self):

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        self._create_layout()

    def _create_layout(self):
        self.grid_layout = QGridLayout(self)

        self.grid_layout.setContentsMargins(30, 0, 30, 0)
        self.grid_layout.setVerticalSpacing(20)
        self.grid_layout.setHorizontalSpacing(50)

    def _create_slider(self, name):
        slider_label = QLabel()

        if name == SliderNames.B0:
            slider = Slider(
                name=SliderNames.B0,
                resolution=500,
                minimum=0,
                maximum=500,
                interval=10,
                initial_value=self.optimiser.phi0_init,
            )
            slider_label.setText("Initial \n % B")

        elif name == SliderNames.BF:
            slider = Slider(
                name=SliderNames.BF,
                resolution=500,
                minimum=0,
                maximum=500,
                interval=10,
                initial_value=self.optimiser.phif_init,
            )
            slider_label.setText("Final \n % B")

        elif name == SliderNames.TG:
            slider = Slider(
                name=SliderNames.TG,
                resolution=1,
                minimum=1,
                maximum=120,
                interval=10,
                initial_value=self.optimiser.tg1,
            )
            slider_label.setText("Gradient \n time")

        elif name == SliderNames.T0:
            slider = Slider(
                name=SliderNames.T0,
                resolution=1,
                minimum=0,
                maximum=5,
                interval=0.1,
                initial_value=self.optimiser.t0,
            )
            slider_label.setText("Dead \n time")

        elif name == SliderNames.TD:
            slider = Slider(
                name=SliderNames.TD,
                resolution=1,
                minimum=0,
                maximum=5,
                interval=0.1,
                initial_value=self.optimiser.td,
            )
            slider_label.setText("Dwell \n time")

        elif name == SliderNames.FLOW_RATE:
            slider = Slider(
                name=SliderNames.FLOW_RATE,
                resolution=1,
                minimum=0,
                maximum=5,
                interval=0.1,
                initial_value=self.optimiser.flow_rate,
            )
            slider_label.setText("Flow \n rate")

        elif name == SliderNames.COLUMN_LENGTH:
            slider = Slider(
                name=SliderNames.COLUMN_LENGTH,
                resolution=1,
                minimum=0,
                maximum=50,
                interval=1,
                initial_value=self.optimiser.col_length,
            )
            slider_label.setText("Column \n length")

        elif name == SliderNames.COLUMN_DIAMETER:
            slider = Slider(
                name=SliderNames.COLUMN_DIAMETER,
                resolution=1,
                minimum=0,
                maximum=5,
                interval=0.1,
                initial_value=self.optimiser.col_diameter,
            )
            slider_label.setText("Column \n diameter")

        elif name == SliderNames.PARTICLE_SIZE:
            slider = Slider(
                name=SliderNames.PARTICLE_SIZE,
                resolution=1,
                minimum=0,
                maximum=200,
                interval=5,
                initial_value=tgo.particle_size,
            )
            slider_label.setText("Particle \n size")

        self.sliders[name] = (slider, slider_label)
