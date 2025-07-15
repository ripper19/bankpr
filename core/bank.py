from db import PostConnection
from threading import RLock
import os
from dotenv import load_dotenv
import random
import psycopg2
from .exceptions import DatabaseError,accountexistserror,createAccountError
import logging
from core.checking import checking_Account
from core.savings import savings_Account
load_dotenv()

class Bank:
    def __init__(self):
        self.post = PostConnection( 
        DB_HOST=os.getenv('DB_HOST'),
        DB_PORT=int(os.getenv('DB_PORT')),
        DB_NAME=os.getenv('DB_NAME'),
        DB_USER=os.getenv('DB_USER'),
        DB_PASSWORD=os.getenv('DB_PASSWORD'))

        self.cursor = self.post.get_cursor()
        self.gen_lock = RLock()
        logging.basicConfig(
            filename = "bank_errors.log",
            level = logging.ERROR,
            format = '%(acstime)s - %(levelname)s, %(message)s'
        )

    def generate(self):
        print("[DEBUG] Entered create_account")
        with self.gen_lock:
            print("[DEBUG] Acquired lock") 
            while True:
                acc_num = str(random.randint(100000,999999))
                self.cursor.execute ("SELECT 1 FROM accounts WHERE account_number = %s LIMIT 1",(acc_num,))

                if not self.cursor.fetchone():
                    return acc_num
    
    def log_error(self, err_mess):
        logging.error(err_mess)

    def check_double(self, owner, acc_type):
        try:
            self.cursor.execute(
            "SELECT 1 from accounts WHERE owner_ID = %s AND account_type = %s LIMIT 1",(owner.PiD, acc_type)
            )
            return self.cursor.fetchone() is not None
        except psycopg2.Error as e:
            self.post.rollback()
            raise DatabaseError (f"Failed to check {e.pgerror}")
        
    
    def create_account(self, owner, acc_type, balance = 0):
        with self.gen_lock:
            try:
                if self.check_double(owner, acc_type):
                    raise accountexistserror(f"Account for user{owner.Fname}, {acc_type} exists")
        
                acc_num = self.generate()
                self.cursor.execute(
    "INSERT INTO accounts (account_number, owner_name, owner_id, account_type, balance) "
    "VALUES (%s, %s, %s, %s, %s) RETURNING account_number",
    (str(acc_num), owner.Fname, owner.PiD, acc_type, float(balance))
)


                result = self.cursor.fetchone()
                self.post.commit()
                return result[0]
        
            except psycopg2.Error as e:
                self.post.rollback()
                raise createAccountError(f"Cant perform action {e.pgcode}: {e.pgerror}")

    def get_account(self, acc_num):
        with self.gen_lock:
            try:
                self.cursor.execute(
                    "SELECT account_type,balance FROM accounts WHERE account_number = %s",(acc_num,)
                    )
                row = self.cursor.fetchone()

                if not row:
                    raise ValueError("No account!!")
                
                account_type , balance = row

                if account_type == "Checking account":
                    return checking_Account(acc_num, balance)
                elif account_type == "Savings account":
                    return savings_Account(acc_num, balance)
                else:
                    raise ValueError(f"Invalid account type {account_type}")
            except psycopg2.Error as e:
                self.post.rollback()
                raise DatabaseError(f"Unable to access database {e.pgerror}")

    def withdraw(self, acc_num, amount):
        with self.gen_lock:
            try:
                account = self.get_account(acc_num)
                if not account:
                    raise ValueError(f"No account for {acc_num}")
                new_balance = account.withdraw(amount)

                self.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",(new_balance, acc_num,)
                )
                self.post.commit()
                return new_balance
            except Exception as e:
                self.post.rollback()
                self.log_error(f"error {str(e)}")
                raise 