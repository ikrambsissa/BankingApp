from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json


def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry("+{}+{}".format(x, y))


class BankingApp:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.title('Banking App')
        self.accounts = []
        self.fenetre.geometry("500x300")
        
        center_window(self.fenetre)

        with open("login_info.json", "r") as file:
            data = json.load(file)
            if "accounts" in data and len(data["accounts"]) > 0:
                self.accounts = data["accounts"]
                self.selected_account = self.accounts[0]  # Sélectionner le premier compte

        self.create_widgets()

    def create_widgets(self):
        self.fenetre.geometry("300x300")
        self.fenetre.configure(bg='#FDFEFE')

        img = Image.open('bnk.jpg')
        img = img.resize((150, 150))
        self.img_tk = ImageTk.PhotoImage(img)

        Label(self.fenetre, text="Welcome to SIA BANK", font=("Calibri", 14), bg='#FDFEFE').pack(pady=10)
        Label(self.fenetre, image=self.img_tk, bg='#FDFEFE').pack(pady=15)

        login_button = Button(self.fenetre, text="Log In", font=("Calibri", 12), width=20, command=self.authenticate, bg='#3498DB', fg='#FDFEFE')
        login_button.pack(pady=10)

    def finish_reg(self):
        messagebox.showinfo("Registration", "Registration completed.")

    def register(self):
        register_screen = Toplevel(self.fenetre)
        register_screen.title('Register')
        center_window(register_screen)

        Label(register_screen, text="Please enter your details below to register", font=("Calibri", 12)).grid(row=0, sticky=N, pady=10)
        Label(register_screen, text="Name", font=("Calibri", 12)).grid(row=1, sticky=W)
        Label(register_screen, text="Age", font=("Calibri", 12)).grid(row=2, sticky=W)
        Label(register_screen, text="Gender", font=("Calibri", 12)).grid(row=3, sticky=W)
        Label(register_screen, text="Password", font=("Calibri", 12)).grid(row=4, sticky=W)

        temp_name = StringVar()
        temp_age = StringVar()
        temp_gender = StringVar()
        temp_password = StringVar()

        Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)
        Entry(register_screen, textvariable=temp_age).grid(row=2, column=0)
        Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0)
        Entry(register_screen, textvariable=temp_password, show="*").grid(row=4, column=0)

        Button(register_screen, text="Register", command=self.finish_reg, font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)

    def authenticate(self):
        login_screen = Toplevel(self.fenetre)
        login_screen.title('Log In')
        center_window(login_screen)

        Label(login_screen, text="Username:", font=("Calibri", 12)).grid(row=0, sticky=W)
        Label(login_screen, text="Password:", font=("Calibri", 12)).grid(row=1, sticky=W)

        username_entry = Entry(login_screen, font=("Calibri", 12))
        username_entry.grid(row=0, column=1)
        password_entry = Entry(login_screen, show="*", font=("Calibri", 12))
        password_entry.grid(row=1, column=1)

        Button(login_screen, text="Log In", command=lambda: self.check_authentication(username_entry, password_entry), font=("Calibri", 12), bg='#3498DB', fg='#FDFEFE').grid(row=2, columnspan=2, pady=10)

    def check_authentication(self, username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        with open("login_info.json", "r") as file:
            data = json.load(file)

        if "accounts" in data:
            authenticated = False
            for account in data["accounts"]:
                if account["username"] == username and account["password"] == password:
                    authenticated = True
                    break

            if authenticated:
                messagebox.showinfo("Authentication", "Authentication successful")
                self.selected_account = account  # Mettre à jour le compte sélectionné
                self.balance = account["balance"]  # Assigner le solde du compte à self.balance
                self.show_operations_window()
            else:
                messagebox.showerror("Authentication", "Authentication failed")
        else:
            messagebox.showerror("Authentication", "Invalid login_info.json file")

    def show_operations_window(self):
        operations_screen = Toplevel(self.fenetre)
        operations_screen.title('Banking Operations')
        operations_screen.geometry("350x220")
        operations_screen.configure(bg='#FDFEFE')
        center_window(operations_screen)

        Button(operations_screen, text="Withdraw Money", command=self.withdraw_money, font=("Calibri", 12), bg='#3498DB', fg='#FDFEFE', width=20).grid(row=0, pady=10, padx=10)
        Button(operations_screen, text="Deposit Money", command=self.deposit_money, font=("Calibri", 12), bg='#3498DB', fg='#FDFEFE', width=20).grid(row=1, pady=10, padx=10)
        Button(operations_screen, text="Check Balance", command=self.check_balance, font=("Calibri", 12), bg='#3498DB', fg='#FDFEFE', width=20).grid(row=2, pady=10, padx=10)
        Button(operations_screen, text="User Info", command=self.show_user_info, font=("Calibri", 12), bg='#3498DB', fg='#FDFEFE', width=20).grid(row=3, pady=10, padx=10)

    def withdraw_money(self):
        # messagebox.showinfo("Withdraw Money", "Performing withdrawal operation...")
        withdraw_screen = Toplevel(self.fenetre)
        withdraw_screen.title("Withdraw")
        withdraw_screen.geometry("300x300")
        withdraw_screen.configure(bg='#FDFEFE')
        center_window(withdraw_screen)

        title = Label(withdraw_screen, text="Withdraw Money", font=("Calibri", 20, "bold"), bg='#FDFEFE')
        title.place(x=20, y=60)
        self.amount = Entry(withdraw_screen, width=30)
        self.amount.place(x=20, y=100)
        btn = Button(withdraw_screen, text="Withdraw", padx=15, pady=6, command=self.withdraw, bg='#3498DB', fg='#FDFEFE')
        btn.place(x=20, y=130)

        withdraw_screen.mainloop()

    def withdraw(self):
        amount = float(self.amount.get())  # Récupérer le montant saisi dans l'Entry "amount"
        if amount <= 0:
            messagebox.showerror("Error", "Invalid amount. Please enter a positive value.")
        elif amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            current_balance = self.balance
            new_balance = current_balance - amount
            self.balance = new_balance  # Mettre à jour le solde dans l'objet BankingApp
            # Enregistrer les modifications dans le fichier ou dans une base de données si nécessaire

            # Afficher le nouveau solde dans le message d'information
            messagebox.showinfo("Withdraw Money", f"Withdrawal successful. New balance: {new_balance}")

            # Mettre à jour le fichier login_info.json avec le nouveau solde
            with open("login_info.json", "r") as file:
                data = json.load(file)

            if "accounts" in data:
                for account in data["accounts"]:
                    if account["username"] == self.selected_account["username"]:
                        account["balance"] = new_balance
                        break

            with open("login_info.json", "w") as file:
                json.dump(data, file)

    # def deposit_money(self):
    #     messagebox.showinfo("Deposit Money", "Performing deposit operation...")


    def deposit_money(self):
        deposit_screen = Toplevel(self.fenetre)
        deposit_screen.title("Deposit")
        deposit_screen.geometry("300x300")
        deposit_screen.configure(bg='#FDFEFE')
        center_window(deposit_screen)

        title = Label(deposit_screen, text="Deposit Money", font=("Calibri", 20, "bold"), bg='#FDFEFE')
        title.place(x=20, y=60)
        self.amount = Entry(deposit_screen, width=30)
        self.amount.place(x=20, y=100)
        btn = Button(deposit_screen, text="Deposit", padx=15, pady=6, command=self.deposit, bg='#3498DB', fg='#FDFEFE')
        btn.place(x=20, y=130)

        deposit_screen.mainloop()

    def deposit(self):
        amount = float(self.amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Invalid amount. Please enter a positive value.")
        else:
            current_balance = self.balance
            new_balance = current_balance + amount
            self.balance = new_balance

            messagebox.showinfo("Deposit Money", f"Deposit successful. New balance: {new_balance}")

            with open("login_info.json", "r") as file:
                data = json.load(file)

            if "accounts" in data:
                for account in data["accounts"]:
                    if account["username"] == self.selected_account["username"]:
                        account["balance"] = new_balance
                        break

            with open("login_info.json", "w") as file:
                json.dump(data, file)

    def check_balance(self):
        messagebox.showinfo("check_balance", f"\nBalance: {self.selected_account['balance']}")

    def show_user_info(self):
     messagebox.showinfo("User Info", f"Username: {self.selected_account['username']}\nPassword: {self.selected_account['password']}\nBalance: {self.selected_account['balance']}")

     self.fenetre.mainloop()
     
     

    def run(self):
        self.fenetre.mainloop()


if __name__ == '__main__':
        app = BankingApp()
        app.run()
