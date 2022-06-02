""" Main Program """
from src.data.test import run_test
from src.shared.consts import (ALGORITHM, EXAMPLE_NUMBER, MAX_ERROR,
                               MAX_ITERATION_COUNT)
from src.utils.user_input import UserInput


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
