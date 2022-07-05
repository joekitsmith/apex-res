import numpy as np

from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QEvent, Qt, pyqtSignal

from ui.utils.utils import check_if_number
from ui.update.check_initialise import check_optimiser_initialisable


class DataEntryTable(QTableWidget):

    keyPressed = pyqtSignal(int)

    def __init__(self, optimiser):
        super().__init__()
        self.optimiser = optimiser
        self.buffer_data = BufferData(self.optimiser)

    def update_model(self, index):
        row, column, cell_value = index.row(), index.column(), index.data()
        if check_if_number(cell_value):
            self.buffer_data.update(cell_value, row, column)
            self.optimiser = self.buffer_data.optimiser

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Return:
            indexes = self.selectedIndexes()
            self.update_model(indexes[0])
            self.keyPressed.emit(event.key())


class BufferData:
    """Stores values updated in table and controls when changes should be fed to the model."""

    def __init__(self, optimiser):
        self.optimiser = optimiser

        self.TR_1 = "tr1"
        self.AREA_1 = "area1"
        self.TR_2 = "tr2"
        self.AREA_2 = "area2"

    def update(self, value, row, column):
        attr = self.mapping()[column]
        if attr == self.TR_1:
            self.optimiser.data[row, 0, 0] = value
        elif attr == self.AREA_1:
            self.optimiser.data[row, 2, 0] = value
        elif attr == self.TR_2:
            self.optimiser.data[row, 0, 1] = value
        elif attr == self.AREA_2:
            self.optimiser.data[row, 2, 1] = value

    def mapping(self):
        return {0: self.TR_1, 1: self.AREA_1, 2: self.TR_2, 3: self.AREA_2}
