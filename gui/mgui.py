from core import ttk,tk
from .create import AccountFormHandler
from .withdr import WithdrawFormHandler

class MainPage:
    def __init__(self):
        self.root =tk.Tk()
        self.root.title("Bankbank")
        self.setInterface()

    def setInterface(self):

        frm = ttk.Frame(self.root, padding=20)
        frm.grid()
        
        self.main_select = tk.StringVar()
        ttk.Label(frm, text="Welcome to bankbank!!What would you like to do today").grid(column=0, row=1)
        ttk.Radiobutton(frm, variable=self.main_select, value="Create account", text="Create account").grid(column=0, row=2)
        ttk.Radiobutton(frm, variable=self.main_select, value="Withdraw", text="Withdraw").grid(column=0, row=3)


        ttk.Button(text="Confirm", command=self.go_next).grid(column=0, row=5)
        
    
    def go_next(self):
        choice = self.main_select.get()
        self.root.destroy()

        if choice == "Create account":
            AccountFormHandler()
        elif choice == "Withdraw":
            WithdrawFormHandler()
        else:
            MainPage()

if __name__ == "__main__":
    main = MainPage()
    main.root.mainloop()