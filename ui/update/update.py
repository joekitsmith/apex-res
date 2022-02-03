from slider.data_classes import SliderNames


class UpdateUI:
    def __init__(self, chromatogram, parameters, sliders, resolution):

        self.chromatogram = chromatogram
        self.optimiser = self.chromatogram.optimiser
        self.parameters = parameters
        self.sliders = sliders.sliders
        self.resolution = resolution

        for slider in self.sliders.values():
            slider.valueChanged.connect(
                lambda val, slider=slider: self.update(val, slider)
            )

    def update(self, val, slider):
        self._set_parameters_text(val, slider)
        self._set_optimiser_and_slider_value(val, slider)

        self.optimiser.predict()

        self._update_plot()
        self._update_resolution()

    def _set_parameters_text(self, val, slider):
        pass

    def _update_plot(self):
        self.chromatogram.update_plot(self.optimiser)

    def _update_resolution(self):
        self.resolution.update_resolution(self.optimiser)

    def _set_optimiser_and_slider_value(self, val, slider):
        abs_val = val / slider.resolution

        if slider.name == SliderNames.B0:
            bf_slider = self.sliders[SliderNames.BF]
            if slider.value() < bf_slider.value():
                self.optimiser.phi0 = abs_val
            else:
                bf_slider.setValue(val)

        elif slider.name == SliderNames.BF:
            b0_slider = self.sliders[SliderNames.B0]
            if slider.value() > b0_slider.value():
                self.optimiser.phif = abs_val
            else:
                b0_slider.setValue(val)

        elif slider.name == SliderNames.TG:
            self.optimiser.tg_final = abs_val

        elif slider.name == SliderNames.T0:
            self.optimiser.t0 = abs_val

        elif slider.name == SliderNames.TD:
            self.optimiser.td = abs_val

        elif slider.name == SliderNames.FLOW_RATE:
            self.optimiser.flow_rate = abs_val

        elif slider.name == SliderNames.COLUMN_LENGTH:
            self.optimiser.column_length = abs_val

        elif slider.name == SliderNames.COLUMN_DIAMETER:
            self.optimiser.column_diameter = abs_val

        elif slider.name == SliderNames.PARTICLE_SIZE:
            self.optimiser.particle_size = abs_val
