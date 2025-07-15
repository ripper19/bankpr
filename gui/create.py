from core import threading, tk, ttk, accountexistserror, createAccountError, Bank
from models import Owner

class AccountFormHandler():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Create Account")
        self.bank = Bank()
        print("[DEBUG] Bank initialized")
        self.setupinfo()
        self.root.mainloop()

    def setupinfo(self):
        self.form = ttk.Frame(self.root, padding=20)
        self.form.grid()
#nameentry
        ttk.Label(self.form, text="Full Name:").grid(column=0, row=1)
        self.name_entry = ttk.Entry(self.form)
        self.name_entry.grid(column=1, row=1)
#id
        ttk.Label(self.form, text="ID number").grid(column=0, row=2)
        self.id_entry = ttk.Entry(self.form)
        self.id_entry.grid(column=1, row=2)

#accttype
        self.acc_type = tk.StringVar()
        ttk.Label(self.form, text="Choose Account : ").grid(column=0, row=3)
        ttk.Radiobutton(self.form, variable=self.acc_type, value="Checking account", text="Checking Account").grid(column=0, row=4)
        ttk.Radiobutton(self.form, variable=self.acc_type, value="Savings account", text="Savings Account").grid(column=0, row=5)


        ttk.Label(self.form, text="First deposit amount: ").grid(column=0, row=6)
        self.first_depo = ttk.Entry(self.form)
        self.first_depo.grid(column=1, row=6)
        
        self.submit_button = ttk.Button(self.form, command=self.submit, text="Submit")
        self.submit_button.grid(column=0, row=9)

        self.backbtn = ttk.Button(self.form, text= "Back<--", command = self.goback)
        self.backbtn.grid(column= 1, row=9)

        self.status_bar = ttk.Label(self.form, text="")
        self.status_bar.grid(column=0, row=12, columnspan=2)

    def submit(self):
        def db_task():
            try:
                Fname = self.name_entry.get()
                PiD = self.id_entry.get()
                acc_type = self.acc_type.get()
                first_depo = float(self.first_depo.get())

                if not all([Fname, PiD, acc_type]):
                    self.status_show("Enter all details", "red")
                    return False

                print(f"[DEBUG] Data: {Fname}, {PiD}, {acc_type}, {first_depo}")

            
                owner = Owner(Fname, PiD)
                acc_num = self.bank.create_account(owner, acc_type, first_depo)

                print(f"[DEBUG] Account created: {acc_num}")

                self.root.after(0, lambda: [
                    self.status_show(f"Successfully created account {acc_num}","green"),
                    self.clearForm()
                ])

            except accountexistserror:
                self.root.after(0, lambda: [self.status_show("Account exists")])
            except createAccountError as e:
                self.root.after(0, lambda:[self.status_show("Error!!")])
                self.bank.log_error(f"Unexpected: {e}")
            except Exception as e:
                print(f"[ERROR] {str(e)}")
                self.root.after(0, lambda: [self.status_show(f"try again {str(e)}", "red")])
            finally:
                self.root.after(0, lambda: self.submit_button.config(state=tk.NORMAL))
        threading.Thread(target=db_task, daemon=True).start()
        print(f"[Thread Info] Active threads: {threading.active_count()}")

    def status_show(self, message, color):
        self.status_bar.config(text=message, foreground=color)

    def clearForm(self):
        self.name_entry.delete(0, 'end')
        self.id_entry.delete(0, 'end')
        self.acc_type.set('')
        self.first_depo.delete(0, 'end')
        self.form.after(3000, lambda: self.status_bar.config(text=""))

    def goback(self):
        self.root.destroy()
        from gui.mgui import MainPage
        MainPage()