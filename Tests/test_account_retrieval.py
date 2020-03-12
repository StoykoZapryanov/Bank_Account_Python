from unittest import TestCase
from Writers import Writers
from Accounts import *


class TestAccountRetrieval(TestCase):

    def test_db_readwrite(self):
        account_num = 'TS4545'
        created_account = CurrentAccount(account_num, 10, 1000)

        w = Writers(created_account)
        w.write_db()

        retrieved_account = Writers.read_db(account_num)
        self.assertEqual(retrieved_account.get_balance, created_account.get_balance())
