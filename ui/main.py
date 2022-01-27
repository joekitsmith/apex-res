import sys

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QStackedLayout,
    QPushButton,
    QVBoxLayout,
)

from chromatogram.chromatogram import ChromatogramWidget
from models.two_gradient.example import generate_example_inputs
from models.two_gradient.two_grad_optimise import TwoGradOptimize
from ui.slider.slider import SliderWidget
from ui.slider.data_classes import SliderNames
from ui.resolution.resolution import ResolutionWidget
from ui.parameters.parameters import ParametersWidget
from ui.update.update import UpdateUI


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self._configure_layout()

        self.initialise_model()

        self.add_chromatogram_widget()
        self.add_slider_widget()
        self.add_parameters_widget()
        self.add_resolution_widget()

        update_ui = UpdateUI(
            self.chromatogram_widget, self.parameters_widget, self.slider_widget, self.resolution_widget
        )

    def initialise_model(self):
        inputs = generate_example_inputs()

        self.optimiser = TwoGradOptimize(*inputs)
        self.optimiser.calculate()

    def add_chromatogram_widget(self):
        self.chromatogram_widget = ChromatogramWidget(self.optimiser)
        self.chromatogram_widget.create_plot()
        self.optimiser = self.chromatogram_widget.optimiser
        self.grid_layout.addWidget(self.chromatogram_widget, 2, 1, 4, 1)

    def add_slider_widget(self):
        self.slider_widget = SliderWidget(self.optimiser)
        self.slider_widget.add_slider(SliderNames.B0)
        self.slider_widget.add_slider(SliderNames.BF)
        self.slider_widget.add_slider(SliderNames.TG)
        self.optimiser = self.slider_widget.optimiser
        self.grid_layout.addWidget(self.slider_widget, 1, 0, 5, 1)

    def add_parameters_widget(self):
        self.parameters_widget = ParametersWidget(self.optimiser)
        self.parameters_widget.add_parameters()
        self.optimiser = self.parameters_widget.optimiser
        self.grid_layout.addWidget(self.parameters_widget, 0, 1, 2, 1)

    def add_resolution_widget(self):
        self.resolution_widget = ResolutionWidget(self.optimiser)
        self.optimiser = self.resolution_widget.optimiser
        self.grid_layout.addWidget(self.resolution_widget, 0, 0, 1, 1)

    def _configure_layout(self):
        self.grid_layout = QGridLayout(self)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.margin = 4
        self.setMouseTracking(True)

        self.setWindowTitle("Apex Res")

        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = Window()
    window.showMaximized()

    sys.exit(app.exec_())
