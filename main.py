""" Main Program """
from src.data.test import run_test
from src.utils.user_input import UserInput

MAX_ERROR = 1e-10
MAX_ITERATION_COUNT = 3


def main():
    while True:
        alg_index = UserInput.GetAlgorithm()
        if alg_index == 0:
            break
        city_index = UserInput.GetCity()
        if city_index == 0:
            break

        run_test(city_index, alg_index, MAX_ERROR, MAX_ITERATION_COUNT)
        if input("Press Enter to continue or 0 to exit.\n") == '0':
            break


if __name__ == "__main__":
    main()
