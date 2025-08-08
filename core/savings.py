import datetime
from .accounts import Account
from .exceptions import PendingWithdrawerror

class savings_Account(Account):
    def __init__(self, acc_num, balance=0, interest_rate = 0.3, pending_withdrawal=None, release_date = None):
        super().__init__(acc_num, balance)
        self.pending_withdrawal = pending_withdrawal
        self.interest_rate = interest_rate
        self.release_date = release_date
        self.balance =float(balance)

    def earn_interest(self):
        interest = self.balance*self.interest_rate
        self.balance +=interest

    def request_withdraw(self,amount):
        if self.pending_withdrawal is not None:
            raise PendingWithdrawerror("Account has a pending withdrawal")
        
        amount = float(amount)
        
        if amount is None:
            raise ValueError("Amount cant be none")
        if amount > self.balance:
            raise ValueError("Not enough money")
        release_date = datetime.date.today() + datetime.timedelta(days=3)
        self.pending_withdrawal = (amount,release_date)
        return self.pending_withdrawal
    
    def process_pending_withdrawal(self):
        if self.pending_withdrawal is None:
            raise ValueError("No Pending Withdrawal.")
        amount, release_date = self.pending_withdrawal
        if  datetime.date.today() >= release_date:
            self.balance -= amount
            self.pending_withdrawal is None
            return True
        return False
    def withdraw(self, amount):
        return self.request_withdraw(amount)
    
    def __iter__(self):
        if self.pending_withdrawal is not None:
            yield self.pending_withdrawal[0]
            yield self.pending_withdrawal[1]
