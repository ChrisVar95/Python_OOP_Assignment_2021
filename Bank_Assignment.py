####################
# Author : Christina Vargka
# Date Reviewed : 18/12/2021
# Program that simulates an ATM machine where Customers can view and manage their accounts.
# Classes : Bank -> Customer -> Account == CheckingAccount/SavingAccount
# Menu Functions : ATM(), Account_Choice(), Menu()
####################

# https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
import ast  # allows to convert lines of text files into dictionaries.
# https://www.geeksforgeeks.org/comparing-dates-python/
# https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
from datetime import *  # allows to control duration between transactions in a Savings Account
# https://realpython.com/python-sleep/
import time  # Pauses the Menus so that user may read output more conveniently


class Bank(object):
    def __init__(self, bank_name: "str" = "PermanentTSD", bank_address: "str" = "123 Main Street, Dublin",
                 country: "str" = "Ireland", interest_rate: "float" = 0.05):
        """initialise the bank class"""
        self.__bank_name = bank_name
        self.__bank_address = bank_address
        self.__country = country
        self.__interest_rate = interest_rate

    def getBankName(self):
        """Returns Bank Name"""
        return self.__bank_name

    def get_bank_address(self):
        """Returns Bank Address"""
        return self.__bank_address

    def get_country(self):
        """Returns Country"""
        return self.__country

    def get_yearly_interest_rate(self):
        """Returns yearly interest"""
        return self.__interest_rate

    def get_monthly_interest_rate(self):
        """Returns monthly interest"""
        return self.__interest_rate / 12

    def __str__(self):
        """Prints out Bank class details"""
        returned = "\n" + self.getBankName() + ","
        returned += "\n" + self.get_bank_address()
        returned += "\n" + self.get_country()
        return returned


class Customer(object):
    """Customer Object. Holds basic information about Customers including age."""

    def __init__(self, bank: Bank = Bank(), customer_id: "str" = "0000", name: "str" = "None", address: "str" = "None",
                 Age: "int" = 0):
        """Initializes values for Customer class objects"""
        # aggregating Bank object
        self.object_bank = bank

        self.__customer_id = customer_id
        self.__name = name
        self.address = address
        self.Age = Age

    def get_customer_id(self):
        """Returns Customer ID"""
        return self.__customer_id

    def get_name(self):
        """Returns Customer Name"""
        return self.__name

    def __str__(self):
        """Prints out all information about the customer"""
        returned = "\nPIN : " + str(self.get_customer_id())
        returned += "\nName : " + str(self.get_name())
        returned += "\nAddress : " + str(self.address)
        returned += "\nAge : " + str(self.Age)
        return returned


class Account(object):
    """Account object that holds most account functions"""

    # Construct an Account object
    def __init__(self, customer: Customer = Customer(), acc_ID: "str" = "0000", balance: "float" = 10.0):
        """Initializes values for Account class objects"""
        # Aggregating Customer object.
        self.object_customer = customer

        self.acc_ID = acc_ID
        self.__balance = balance

    def get_balance(self):
        """Returns the account balance"""
        return self.__balance

    def deposit(self, amount: "float"):
        """Deposits amount into account balance"""
        self.__balance += amount
        self.update_balance_in_txt()

    def transfer(self, account, amount: "float"):
        """Transfers amount into another account balance"""
        self.withdraw(amount)
        account.deposit(amount)

    def withdraw(self, amount: "float"):
        """Withdraws amount from account balance"""
        self.__balance -= amount
        self.update_balance_in_txt()

    def record_Transaction(self, num: "float", method: "str"):
        """Records Transactions"""
        count = 1
        myList = openfile("accountTransactions.txt")
        tim = date.today()  # today's date
        trans_id = str(self.acc_ID) + method + str(tim) + "_" + str(count)
        while [i for i in myList if i["TransID"] == trans_id]:  # creates unique ID
            count += 1
            # changes trans_id so there are no infinite loops
            trans_id = str(self.acc_ID) + method + str(tim) + "_" + str(count)
        dic = {
            "Customer": str(self.object_customer.get_customer_id()),
            "AccID": str(self.acc_ID),
            "TransID": trans_id,
            "Balance": self.get_balance(),
            "TransTime": str(tim),
            "Amount": num
        }
        myList.append(dic)  # adds record to the list
        writefile("accountTransactions.txt", myList)

    def update_balance_in_txt(self):
        """Updates accounts.txt file with the new balance"""
        myList = openfile("accounts.txt")
        acid = self.acc_ID
        # filters search
        found_value = search_dic_list(myList, "AccID", acid)

        # removes redundant item
        myList.remove(found_value[0])
        # turns item into dictionary
        found_value = ast.literal_eval(str(found_value[0]))
        # changes value of balance
        found_value["Balance"] = self.get_balance()
        myList.append(found_value)
        writefile("accounts.txt", myList)

    def __add__(self, other) -> "float":
        """adds the balance between two accounts (if exists)
        is not intended for any other use"""
        try:
            return self.get_balance() + other.get_balance()
        except AttributeError:
            return self.get_balance()

    def __radd__(self, other):
        """Works with __add__"""
        return self.__add__(other)

    def __str__(self):
        """Prints out User Friendly account information"""
        returned = str(self.object_customer.get_name()) + "\n"
        returned += str(self.object_customer.object_bank.getBankName())
        returned += "\nAccount ID is " + str(self.acc_ID)
        return returned


