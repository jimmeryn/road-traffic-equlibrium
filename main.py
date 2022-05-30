""" Main Program """
import os

from dotenv import load_dotenv

from src.data.test import run_test
from src.shared.consts import MAX_ERROR, MAX_ITERATION_COUNT
from src.utils.user_input import UserInput

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
EXAMPLE_NUMBER = os.getenv('EXAMPLE_NUMBER')


def main():
    while True:
        if not ALGORITHM:
            alg_index = UserInput.GetAlgorithm()
            if alg_index == 0:
                break
        else:
            alg_index = int(ALGORITHM)
        if not EXAMPLE_NUMBER:
            city_index = UserInput.GetCity()
            if city_index == 0:
                break
        else:
            city_index = int(EXAMPLE_NUMBER)

        run_test(
            city_index,
            alg_index,
            MAX_ERROR,
            MAX_ITERATION_COUNT
        )
        if ALGORITHM or input("Press Enter to continue or 0 to exit.\n") == '0':
            break


if __name__ == "__main__":
    main()
