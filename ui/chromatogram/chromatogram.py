from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../../").resolve()
sys.path.append(str(root_dir))

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from models.two_gradient.plot import TwoGradOptimisePlot

from .figure_canvas import ChromatogramCanvas


class ChromatogramWidget(QWidget):
    def __init__(self, optimiser):
        """
        optimiser : TwoGradOptimise
            initialised optimiser object with parameters calculated and tr, w predicted
        """
        super(ChromatogramWidget, self).__init__()

        self.optimiser = optimiser

        self._initialise()

    def create_plot(self):
        """
        Plot optimiser data onto chromatogram canvas.
        """
        self.plotter = TwoGradOptimisePlot(self.figure, self.optimiser)
        self.v_layout.addWidget(self.plotter.fig_canvas, 0)

    def update_plot(self, optimiser):
        """
        Update plot with new optimiser conditions.
        """
        self.optimiser = optimiser
        if not self.plotter.plot_generated:
            self.plotter.generate_plot()
        self.plotter.update_plot(self.optimiser)

        return self.optimiser

    def _initialise(self):
        """
        Create chromatogram canvas.
        """
        self.setObjectName("ChromatogramWidget")

        self.figure = ChromatogramCanvas()

        self.v_layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