class SavingAccount(Account):
    """Savings account. One withdrawal/month. Age 14+"""

    def __init__(self, customer: Customer = Customer(), acc_ID: "str" = "0000", balance: "float" = 0.0):
        """Initialises Inherited values"""
        super().__init__(customer, acc_ID, balance)

    def get_monthly_interest(self):
        """Returns monthly interest on Savings account"""
        return self.get_balance() * self.object_customer.object_bank.get_monthly_interest_rate()

    def check_amount(self, amount: "float") -> "bool":
        """Checks if amount can be withdrawn"""
        if amount > self.get_balance():
            return False
        else:
            return True

    def write_and_withdraw_amount(self, amount: "float"):
        """Checks if amount can be withdrawn then saves the transaction to file"""
        if not self.check_amount(amount):
            print("\nSorry you cant withdraw amount : " + str(amount))
            print("\nYour account balance is : " + str(self.get_balance()))
        else:
            self.withdraw(amount)
            self.record_Transaction(amount, "_WD_")

    def okToWithdraw(self) -> "bool":
        """Filters list of dictionaries.
        Filters types of Transactions
        Compares two dates then gives the ok"""
        # reads lines of dictionaries and appends the to a list
        myList = openfile("accountTransactions.txt")
        # today's date
        tim = str(date.today())
        # filters through the file so that only transactions
        # from the same account are forwarded
        found_list = search_dic_list(myList, "AccID", self.acc_ID)
        found = False
        try:
            for i in found_list:
                tid = str(i["TransID"])
                x = tid.split("_")
                if "WD" in x:  # Withdrawal found
                    found = True
                if found:
                    dic = i
                    # compared dates
                    if days_between(tim, str(dic["TransTime"])) >= 30:
                        return True
                    return False
        except TypeError:  # nothing was found
            pass
        return True

    def __str__(self):
        """Prints out Savings Account information"""
        returned = "\nSavings account: " + super().__str__()
        returned += self.object_customer.__str__()
        returned += "\nBalance is " + str(self.get_balance())
        returned += "\nInterest on balance is\t" + str("{:.2f}".format(self.get_monthly_interest()))
        return returned


