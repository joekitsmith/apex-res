from PyQt5.QtWidgets import QHBoxLayout

def combine_field_and_value(field, value):
    h_layout = QHBoxLayout()
    h_layout.setSpacing(8)
    h_layout.addWidget(field, 0)
    h_layout.addWidget(value, 1)

    return h_layout