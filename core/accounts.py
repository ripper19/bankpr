import psycopg2
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
              
        