class CheckingAccount(Account):
    """Regular account. Can have negative balance until a specified amount. Age 18+"""

    def __init__(self, customer: Customer = Customer(), acc_ID: "str" = "", balance: "float" = 0.0, credit_limit=-5000):
        """Initializes values for Checking Account"""
        super().__init__(customer, acc_ID, balance)
        self.__credit_limit = credit_limit

    def get_credit_limit(self):
        """Returns credit limit set by the bank"""
        return self.__credit_limit

    def check_amount(self, amount: "float"):
        """Checks if amount can be withdrawn"""
        if (float(self.get_balance()) - amount) < float(self.get_credit_limit()):
            return False
        else:
            return True

    def write_and_withdraw_amount(self, amount: "float"):
        """Checks if amount can be withdrawn then saves the transaction to file"""
        if not self.check_amount(amount):
            print("\nSorry you cant withdraw amount : " + str(amount) + "\nYour account balance is : " +
                  str(self.get_balance()) + "\nCredit limit is : " + str(self.get_credit_limit()))
        else:
            self.withdraw(amount)
            self.record_Transaction(amount, "_WD_")

    def __str__(self):
        """Prints out values for Checking Account"""
        returned = "\nChecking account: " + super().__str__()
        returned += self.object_customer.__str__()
        returned += "\nBalance is " + str(self.get_balance())
        returned += "\nCredit limit is " + str(-(self.get_credit_limit()))
        return returned


def Number_Verification(num: "str") -> "float" or None:
    """Verifies that numeric input positive numbers. Returns None if string or if negative"""
    try:
        num = float(num)
        if num < 0:  # checks to see if value is positive
            return None
        return num
    except ValueError:  # will run if num = float(num) fails
        return None


def openfile(filename: "str") -> "list":
    """Opens a text file containing lines of dictionaries
    It then appends the lines of that file to a list.
    This will create a list of dictionaries
    Returns a list"""
    myList = []
    try:
        file = open(filename, "r")
        data = file.readlines()  # data is a list of strings
        for line in data:  # for each string in data
            dic = ast.literal_eval(line)  # dictionaries from the strings
            myList.append(dic)  # are added to my empty list
        file.close()
    except FileNotFoundError:
        file = open(filename, "a")
        file.close()
    return myList


def writefile(filename: "str", DicList: "list") -> None:
    """Opens a text file and overwrites content with the new List
    No returned value"""
    # Open the file in write mode ('w')
    with open(filename, "w") as file:
        for line in DicList:
            file.write(str(line) + "\n")  # makes sure they are on separate lines
    file.close()


def search_dic_list(myList: "list", key: "str", item: "str") -> "list" or None:
    """Searches a list of dictionaries by its key for a certain value
    returns the found value as a list
    None is it doesnt exist"""
    found_value = []
    found = False
    for dictionary in myList:
        if dictionary[key] == item:
            found_value.append(dictionary)
            found = True
    if found:
        return found_value
    return None


def days_between(date_1: "str", date_2: "str"):
    """Calculates days between two compatible strings"""
    date_1 = datetime.strptime(date_1, "%Y-%m-%d")
    date_2 = datetime.strptime(date_2, "%Y-%m-%d")
    return abs((date_2 - date_1).days)


def enter_customer_details() -> "dict" or None:
    """Returns a dictionary with the customer's details"""
    try:
        age = int(input("Please enter your age : "))
    except ValueError:
        return None
    if age < 14:  # min required age to open a savings account.
        print("Sorry, you need to be at least 14 years old to open an account.")
        exit()
    var = input("Please enter a 4 digit PIN code : ")
    while len(var) != 4:
        print("OOPS!\nYou entered a " + str(len(var)) + " digit PIN code.\n")
        var = input("Please enter a 4 PIN code : ")
    name = input("Please enter your name : ")
    address = input("Please enter your home address : ")
    user = {
        'ID': var,
        'Name': name,
        'Address': address,
        'Age': age
    }
    return user


def login() -> Customer or None:
    """login function that identifies existing customers
    customer details are saved in the customers.txt file
    returns a Customer class
    returns None if failed"""
    myList = openfile("customers.txt")
    username = input("Please enter your username : ")
    found_value = search_dic_list(myList, "ID", username)
    try:
        user_dic = found_value[0]
    except TypeError:
        return None
    val = Customer(Bank(), user_dic["ID"], user_dic["Name"], user_dic["Address"], user_dic["Age"])
    return val  # :Customer returned to acc: Customer in ATM()


def sign_up() -> None:
    """Writes new customer to the txt file"""
    myList = openfile("customers.txt")
    new_user = enter_customer_details()
    if new_user is None:
        print("Sign up failed!!")
        return None
    if search_dic_list(myList, "ID", new_user["ID"]) is None:
        myList.append(new_user)
        writefile("customers.txt", myList)
        print("\nThank you for signing up with us.\n")
    else:
        print("OOPS!\nThis username already exists!\nPlease try again.")


