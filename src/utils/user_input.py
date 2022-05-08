""" User Input """
from src.data.test import ALGORITHMS, DATA_LIST


def wrong_option():
    print("\nWrong option. Please try again.\n")


class UserInput:
    """
    Class used for the getting user input and displaying initial messages to the user.
    """
    @staticmethod
    def GetAlgorithm() -> int:
        while True:
            print("0 - Exit program")
            print("".join((f"{index} - {item.__name__}\n" for index,
                           item in ALGORITHMS.items())))
            user_input_alg = input("Algorithm index: ")

            try:
                if user_input_alg == '0' or int(user_input_alg) in ALGORITHMS:
                    break
                else:
                    wrong_option()
            except ValueError:
                wrong_option()

        return int(user_input_alg)

    @staticmethod
    def GetCity() -> int:
        while True:
            print("0 - Exit program")
            print("".join((f"{index} - {item}\n" for index,
                           item in DATA_LIST.items())))
            user_input_city = input("Data index: ")

            try:
                if user_input_city == '0' or int(user_input_city) in DATA_LIST:
                    break
                else:
                    wrong_option()
            except ValueError:
                wrong_option()

        return int(user_input_city)
