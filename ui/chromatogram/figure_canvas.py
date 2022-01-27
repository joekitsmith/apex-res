from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button


class ChromatogramCanvas(FigureCanvas):
    def __init__(self):

        super(ChromatogramCanvas, self).__init__()

        self.figure = Figure(figsize=(8, 4))
        self.figure.set_facecolor((0.906, 0.906, 0.906, 0.5))

        FigureCanvas.__init__(self, self.figure)

        self._initialise()

    def _initialise(self):
        """
        Initialise chromatogram axes and make them invisible.
        """
        # create axis with defined colour
        self.ax1 = self.figure.add_axes([0.05, 0.05, 0.92, 0.9])
        self.ax1.set_facecolor((0.906, 0.906, 0.906, 0.001))
        # set invisible
        self.ax1.spines["top"].set_visible(False)
        self.ax1.spines["right"].set_visible(False)
        self.ax1.set_visible(False)
        # define tick properties
        self.ax1.tick_params(labelsize=8)
        self.ax1.minorticks_on()

        # maximise axis
        self.ax_maximise = self.figure.add_axes([0.72, 0.91, 0.2, 0.05])
        self.ax_maximise.set_visible(False)

        # maximise button
        self.b_maximise = Button(self.ax_maximise, "Maximise resolution")

    def draw_res_map(self):
        """
        Initialise resolution map axis.
        """
        # create axis with defined colour
        self.ax2 = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax2.set_facecolor((0, 0, 0, 0.5))
        # define tick properties
        self.ax2.tick_params(labelsize=8)