def ATM() -> None:
    """Interface for customers who wish to use the Banking System"""
    while True:
        acc = Customer()
        menu = "*********************\n"
        menu += "Welcome to " + str(acc.object_bank.getBankName()) + "\n"
        menu += "0. Exit\n"
        menu += "1. Sign in\n"
        menu += "2. Sign up\n"
        menu += "*********************\n"
        print(menu)

        # Customer prompt
        option = input("Selection : ")
        option = Number_Verification(option)

        # case 1 : Sign in
        if option == 1:
            acc = login()
            if acc is None:
                print("OOPS!\nUsername doesn't exist")
            else:
                print("Successful Login")
                Account_Choice(acc)

        # case 2 : Sign up
        elif option == 2:
            sign_up()

        # case 3 : Exit
        elif option == 0:
            print("Goodbye")
            exit()

        # case : bad input
        else:
            print("OOPS!\nThat is not a valid option.")
        time.sleep(1)


def create_acc(acc: Customer, method: "str") -> CheckingAccount or SavingAccount or None:
    """Writes a new Account Dict into the accounts.txt file
    Creates appropriate account type"""
    answer = input("You do not have any accounts of this type.\nOpen new account? (y/n) : ")
    new_acc = None  # returning value
    if answer == 'y' or answer == 'Y':
        myList = openfile("accounts.txt")
        acc_id = str(acc.get_customer_id()) + "_" + method
        dic = {
            "Bank": str(acc.object_bank.getBankName()),
            "AccID": acc_id,
            "Customer ID": str(acc.get_customer_id()),
            "Balance": 0.0,
            "Name": str(acc.get_name()),
            "Age": acc.Age,
            "Address": acc.address
        }
        myList.append(dic)
        writefile("accounts.txt", myList)
        if method == "Check":
            new_acc = CheckingAccount(acc, dic["AccID"], dic["Balance"])
        elif method == "Sav":
            new_acc = SavingAccount(acc, dic["AccID"], dic["Balance"])
    return new_acc


def search_acc(acc: Customer, method: "str"):
    """Checks if Customer has specified account type
    If yes, it loads the account into the program"""
    myList = openfile("accounts.txt")
    sav_acid = str(acc.get_customer_id()) + "_" + method
    found = search_dic_list(myList, "AccID", sav_acid)
    new_acc = None
    if not found:
        pass
    else:
        dic = found[0]
        if method == "Check":
            new_acc = CheckingAccount(acc, dic["AccID"], dic["Balance"])
        elif method == "Sav":
            new_acc = SavingAccount(acc, dic["AccID"], dic["Balance"])
    return new_acc


def Account_Choice(acc: Customer) -> None:
    """Branches choices off by their account type"""
    adult = False
    if acc.Age >= 18:
        adult = True
    check = search_acc(acc, "Check")  # Loads checking account
    sav = search_acc(acc, "Sav")  # Loads saving account
    while True:
        menu_choice = "*********************\n"
        menu_choice += "0. Exit\n"
        menu_choice += "1. View Accounts\n"
        menu_choice += "2. Savings account\n"
        if adult:
            menu_choice += "3. Checking account\n"
        menu_choice += "9. Sign out\n"
        menu_choice += "*********************\n"
        print(menu_choice)

        # Customer prompt
        choice = input("Selection: ")
        choice = Number_Verification(choice)

        # case 9: Log out
        if choice == 9:
            print("Signing out...")
            ATM()

        # case 0 : Exit
        elif choice == 0:
            print("Goodbye")
            exit()

        # case 1 : View Accounts
        elif choice == 1:
            try:
                if sav:
                    print(sav)
                if check:
                    print(check)
                print("\nTotal balance between accounts: " + str(check + sav))
            except TypeError:
                print("You do not have any accounts")

        # case 2 : Savings Account
        elif choice == 2:
            if not sav:
                sav = create_acc(acc, "Sav")  # Saving account option
            if sav:
                Menu(sav, check)

        # case 3 : Checking Account
        elif choice == 3 and adult:
            if not check:  # Checking account option
                check = create_acc(acc, "Check")
            if check:
                Menu(check, sav)

        # case : bad input
        else:
            print("Oops! That is not a valid option.")


