import json
from abc import ABC
from datetime import datetime, date

import sys
import abc
import psycopg2


class Account(metaclass=abc.ABCMeta):
    __is__abstract = True
    """An abstract class in python that serves as basis for modeling specific bank accounts"""

    def __init__(self):
        if self._is_abstract:
            raise RunTimeError("Abstract class instantiation.")

    @abc.abstractmethod
    def deposit(self, amount):
        """Deposits an amount of money"""
        return

    @abc.abstractmethod
    def withdraw(self, amount):
        """Withdraws an amount of money"""
        return

    @abc.abstractmethod
    def get_balance(self):
        """Checks the balance"""
        print(f"The current balance is {round(self.balance, 2)}")
        return

    @abc.abstractmethod
    def transfer(self, account_from, account_to, amount):
        """Transfers money between accounts"""
        return

    @abc.abstractmethod
    def add_interest(self):
        """Adds an interest to the balance"""
        self.balance = self.balance * (1 + self.int_rate)
        print(f"Interest added. Current balance of account {self.account_number} is: {round(self.balance, 2)}$")

    @abc.abstractmethod
    def transactions_history(self):
        """Prints a log of all transactions (deposits and withdraws)"""
        if len(self.transactions) < 1:
            print("No history available")
        else:
            for i in range(1, len(self.transactions)):
                print(f"Transaction history:\n{self.transactions[i]} on {datetime.today()}")

    def print_menu(self):
        """Prints a menu which allows to an user to choose among banking operations"""
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
                    self.deposit(amount_d)
                elif user_input == 2:
                    amount_w = int(input("Please, enter an amount to withdraw:\n"))
                    self.withdraw(amount_w)
                elif user_input == 3:
                    self.get_balance()
                elif user_input == 4:
                    self.transfer(self, CurrentAccount(input("Please, enter account to transfer:\n"), 0.05, 0),
                                  input("Please, enter amount to transfer:\n"))
                elif user_input == 5:
                    Writers.write_json(self.account_number)
                elif user_input == 6:
                    Writers.write_db(self.account_number)
                elif user_input == 7:
                    print("Thank you for using our banking system!")
                    sys.exit(0)
        except ValueError:
            print("Please try again by entering a valid input between 1-7")
            raise ValueError

    def __repr__(self):
        return '{0.__class__.__name__}(account_number={0.account_number}, balance={0.balance})'.format(self)

    def __str__(self):
        return f"account number: {self.account_number}"


class CurrentAccount(Account, ABC):

    def __init__(self, account_number, int_rate, balance):
        super().__init__(account_number, int_rate, balance, account_type="current")
        self.Writers = Writers
        self.account_number = account_number
        self.opening_date = date.today()
        self.int_rate = int_rate
        self.balance = balance
        self.account_type = "current"

        self.transactions = []

    def deposit(self, amount):
        try:
            if int(amount) < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            else:
                self.balance += int(amount)
                self.transactions.append(f"Deposit of {int(amount)}$. Interest added. ")
                print(f"Amount of {int(amount)}$ deposited to account {self.account_number}")
                self.add_interest()
        except TypeError:
            raise TypeError

    def withdraw(self, amount):
        try:
            if int(amount) < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            elif self.balance < int(amount):
                print(f"The withdrawn {int(amount)}$ exceed your balance of {round(self.balance, 2)}$")
                raise ValueError
            else:
                self.add_interest()
                self.balance -= int(amount)
                self.transactions.append(f"Withdraw of {int(amount)}$. Interest added.")
                print(f"Amount of {int(amount)}$ withdrawn from account {self.account_number}")
        except TypeError:
            raise TypeError

    def transfer(self, account_from, account_to, amount):
        try:
            if int(amount) < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            else:
                account_from.withdraw(amount)
                account_to.deposit(amount)
        except TypeError:
            raise TypeError


class DepositAccount(Account, ABC):

    def __init__(self, account_number, int_rate, balance):
        super().__init__(account_number, int_rate, balance, account_type="deposit")
        self.Writers = Writers
        self.account_number = account_number
        self.opening_date = date.today()
        self.int_rate = int_rate
        self.balance = balance
        self.account_type = "deposit"

        self.transactions = []
        self.term_date = date(2020, 3, 5)

    def deposit(self, amount):
        try:
            if amount < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            elif self.term_date == date.today():
                self.balance += amount
                self.transactions.append(f"Deposit of {amount}$. Interest added.")
                print(f"Amount of {amount}$ deposited to account {self.account_number}")
                self.add_interest()
            else:
                print(f"It is not the term date. Term date is on {self.term_date}")
        except TypeError:
            raise TypeError

    def withdraw(self, amount):
        try:
            if int(amount) < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            elif self.balance < amount:
                print(f"The withdrawn {amount}$ exceed your balance of {round(self.balance, 2)}$")
                raise ValueError
            elif self.term_date == date.today():
                self.add_interest()
                self.balance -= amount
                self.transactions.append(f"Withdraw of {amount}$. Interest added.")
                print(f"Amount of {amount}$ withdrawn from account {self.account_number}")
            else:
                print(f"It is not the term date. Term date is on {self.term_date}")
        except TypeError:
            raise TypeError

    def transfer(self, account_from, account_to, amount):
        try:
            if amount < 0:
                print("Please enter a valid positive value.")
                raise ValueError
            elif self.term_date == date.today():
                account_from.withdraw(amount)
                account_to.deposit(amount)
            else:
                print(f"It is not the term date. Term date is on {self.term_date}")
        except TypeError:
            raise TypeError


class Writers(Account, ABC):

    def __init__(self, account_number, opening_date, int_rate, account_type):
        super().__init__(account_number, opening_date, int_rate, account_type)
        self.transactions = Account.transactions_history(self)
        Account.get_balance(self)

    def write_db(self):
        try:
            conn = psycopg2.connect(database="account_data",
                                    port="5432",
                                    user="postgres",
                                    password="test123")
            cur = conn.cursor()
            print(self.transactions)
            for d in self.transactions:
                cur.execute("INSERT INTO account_data (transaction, account_number) "
                            "VALUES (%s, %s);", (d, self.account_number))
                conn.commit()
                print(cur.rowcount, "record inserted.")
            cur.close()
            conn.close()
        except psycopg2.Error:
            print("Unable to connect to the database")

    def write_json(self):
        account_data = {self.account_number: [
            {'Balance': str(round(self.balance, 2)) + '$', 'Transactions_history': self.transactions}]}
        with open('account_data.json', 'w'):
            json1 = json.dumps(account_data, indent=4)
            print(json1)


class Main:
    # curr1 = CurrentAccount("123", 0.05, 100)
    # curr2 = CurrentAccount("124", 0.05, 0)
    # curr1.transfer(curr1, curr2, 50)
    # curr1.print_menu()

    dep1 = DepositAccount("125", 0.10, 0)
    dep2 = DepositAccount("126", 0.10, 0)

    dep1.print_menu()


if __name__ == '__main__':
    pass
