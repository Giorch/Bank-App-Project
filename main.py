# BankApp: Single Flow Console Application
# Main -> Welcome Message -> Authenthication/Autoriozation(login)
# 2 stakeholders: Admin, Customer
# 2 dashboard/menus: AdminMenu, CustomerMenu
# Operations: CRUD(Add Customer, Delete, Update, Add Account, View All Accounts
# Programming and OOD concepts
# Loops and single flow
from getpass import getpass
from abc import ABC, abstractmethod
import math
import sys
import os


class User:
    def __init__(self, username, pw):
        self.username: str = username
        self.pw: str = pw

class Customer(User):
    def __init__(self, id, username, pw, firstName, lastName, accounts):
        super().__init__(username, pw)
        self.__id = id
        self.__firstName = firstName
        self.__lastName = lastName
        self.__accounts: list[Account] = accounts
    def getId(self):
        return self.__id
    def setId(self, id):
        self.__id = id
    def getFirstName(self):
        return self.__firstName
    def setFirstName(self, firstName):
        self.__firstName = firstName
    def getLastName(self):
        return self.__lastName
    def setLastName(self, lastName):
        self.__lastName = lastName
    
    def getAccounts(self):
        return self.__accounts
    def setAccounts(self, accounts):
        self.__accounts = accounts


class Admin(User):
    def __init__(self, id, username, pw):
        self.username = "admin"
        self.pw = "admin123" 
        super().__init__(username, pw)
        self.id: str = id

class ITransaction(ABC):
    def printReceipt(self):
        pass
class Account(ITransaction):
    def __init__(self, id):
        self.__id = id
        self.__balance = 0.0
    
    @abstractmethod
    def AddInterest(self):
        pass
    def GetId(self):
        return self.__id
    def GetBalance(self):
        return self.__balance
    def Deposit(self, amount):
        self.__balance += amount
    def Withdraw(self, amount):
        self.__balance -= amount
    
        

class CheckinsAccount(Account):
    def __init__(self, id):
        self.accountType = "CheckingsAccount"
        super().__init__(id)
    def AddInterest(self):
        super().__balance *= 1.05


class SavingsAccount(Account):
    def __init__(self, id):
        self.accountType = "SavingsAccount"
        super().__init__(id)
    def AddInterest(self):
        super().__balance *= 1.02
    


class Main:

    @staticmethod
    def _CreateAccount(user: Customer):
        while True:
            os.system('cls')
            accType = input("1). Checking\n2). Savings\n3). Go Back\nSelect account type\n")
            match accType:
                case "1":
                    balance = int(input("Initial Balance: "))
                    acc = CheckinsAccount(str(user.getId() + len(user.getAccounts())))
                    acc.Deposit(balance)
                    user.getAccounts().append(acc)
                case "2":
                    balance = int(input("Initial Balance: "))
                    acc = SavingsAccount(str(user.getId() + len(user.getAccounts())))
                    acc.Deposit(balance)
                    user.getAccounts().append(acc)
                case "3":
                    return
            
    @staticmethod
    def _welcome():
        print("Welcome to ModernBank Solutions")

    @staticmethod
    def _login():
        user = input("Enter username: ")
        pw = getpass("Enter password: ")
        if user == "admin" and pw == "admin123":
            return "admin"
        
        for u in users:
            if user == u.username and pw == u.pw:
                return u.username
        
        return "Login Failed"
    
    @staticmethod
    def _CustomerDashboard(user :Customer):
        while True:
            os.system('cls')
            print(f"Welcome {user.username}")
            print("1) Create Account")
            print("2) View All Accounts")
            print("3) Deposit")
            print("4) Withdraw")
            print("5) Transfer")
            print("6) Close Account")
            print("7) Exit")
            option = input("Select an option: ")
            match option:
                case "1":
                    Main._CreateAccount(user)
                case "2":
                    for a in user.getAccounts():
                        print("Account ID: " + a.GetId())
                        print(f"Account Balance: {a.GetBalance()}\n")
                    input()
                case "3":
                    for a in user.getAccounts():
                        print(f"- {a.GetId()}")
                    account_id = input("Select Account: ")
                    acc = next((a for a in user.getAccounts() if a.GetId() == account_id), None)

                    
                case "4":
                    print("Withdraw Selected")
                case "5":
                    print("Transfer Selected")
                case "6":
                    print("Close Account Selected")
                case "7":
                    break




    @staticmethod
    def _AdminDashboard():
        print("Welcome Admin")
        while True:
            os.system('cls')
            print(f"Welcome Admin")
            print("1) Create Account")
            print("2) View All Accounts")
            print("3) Deposit")
            print("4) Withdraw")
            print("5) Transfer")
            print("6) Close Account")
            print("7) Exit")
            option = input("Select an option: ")
            match(option):
                case "1":
                    print("Create Account Selected")
                case "2":
                    print("View All Account Selected")
                case "3":
                    print("Deposit Selected")
                case "4":
                    print("Withdraw Selected")
                case "5":
                    print("Transfer Selected")
                case "6":
                    print("Close Account Selected")
                case "7":
                    break

if __name__ == "__main__":
    counter = 145
    loggedUser = ""
    u1 = User("Jorge", "jorge123")
    u2 = User("David", "david123")
    u3 = User("William", "william123")
    users = [u1, u2, u3]
    c1 = Customer(counter, u1.username, u1.pw, "Jorge", "Mejia", [])
    counter = 784
    c2 = Customer(counter, u2.username, u2.pw, "David", "Smith", [])
    counter = 251
    c3 = Customer(counter, u3.username, u3.pw, "William", "Benedict", [])
    customers = [c1, c2, c3]
    ad = Admin(78, "admin", "admin123")
    Main._welcome()
    validation = Main._login()
    while validation == "Login Failed":
        print("Login Failed")
        validation = Main._login()
    
    if validation == "admin":
            loggedUser = ad
            Main._AdminDashboard()
    else:
            loggedUser = next(c for c in customers if c.username == validation)
            Main._CustomerDashboard(loggedUser)
    

    
        