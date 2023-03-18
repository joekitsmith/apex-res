import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from optimisers.two_gradient.example import generate_example_inputs
from optimisers.two_gradient.two_grad_optimise import TwoGradOptimise
from ui.chromatogram.chromatogram import ChromatogramWidget
from ui.data_entry.data_entry import DataEntryWidget
from ui.parameters.parameters import ParametersWidget
from ui.resolution.resolution import ResolutionWidget
from ui.slider.data_classes import SliderNames
from ui.slider.slider import SliderWidget
from ui.update.update import UpdateUI


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._configure_layout()

        self.initialise_model()

        self.initial_sliders = [
            SliderNames.B0,
            SliderNames.BF,
            SliderNames.TG,
        ]

        self.initial_slider_checks = [
            SliderNames.B0,
            SliderNames.BF,
            SliderNames.TG,
            SliderNames.T0,
            SliderNames.TD,
            SliderNames.FLOW_RATE,
            SliderNames.COLUMN_LENGTH,
            SliderNames.COLUMN_DIAMETER,
            SliderNames.PARTICLE_SIZE,
        ]

        self.add_chromatogram_widget()
        self.add_slider_interface()
        self.add_parameters_widget()
        self.add_resolution_widget()
        self.add_data_entry_widget()

        update_ui = UpdateUI(
            self.chromatogram_widget,
            self.parameters_widget,
            self.slider_widget,
            self.resolution_widget,
            self.data_entry_widget,
        )

    def initialise_model(self):
        self.optimiser = TwoGradOptimise()

    def add_chromatogram_widget(self):
        self.chromatogram_widget = ChromatogramWidget(self.optimiser)
        self.chromatogram_widget.create_plot()
        self.optimiser = self.chromatogram_widget.optimiser
        self.grid_layout.addWidget(self.chromatogram_widget, 2, 1, 1, 2)

    def add_slider_interface(self):
        self.slider_widget = SliderWidget(self.optimiser, self.initial_sliders)
        self.slider_widget.enable_checkboxes(self.initial_slider_checks)

        self.optimiser = self.slider_widget.optimiser

        self.grid_layout.addWidget(self.slider_widget, 1, 0, 2, 1)

    def add_parameters_widget(self):
        self.parameters_widget = ParametersWidget(self.optimiser)
        self.parameters_widget.add_parameters()
        self.optimiser = self.parameters_widget.optimiser
        self.grid_layout.addWidget(self.parameters_widget, 0, 1, 2, 1)

    def add_resolution_widget(self):
        self.resolution_widget = ResolutionWidget(self.optimiser)
        self.optimiser = self.resolution_widget.optimiser
        self.grid_layout.addWidget(self.resolution_widget, 0, 0, 1, 1)

    def add_data_entry_widget(self):
        self.data_entry_widget = DataEntryWidget(self.optimiser)
        self.grid_layout.addWidget(self.data_entry_widget, 0, 2, 2, 1)

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setRowStretch(2, 2)
        self.grid_layout.setColumnStretch(2, 5)
        self.grid_layout.setColumnStretch(1, 2)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.margin = 4
        self.setMouseTracking(True)
        with open(
            os.path.join(os.path.dirname(__file__), "ui/styles/light.qss")
        ) as style_file:
            style = style_file.read()
        self.setStyleSheet(style)

        self.setWindowTitle("Apex Res")

        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = Window()
    window.showMaximized()

    sys.exit(app.exec_())
