"""
Main Program
0 - Exit program
1 - Four Nodes test
"""

from src.data.test import DATA_LIST, run_test


def main():
    run_test(0)
    return

    user_input = None
    while True:
        print("Run testing for A Algorithm\n")
        print("0 - Exit program")
        print("".join((f"{index + 1} - {item}\n" for index,
              item in enumerate(DATA_LIST))))
        user_input = input("Data index: ")
        print("\n")

        if user_input == '0':
            break

        try:
            city_index = int(user_input) - 1
            run_test(city_index)
            input("Press Enter to continue...\n")
        except IndexError:
            print("Wrong option. Please try again\n")


if __name__ == "__main__":
    main()
