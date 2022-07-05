def check_if_number(cell_value) -> bool:
    try:
        num = float(cell_value)
        return True

    except:
        return False