from pathlib import Path
import sys

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

import pytest
import numpy as np

from resolution_equations import ResolutionEquations
