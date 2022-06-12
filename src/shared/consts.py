""" Consts - constant values used in the app"""
import os
from distutils.util import strtobool
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

MULTI_STEP = False

ALGORITHM = os.getenv('ALGORITHM')
EXAMPLE_NUMBER = os.getenv('EXAMPLE_NUMBER')
MAX_ITERATION_COUNT = int(os.getenv('MAX_ITERATION_COUNT', '1000'))
MAX_ERROR = float(os.getenv('MAX_ERROR', '1e-14'))
ZERO_FLOW = float(os.getenv('ZERO_FLOW', '1e-15'))
DIR_TOLERANCE = float(os.getenv('DIR_TOLERANCE', '1e-15'))
COMPARE_SOLUTION = strtobool(os.getenv("COMPARE_SOLUTION", 'False'))
GAP: Literal[0, 1] = int(os.getenv("GAP", '1'))  # REL: 0, MAX: 1
MU: float = float(os.getenv("MU", '0.5'))  # used in TAPAS
V: float = float(os.getenv("V", '0.25'))  # used in TAPAS
