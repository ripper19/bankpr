from core import tk,ttk
from core.bank import Bank

class transfersFormHandler():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Transfer money")
        self.bank = Bank()
        self.transferDetails()
        self.root.mainloop()
        

    def transferDetails(self):
        self.form = ttk.Frame(self.root, padding=20)
        self.form.grid()

        ttk.Label(self.form, text="Transder Money").grid(column=0, row=1)

        ttk.Label(self.form, text="Account to creedit: ").grid(column=0, row=4)
        self.cred_acc =  ttk.Entry(self.form)
        self.cred_acc.grid(column=1, row=4)

        ttk.Label(self.form, text="Account to debit: "). grid(column=0, row=6)
        self.deb_acc = ttk.Entry(self.form)
        self.deb_acc.grid(column=1, row=6)

        ttk.Label(self.form, text="Amount :").grid(column=0, row=9)
        self.amount = ttk.Entry(self.form)
        self.amount.grid(column=1, row=9)

        ttk.Button(self.form, text="Transfer", command=self.performtransfer).grid(column=0, row=12)

        ttk.Button(self.form, text="Back"). grid(column=1, row=12)

        self.show_status = tk.Label(self.form, text="")
        self.show_status.grid(column=0, row=16, columnspan=15)

    def performtransfer(self):
        cred_account = self.cred_acc.get()
        deb_account = self.deb_acc.get()
        amount = self.amount.get()

        if not all([cred_account, deb_account,amount]):
            self.status_show("Please input all details", "red")

        current_balance = self.bank.transfers(cred_account,deb_account,amount)
        print(f"Transferred {amount} current balance {current_balance}")

        self.root.after(0, lambda:[
            self.status_show(f"Successfully transferred {amount} from {cred_account} to {deb_account}", "green"),
            self.clearform()
        ])

    def status_show(self, message, color):
        self.show_status.config(text=message, foreground=color)
    def clearform(self):
        self.cred_acc.delete(0, "end")
        self.deb_acc.delete(0, "end")
        self.amount.delete(0, "end")
        self.form.after(3000, lambda: self.show_status.config(text=""))
