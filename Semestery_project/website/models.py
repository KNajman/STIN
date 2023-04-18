import random # for generating random account numbers

# bank user model class (name, password, account)
class user(self):
    """User model
    name : str
    password : str
    accounts : list of accounts
    """
    name : str
    email : str
    PIN : str
    account : account
    
    # account model
    def __init__(self, name, password, account):
        self.name = name
        self.password = password
        self.account = account
        
    # class method to create a new user
    @classmethod
    def create_user(cls, name, password):
        user = cls(name, password)
        return user
    
    # class method to create a new account
    @classmethod
    def create_account(cls, account_number, balance, currency):
        account = cls(account_number, balance, currency)
        return account
        
    
# account model class
def account(self):
    """Account model
    account_number : int
    balance : float
    currency : str
    """
    account_number = self.account_number
    balance = self.balance
    currency = list(self.currency)
    
    # class method to create a new account
    @classmethod
    def create_account(cls, account_number, balance, currency):
        account = cls(account_number, balance, currency)
        return account
    
    # class method to deposit money
    @classmethod
    def deposit(self, amount):
        balance += amount
        return balance

    # class method to withdraw money, if balance is less than amount, return error
    @classmethod
    def withdraw(cls, amount):
        if balance < amount:
            return "Insufficient funds"
        else:
            balance -= amount
            return balance
        
    # class method to transfer money, if balance is less than amount, return error
    def transfer(cls, amount, account):
        if balance < amount:
            return "Insufficient funds"
        else:
            balance -= amount
            account.balance += amount
            return balance, account.balance

    # class method to return balance
    def return_balance(self):
        return balance
    
    # class method to pay bills
    def pay_bills(self, amount):
        if balance < amount:
            return "Insufficient funds"
        else:
            balance -= amount
            return balance
    
# generate random account number for new account (8 digits) starting with 123
def generate_account_number():
    return random.randint(123000000, 123999999)