from .accounts import Account
CHECKING  = "Checking account"
SAVINGS = "Savings account"

class checking_Account(Account):
    def __init__(self, acc_num, balance):
        super().__init__(acc_num, balance)

        self.balance = float(balance)

    def withdraw(self, amount):
        if float(amount) > self.balance:
            raise ValueError("Insufficient funds please perform an overdraft")
        else:
            self.balance -= float(amount)
            return self.balance
        