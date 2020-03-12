from abc import ABC

import psycopg2
import json
from Accounts import Account


class Writers(ABC):

    def __init__(self, a: Account):
        self.account = a

    def write_db(self):
        try:
            conn = psycopg2.connect(database="account_data",
                                    port="5432",
                                    user="postgres",
                                    password="test123")
            cur = conn.cursor()
            print(self.account.transactions)
            for d in self.account.transactions:
                cur.execute("INSERT INTO account_data (transaction, account_number) "
                            "VALUES (%s, %s);", (d, self.account.account_number))
                print(cur.rowcount, "record inserted.")

            # commit after all records are inserted so that in case of failure
            # rollback will apply to all records
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error:
            print("Unable to connect to the database")

    def write_json(self):
        account_data = {self.account.account_number: [
            {'Balance': str(round(self.account.balance, 2)) + '$', 'Transactions_history': self.account.transactions}]}
        with open('account_data.json', 'w'):
            json1 = json.dumps(account_data, indent=4)
            print(json1)

    @staticmethod
    def read_db(account_number: str) -> Account:
        # TODO: implement
        raise NotImplementedError
