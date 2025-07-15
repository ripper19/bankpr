import datetime
from .accounts import Account
CHECKING  = "Checking account"
SAVINGS = "Savings account"

class savings_Account(Account):
    def __init__(self, owner,balance=0, interest_rate = 0.3, waiting_period = 3):
        super().__init__(owner,SAVINGS, balance)
        self.pending_withdrawal = None
        self.interest_rate = interest_rate
        self.waiting_period = waiting_period

    def earn_interest(self):
        interest = self.balance*self.interest_rate
        self.balance +=interest

    def request_withdraw(self,amount):
        if self.pending_withdrawal is not None:
            return False
        if amount > self.balance:
            return False
        release_date = datetime.date.today() + datetime.timedelta(days=self.waiting_period)
        self.pending_withdrawal = (amount, release_date)

    def withdraw(self):
        if self.pending_withdrawal is None:
            return False
        amount, release_date = self.pending_withdrawal
        if  datetime.date.today() >= release_date:
            self.balance -= amount
            self.pending_withdrawal is None
            return True