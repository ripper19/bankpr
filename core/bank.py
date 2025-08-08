from db import PostConnection
from threading import RLock
import os
from dotenv import load_dotenv
import random
import psycopg2
from .exceptions import DatabaseError,accountexistserror,createAccountError
import logging
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

    def get_check_account(self, acc_num):
        from core.accounts import Account
        with self.gen_lock:
            try:
                self.cursor.execute(
                    "SELECT account_type, balance FROM accounts WHERE account_number = %s AND account_type = 'Checking account'",(acc_num,)
                    )
                row = self.cursor.fetchone()

                if not row:
                    return None
                
                account_type , balance = row
                print(acc_num, balance, account_type)
                return Account.sortaccount(acc_num, balance, account_type)
            
            except psycopg2.Error as e:
                self.post.rollback()
                raise DatabaseError(f"Unable to access database {e.pgerror}")
            
    def get_savings_account(self, acc_num):
        from core.accounts import Account
        with self.gen_lock:
            try:
                self.cursor.execute(
                    "SELECT account_type, balance, pending_withdrawal,release_date FROM accounts WHERE account_number = %s AND account_type = 'Savings account'",(acc_num,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                
                account_type, balance,pending_withdrawal,release_date = row
                print(account_type,balance,pending_withdrawal,release_date)
                return Account.sortaccount(acc_num, balance,account_type,pending_withdrawal,release_date)
            except psycopg2.Error as e:
                self.post.rollback()
                raise DatabaseError(f"Cant access db {e.pgerror}")

    def withdraw(self, acc_num, amount):
        with self.gen_lock:
            try:
                check = self.get_check_account(acc_num)
                if check and check.account_type == "Checking account":
                    new_balance = check.withdraw(amount)
                    self.cursor.execute(
                        "UPDATE accounts SET balance = %s WHERE account_number = %s RETURNING balance",(new_balance,acc_num,)
                    )

                    ded_balance = self.cursor.fetchone()[0]
                    self.post.commit()
                    return ded_balance
                else:
                    save = self.get_savings_account(acc_num)
                    if save:
                        new_details = save.request_withdraw(amount)
                        if new_details is False:
                            raise ValueError("Insufficient funds or No requested withdraw")
                        else:
                            amount, release_date = new_details
                            self.cursor.execute(
                                "UPDATE accounts SET pending_withdrawal = %s,release_date =%s WHERE account_number = %s RETURNING release_date",(amount,release_date,acc_num)
                                )
                            updated_dets = self.cursor.fetchone()[0]
                            self.post.commit()
                            return updated_dets
            except psycopg2.Error as e:
                self.post.rollback()
                self.log_error(f"error {str(e)}")
                raise DatabaseError(f"cant access db {e.pgerror}")
    def transfers(self, from_acc_num, to_acc_num, amount):
        with self.gen_lock:
            try:
                creditor = self.get_check_account(from_acc_num)
                debitor = self.get_check_account(to_acc_num)

                if creditor.balance < float(amount) :
                    raise ValueError("Not enough money")
                
                source_balance = creditor.withdraw(amount)
                target_balance = debitor.Deposit(amount)

                self.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s", (source_balance, creditor.acc_num,)
                )
                self.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s", (target_balance, debitor.acc_num,)
                )
                self.post.commit()
                return source_balance
            except Exception as e:
                self.post.rollback()
                self.log_error(f"error {str(e)}")
                raise