from abc import ABC
from datetime import datetime, date

import abc


class Account(metaclass=abc.ABCMeta):
    _is_abstract = True
    """An abstract class in python that serves as basis for modeling specific bank accounts"""

    def __init__(self, account_number: str):
        self.account_number = account_number
        self.int_rate = 0
        self.transactions = []

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
        return self.balance

    @abc.abstractmethod
    def transfer(self, account_from, account_to, amount):
        """Transfers money between accounts"""
        return

    @abc.abstractmethod
    def add_interest(self):
        """Adds an interest to the balance"""
        self.balance = self.balance * (1 + self.int_rate)
        return self.get_balance()

    @abc.abstractmethod
    def transactions_history(self):
        return self.transactions

    def __repr__(self):
        return '{0.__class__.__name__}(account_number={0.account_number}, balance={0.balance})'.format(self)

    def __str__(self):
        return f"account number: {self.account_number}"


class CurrentAccount(Account, ABC):

    def __init__(self, account_number, int_rate, balance):
        super().__init__(account_number)
        self.opening_date = date.today()
        self.int_rate = int_rate
        self.balance = balance
        self.account_type = "current"

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
        super().__init__(account_number)
        self.opening_date = date.today()
        self.int_rate = int_rate
        self.balance = balance
        self.account_type = "deposit"

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


