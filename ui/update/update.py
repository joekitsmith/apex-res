from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QPushButton, QSizePolicy

from slider.data_classes import SliderNames
from ui.update.check_initialise import check_optimiser_initialisable
from ui.utils.utils import check_if_number
from ui.parameters.names import (
    InstrumentParameterNames,
    MethodParameterNames,
    ConditionParameterNames,
    DataEntryParameterNames,
)


class UpdateUI:
    def __init__(self, chromatogram, parameters, sliders, resolution, data_entry):

        self.chromatogram_widget = chromatogram
        self.optimiser = self.chromatogram_widget.optimiser
        self.parameters_widget = parameters
        self.sliders_widget = sliders
        self.resolution_widget = resolution
        self.data_widget = data_entry

        self.parameters_widget.instrument.t0_input.setText("3.05")
        self.parameters_widget.instrument.td_input.setText("2.56")
        self.parameters_widget.instrument.n_input.setText("19000")
        self.data_widget.header.tg1_input.setText("15")
        self.data_widget.header.tg2_input.setText("30")
        self.data_widget.conditions.initial_input.setText("40")
        self.data_widget.conditions.final_input.setText("100")

        self._create_update_button()

        print(self.sliders_widget.sliders)

        for slider in self.sliders_widget.sliders.values():
            slider.valueChanged.connect(
                lambda val, slider=slider: self.update(val, slider=slider)
            )

        # for text_input in self.parameters_widget.parameters:
        #     if isinstance(text_edit, QLineEdit):
        #     text_input.returnPressed.connect(
        #         lambda name=text_input.objectName(): self.update(name=name)
        #     )

        for data_input in self.data_widget.data:
            data_input.returnPressed.connect(
                lambda name=data_input.objectName(): self.update(name=name)
            )

        # self.data_widget.analytes.table.keyPressed.connect(self.update)

    def update(self, val=None, name=None, slider=None):
        print("update")
        self._update_data_entry(name)
        self._update_parameters(name)
        if self.optimiser.is_initialised:
            self.optimiser.calculate()
            self.optimiser.predict()
            print("initialised")
            if slider is not None:
                self._set_optimiser_from_sliders(val, slider)
            self._update_plot()
            self._update_resolution()
        else:
            self._initialise_optimiser()

    def _initialise_optimiser(self):
        if check_optimiser_initialisable(self.optimiser):
            self.optimiser.initialise()

    def _update_plot(self):
        self.optimiser = self.chromatogram_widget.update_plot(self.optimiser)

    def _update_resolution(self):
        self.optimiser = self.resolution_widget.update_resolution(self.optimiser)

    def _update_data_entry(self, name):
        tg1_input = self.data_widget.header.tg1_input
        tg2_input = self.data_widget.header.tg2_input
        initial_input = self.data_widget.conditions.initial_input
        final_input = self.data_widget.conditions.final_input
        if tg1_input.text():
            tg1_input.setStyleSheet("""border: 1px solid green;""")
            self.optimiser.tg1 = float(tg1_input.text())
        else:
            tg1_input.setStyleSheet("""border: 1px solid red;""")

        if tg2_input.text():
            self.optimiser.tg2 = float(tg2_input.text())
            tg2_input.setStyleSheet("""border: 1px solid green;""")
        else:
            tg2_input.setStyleSheet("""border: 1px solid red;""")

        if initial_input.text():
            self.optimiser.phi0_init = float(initial_input.text()) / 100
            initial_input.setStyleSheet("""border: 1px solid green;""")
        else:
            initial_input.setStyleSheet("""border: 1px solid red;""")

        if final_input.text():
            self.optimiser.phif_init = float(final_input.text()) / 100
            final_input.setStyleSheet("""border: 1px solid green;""")
        else:
            final_input.setStyleSheet("""border: 1px solid red;""")

        self.optimiser = self.data_widget.analytes.table.optimiser

    def _update_parameters(self, name):
        instrument = self.parameters_widget.instrument
        method = self.parameters_widget.method

        t0_input = instrument.t0_input
        n_input = instrument.n_input
        td_input = instrument.td_input
        tg_input = method.tg_label
        phi0_input = method.phi0_label
        phif_input = method.phif_label

        self.optimiser = self._process_input(self.optimiser, t0_input, "t0")
        self.optimiser = self._process_input(self.optimiser, n_input, "n_est")
        self.optimiser = self._process_input(self.optimiser, td_input, "td")

    def _process_input(self, optimiser, text_input, attr):
        text = text_input.text()
        if check_if_number(text):
            setattr(optimiser, attr, float(text))
            text_input.setStyleSheet("""border: 1px solid green;""")
        else:
            text_input.setStyleSheet("""border: 1px solid red;""")

        return optimiser

    def _set_optimiser_from_sliders(self, val, slider):
        abs_val = val / slider.resolution

        print(slider.name)

        if slider.name == SliderNames.B0:
            bf_slider = self.sliders_widget.sliders[SliderNames.BF]
            if slider.value() < bf_slider.value():
                self.optimiser.phi0 = abs_val
            else:
                bf_slider.setValue(val)

        elif slider.name == SliderNames.BF:
            b0_slider = self.sliders_widget.sliders[SliderNames.B0]
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

    def _create_update_button(self):
        self.update_button = QPushButton("Update")  #
        self.update_button.setFixedHeight(40)
        self.update_button.setStyleSheet("""margin-top: 15px""")
        self.update_button.clicked.connect(self.update)
        method_param_layout = self.parameters_widget.method.grid_layout
        method_param_layout.addWidget(
            self.update_button,
            method_param_layout.rowCount() + 1,
            0,
            1,
            1,
            alignment=Qt.AlignBottom,
        )
