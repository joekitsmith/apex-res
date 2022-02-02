import math
import numpy as np

from models.two_gradient.resolution import Resolution


class TwoGradOptimisePlot:
    def __init__(self, fig_canvas, optimiser):
        """
        Parameters
        ----------
        fig_canvas : FigCanvas
            initialised figure to plot on
        optimiser : TwoGradOptimiser
            executes two gradient optimisation model
        """
        # number of x data points
        self.x_resolution = 1000
        # number of resolution data points when maximising
        self.res_resolution = 501

        # constant to modulate hight (inversely proportional)
        self.c = 100

        self.fig_canvas = fig_canvas

        self.optimiser = optimiser

    def generate_plot(self) -> None:
        """
        Plot initial conditions on chromatogram.
        """
        self.optimiser.predict()
        x, y = self._generate_x_y()

        # create plot on axis 1
        self.fig_canvas.ax1.set_visible(True)
        (self.graph,) = self.fig_canvas.ax1.plot(x, y, linewidth=1, color="black")

        # tidy graph
        self._set_limits()
        self._set_xticks()

    def update_plot(self, optimiser):
        """
        Update chromatogram with new data.
        """
        self.optimiser = optimiser

        # run model under currently set conditions
        self.optimiser.predict()
        x, y = self._generate_x_y()

        # add data to plot
        self.graph.set_data(x, y)
        self.fig_canvas.ax1.set_xlim([0, self.optimiser.tg_final])

        # tidy graph
        self._set_limits()
        self._set_xticks()

        self.fig_canvas.figure.canvas.draw()

    def plot_resolution_map(self):
        """
        Plot resolution map across allowed condition space.
        """
        ax2 = self.fig_canvas.ax2

        #
        m = np.linspace(0, 1, 501)
        n = np.linspace(0, 1, 501)
        o = np.array(np.meshgrid(m, n))
        p = o.transpose()
        valid = np.where((o[0] - o[1] >= 0.15))
        conditions = np.array(p[valid], dtype="float64")

        self.phi0 = conditions[:, 0]
        self.phif = conditions[:, 1]

        self.optimiser.predict()
        critical_res = Resolution.predict_resolution(self.optimiser)[1]
        critical_res = np.nan_to_num(critical_res)
        max_res = np.max(critical_res)

        ax2.tricontourf(
            self.phi0,
            self.phif,
            critical_res,
            levels=[0, max_res / 4, max_res / 2, max_res / 1.5, max_res],
            colors=["blue", "green", "yellow", "red"],
        )

    def _generate_x_y(self):
        """
        Generate x and summed y values of peaks in chromatogram.
        """
        x = np.linspace(0, self.optimiser.tg_final, self.x_resolution)

        time_diff_matrix, w_matrix, area_matrix = self._generate_mesh_arrays(x)

        h = area_matrix / (np.sqrt(np.pi) * self.c)
        y = h * np.exp(-1 * ((time_diff_matrix ** 2) / ((w_matrix / 2) ** 2)))

        total_y = np.sum(y, axis=0)

        self._get_y_max(y)

        return (x, total_y)

    def _get_y_max(self, y):
        max_y = np.nanmax(y)

        max_y = max_y + (0.1 * max_y)

        self.y_max = max_y

    def _generate_mesh_arrays(self, x):
        x_tr_mesh = np.meshgrid(x, self.optimiser.tr_pred)
        time_diff_matrix = x_tr_mesh[0] - x_tr_mesh[1]

        x_w_mesh = np.meshgrid(x, self.optimiser.w_pred)
        w_matrix = x_w_mesh[1]

        x_area_mesh = np.meshgrid(x, self.optimiser.area.mean(axis=1))
        area_matrix = x_area_mesh[1]

        return time_diff_matrix, w_matrix, area_matrix

    def _set_limits(self):
        """
        Set limits on x and y axis according to model parameters.
        """
        # set x limit to gradient time
        self.fig_canvas.ax1.set_xlim([0, self.optimiser.tg_final])
        # set y limit dependent slightly below 0 to maximum y
        if self.y_max != 0:
            self.fig_canvas.ax1.set_ylim([(0 - self.y_max / 100), self.y_max])

    def _set_xticks(self):
        """
        Set x-ticks of plot depending on current gradient time.
        """
        tg_final = self.optimiser.tg_final
        if tg_final <= 1:
            xticks = np.round(
                np.linspace(0, tg_final, math.floor((tg_final / 0.2) + 1)), 1
            )
        elif tg_final <= 2:
            xticks = np.round(
                np.linspace(0, tg_final, math.floor((tg_final / 0.4) + 1)), 1
            )
        elif tg_final <= 4:
            xticks = np.linspace(0, tg_final, math.floor((tg_final / 0.5) + 1))
        elif tg_final <= 20:
            xticks = range(0, math.floor(tg_final + 1), 1)
        elif tg_final <= 50:
            xticks = range(0, math.floor(tg_final + 1) + 1, 2)
        else:
            xticks = range(0, math.floor(tg_final + 1), 5)

        self.fig_canvas.ax1.set_xticks(xticks)