def Menu(acc, other):
    """Main menu for the customer.
    Allows access to all Account related functions"""
    # customer signed in
    while True:
        menu_choice = "*********************\n"
        menu_choice += "0. Exit\n"
        menu_choice += "1. View Balance\n"
        menu_choice += "2. Withdraw\n"
        menu_choice += "3. Deposit\n"
        menu_choice += "4. Transfers & Payments\n"
        menu_choice += "5. View Interest\n"
        menu_choice += "6. Transaction History\n"
        menu_choice += "7. Delete Account\n"
        menu_choice += "8. Choose Account\n"
        menu_choice += "9. Sign out\n"
        menu_choice += "*********************\n"
        print(menu_choice)

        # Customer prompt
        choice = input("Selection: ")
        choice = Number_Verification(choice)

        # case 0: Exit
        if choice == 0:
            print("Goodbye")
            exit()

        # case 1: View balance
        elif choice == 1:
            print("Balance : " + str(acc.get_balance()))

        # case 2: Withdrawal
        elif choice == 2:
            case_2_withdrawal(acc)

        # case 3: Deposit
        elif choice == 3:
            case_3_deposit(acc)

        # case 4: Transfers and Payments
        elif choice == 4:
            case_4_Transfer(acc)

        # case 5: View interest
        elif choice == 5:
            case_5_viewInterest(acc)

        # case 6: Transaction History
        elif choice == 6:
            case_6_transactionHistory(acc)

        # case 7: Delete account
        elif choice == 7:
            case_7_deleteAccount(acc, other)

        # case 8: Choose Account
        elif choice == 8:
            Account_Choice(acc.object_customer)

        # case 9: Log out
        elif choice == 9:
            print("Signing out...")
            ATM()

        # case : bad input
        else:
            print("Oops! That is not a valid option.")
        time.sleep(2)


def transfer_acc(acc):
    """Creates a temporary Account class type for transactional purposes"""
    accList = openfile("accounts.txt")
    key = "AccID"
    found = search_dic_list(accList, key, acc)
    if found:
        dic = found[0]
        transfer = Account(dic["Customer ID"], dic["AccID"], dic["Balance"])
        return transfer
    return None


def amount_verification() -> "float":
    """Filters out bad input for money amounts and returns that value"""
    amount = None
    while not amount:
        amount = input()
        amount = Number_Verification(amount)
        if not amount:
            print("Sorry, that is not a valid number, try again : ")
    return amount


def case_2_withdrawal(acc) -> None:
    """Checks amount and allows user to withdraw amount
    SavingAccount Users can only withdraw once a month"""
    if type(acc) == SavingAccount:
        ok = acc.okToWithdraw()
        if not ok:
            print("\nSorry, you can't withdraw from this account at the moment.\n")
            return None
    print("\nPlease enter amount to be withdrawn : ")
    amount = amount_verification()
    acc.write_and_withdraw_amount(amount)
    print("You withdrew : " + str(amount))
    return None


def case_3_deposit(acc) -> None:
    """Function that allows user to deposit amount into account"""
    print("\nPlease enter amount to be deposited : ")
    amount = amount_verification()
    acc.deposit(amount)
    acc.record_Transaction(amount, "_Dep_")
    print("Deposited amount : " + str(amount))
    return None


