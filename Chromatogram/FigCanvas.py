from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from matplotlib.widgets import Slider, Button

class CustomFigCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure(figsize=(8, 4))
        self.fig.set_facecolor((0.906,0.906,0.906,0.5))

        FigureCanvas.__init__(self, self.fig)
        
    def drawChromatogram(self):
        self.ax1 = self.fig.add_axes([0.05, 0.05, 0.92, 0.9])
        self.ax1.set_facecolor((0.906,0.906,0.906,0.001))
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.tick_params(labelsize = 8)
        self.ax1.minorticks_on()

        self.ax_maximise = self.fig.add_axes([0.72, 0.91, 0.2, 0.05])
        self.b_maximise = Button(self.ax_maximise, 'Maximise resolution')

        self.ax1.set_visible(False)
        self.ax_maximise.set_visible(False)

    def drawResMap(self):
        self.ax2 = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax2.set_facecolor((0,0,0,0.5))
        self.ax2.tick_params(labelsize=8)