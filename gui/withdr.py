from core import tk, ttk
from core.bank import Bank

class WithdrawFormHandler():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Withdrawals")
        self.bank = Bank()
        self.withdrawal_info()
        self.root.mainloop()

    def withdrawal_info(self):
        self.form = ttk.Frame(self.root, padding=20)
        self.form.grid()

        ttk.Label(self.form, text="Withdrawals").grid(column=0, row=1)

        ttk.Label(self.form, text="Account to withdraw from :").grid(column=0, row=2)
        self.with_from_account = ttk.Entry(self.form)
        self.with_from_account.grid(column=1, row=2)

        ttk.Label(self.form, text="Amount to withdraw : ").grid(column=0, row=3)
        self.with_amount = ttk.Entry(self.form)
        self.with_amount.grid(column=1, row=3)

        ttk.Button(self.form, command=self.with_dr, text="withdraw").grid(column=0, row=5)
        ttk.Button(self.form, text= "Back <--", command=self.goback).grid(column=1, row=5)

        self.show_status = ttk.Label(self.form, text="")
        self.show_status.grid(column=0, row= 7, columnspan=2)

    def with_dr(self):
        account_number = self.with_from_account.get()
        amount = self.with_amount.get()
        if not all([account_number, amount]):
            self.status_show("Enter dets!!", "red")
        
        current_balance = self.bank.withdraw(account_number, amount)
        print(f"Withdrawal of {amount} balance is {current_balance}")

        self.root.after(0, lambda: [
            self.status_show(f"Successfully withdrawn {amount} from {account_number}", "green"),
            self.clearForm()
        ])
    def status_show(self, message,color):
        self.show_status.config(text=message, foreground=color)
    def clearForm(self):
        self.with_from_account.delete(0, "end")
        self.with_amount.delete(0, "end")
        self.form.after(3000, lambda: self.show_status.config(text = ""))
    def goback(self):
        self.root.destroy()
        from gui.mgui import MainPage
        MainPage()
