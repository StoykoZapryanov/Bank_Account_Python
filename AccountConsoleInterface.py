import sys

from Accounts import *
from Writers import Writers


class AccountConsoleInterface:
    def print_menu(a: Account):
        """Prints a menu which allows to an user to choose among banking operations"""
        w = Writers(a)
        try:
            while 1:
                print("1.Deposit\n"
                      "2.Withdraw\n"
                      "3.Balance\n"
                      "4.Transfer\n"
                      "5.Write JSON\n"
                      "6.Write DB\n"
                      "7.Exit")
                user_input = int(input("Please, enter your choice:\n"))
                if user_input == 1:
                    amount_d = int(input("Please, enter an amount to deposit:\n"))
                    a.deposit(amount_d)
                elif user_input == 2:
                    amount_w = int(input("Please, enter an amount to withdraw:\n"))
                    a.withdraw(amount_w)
                elif user_input == 3:
                    a.get_balance()
                elif user_input == 4:
                    a.transfer(a, CurrentAccount(input("Please, enter account to transfer:\n"), 0.05, 0),
                                  input("Please, enter amount to transfer:\n"))
                elif user_input == 5:
                    w.write_json()
                elif user_input == 6:
                    w.write_db()
                elif user_input == 7:
                    print("Thank you for using our banking system!")
                    sys.exit(0)
        except ValueError:
            print("Please try again by entering a valid input between 1-7")
            raise ValueError
