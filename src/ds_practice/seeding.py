"""Consistent random seeding for reproducible results."""
from __future__ import annotations

import os
import random


def set_seed(seed: int = 42) -> int:
    """Seed the standard-library and NumPy RNGs; return the seed used."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:  # numpy is a hard dependency, but seeding must not break
        pass
    return seed