def case_4_Transfer(acc) -> None:
    """Function that enables the safe transfer of funds"""
    if type(acc) == SavingAccount:  # Saves time for User
        # checks when last withdrawal was
        ok = acc.okToWithdraw()
        if not ok:
            print("Sorry, its not possible from this account at the moment")
            return None
        if acc.get_balance() == 0:
            print("Sorry your balance is " + str(acc.get_balance()))
            return None
    # prompt for foreign acc_ID
    foreign_acc = input("Which account to send money to? : ")
    if foreign_acc == acc.acc_ID:
        print("You entered your own bank details.")
        return None
    acc2 = transfer_acc(foreign_acc)  # returns an Account class.
    if acc2:  # if acc2 was found and is not None
        print("Please specify amount to be transferred")
        amount = amount_verification()

        # checks if possible to withdraw that amount
        T = acc.check_amount(amount)
        if T:
            acc.transfer(acc2, amount)
            method = "_trans_from_" + str(acc.acc_ID) + "_"
            acc2.record_Transaction(amount, method)
            print("Funds transferred successfully.")
        else:
            print("Sorry, you cant do that.")
            print(acc)
    else:
        print("Sorry, entered Account ID not in database")
    return None


def case_5_viewInterest(acc) -> None:
    """Saving Accounts Customers may view the interest rates"""
    result = "\nInterest Rate of the Bank: " + str(
        int(acc.object_customer.object_bank.get_yearly_interest_rate() * 100)) + "%"
    if type(acc) == SavingAccount:
        result += "\nAccount's Monthly Interest: " + str("{:.2f}".format(acc.get_monthly_interest()))
    else:
        result += "\nThis account doesn't have a monthly interest"
    print(result)
    return None


def case_6_transactionHistory(acc) -> None:
    """Shows their own Transaction History to the account holder"""
    myList = openfile("accountTransactions.txt")
    key = str(acc.acc_ID)
    # filters output
    result = [i for i in myList if str(i["AccID"]) == key]
    if len(result) == 0:
        print("No transactions made")
    count = 1  # counter
    for i in result:
        result = "\nTransaction: " + str(count)
        result += "\nAccount ID: " + str(i["AccID"])
        result += "\nCustomer: " + str(i["Customer"])
        result += "\nTransaction ID: " + str(i["TransID"])
        result += "\nAmount: " + str(i["Amount"])
        result += "\nBalance: " + str(i["Balance"])
        result += "\nTime: " + str(i["TransTime"])
        print(result)
        count += 1
    return None


def case_7_deleteAccount(acc, other) -> None:
    """Deletes all information stored of a chosen account"""
    sure = input("Are you sure you want to delete your account? (y/n) : ")
    if sure == "y" or sure == "Y":
        # if user has another account
        if other and acc.get_balance() > 0:
            transfer_balance = input("Continue transferring balance to other existing accounts? (y/n) : ")
            if transfer_balance == 'y' or transfer_balance == 'Y':
                print("Amount transferred : " + str(acc.get_balance()))
                acc.transfer(other, acc.get_balance())
                method = "_trans_from_removed_" + str(acc.acc_ID)
                other.record_Transaction(acc.get_balance(), method)
            else:
                print("Please head to the nearest bank at" + str(acc.object_customer.object_bank))
        elif acc.get_balance() > 0:
            print("Please head to the nearest bank at" + str(acc.object_customer.object_bank))
        customer_account = acc.object_customer  # Returns to Account choice
        remove_from_accounts_txt(acc)
        remove_from_accountTrans_txt(acc)
        print("Account deleted successfully")
        Account_Choice(customer_account)  # Prevents weird bug where Menu was still running
    else:
        print("Nothing was deleted")
    return None


def remove_from_accountTrans_txt(acc) -> None:
    """Removes transactions from accountTransactions.txt"""
    # reads lines of dictionaries and appends them to a list
    myList = openfile("accountTransactions.txt")
    # filters through the file so that only transactions
    # from the same account are forwarded
    found_list = search_dic_list(myList, "AccID", acc.acc_ID)
    try:
        for element in found_list:
            myList.remove(element)
            # saves changes
        writefile("accountTransactions.txt", myList)
    except TypeError:  # In case there were no transactions made
        pass
    return None


def remove_from_accounts_txt(acc) -> None:
    """Removes selected account from the accounts.txt file"""
    myList = openfile("accounts.txt")
    acid = acc.acc_ID
    # filters search
    found_value = search_dic_list(myList, "AccID", acid)
    # removes redundant item
    myList.remove(found_value[0])
    writefile("accounts.txt", myList)
    return None


ATM()
