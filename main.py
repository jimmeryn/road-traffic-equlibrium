""" Main Program """
from src.data.test import run_test
from src.utils.user_input import UserInput


def main():
    while True:
        alg_index = UserInput.GetAlgorithm()
        if alg_index == 0:
            break
        city_index = UserInput.GetCity()
        if city_index == 0:
            break

        run_test(city_index, alg_index)
        input("Press Enter to continue...\n")


if __name__ == "__main__":
    main()
