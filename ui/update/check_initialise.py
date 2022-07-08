import numpy as np


def check_optimiser_initialisable(optimiser):
    values = [optimiser.phi0_init, optimiser.phif_init, optimiser.tg1, optimiser.tg2, optimiser.td, optimiser.t0]

    if None in values:
        return False
    else:
        count = 0
        for row in optimiser.data:
            if np.all(np.delete(row, (1), axis=0) != 0):
                count += 1

        if count > 1:
            return True

    return False
