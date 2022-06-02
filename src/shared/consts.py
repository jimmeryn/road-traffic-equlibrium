""" Consts - constant values used in the app"""
import os

from dotenv import load_dotenv

load_dotenv()

MULTI_STEP = False

ALGORITHM = os.getenv('ALGORITHM')
EXAMPLE_NUMBER = os.getenv('EXAMPLE_NUMBER')
MAX_ITERATION_COUNT = int(os.getenv('MAX_ITERATION_COUNT', '1000'))
MAX_ERROR = float(os.getenv('MAX_ERROR', '1e-14'))
ZERO_FLOW = float(os.getenv('ZERO_FLOW', '1e-15'))
DIR_TOLERANCE = float(os.getenv('DIR_TOLERANCE', '1e-15'))
