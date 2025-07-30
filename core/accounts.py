from abc import ABC, abstractmethod
class Account(ABC):
        
        def __init__(self, acc_num, balance):
              self.acc_num = acc_num
              self.balance =balance
              
        @abstractmethod
        def withdraw(self, amount):
            pass

        def Deposit(self, amount):
            self.balance += amount
            return self.balance
        
        @staticmethod
        def sortaccount(acc_num, balance, account_type):
              from core.checking import checking_Account
              if account_type == "Checking account":
                    return checking_Account(acc_num, balance)
              elif account_type == "Savings account":
                    from core.savings import savings_Account

                    return savings_Account(acc_num, balance)
              else:
                    raise ValueError(f"Cannot find this {account_type}")