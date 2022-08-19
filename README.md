# Python_OOP_Assignment_2021

Author : Christina Vargka C20737009
Date Reviewed : 18/12/2021
Program that simulates an ATM machine where Customers can view and manage their accounts.
Summary:
-	Classes : Bank -> Customer -> Account == CheckingAccount/SavingAccount
-	Main Functions : ATM(), Account_Choice(), Menu()
CLASSES:
-	Bank(object): Holds any necessary about the Bank. There are default values set.
o	__init__: Initializes its Name, Address, Country and Interest Rate. 
                 All of them are set as private.
o	Each private attribute has a get method.
o	get_monthly_interest_rate: returns interest rate
o	__str__: Prints out Bank’s details except for the interest rate. Required output seemed weird otherwise.
-	Customer(object): Holds information about a Customer 
                                    Aggregates Bank class
o	__init__: Initializes the Bank object, and the Customer’s Name, Age and address as well as a ID. This ID will be used to access the Customer and their accounts
customer_ID and name are private.
o	Private attribute has get methods
o	__str__: Prints out Customer’s details and information.
-	Account(object): Holds basic account information. Contains most methods and operations.
                                  Aggregates Customer Class.
o	__init__: Initializes the Customer object, Account_ID and balance.
                  Balance is private.
o	Balance get method.
o	deposit: Increases balance by a specified amount. Updates Account.txt
o	withdraw: Decreases balance by a specified amount. Updates Account.txt
o	transfer: withdraws amount from account a, deposits amount to account b
o	record_transaction: passes a float and a string. It saves transactions into the AccountTransactions.txt file in the form of a dictionary. Increments transaction identifier.
o	update_balance_in_txt: works together with withdraw and deposit and “updates” balance of account. This is done by first deleting the instance then re-adding it to the list of dictionaries that saves the accounts.
o	__add__: allows the balances of two accounts to be added together. Works together with 
o	__radd__: which allows at least on of them to be printed in case there is an Attribute error.
o	__str__: prints out customer’s name, the bank’s name and their account ID.
-	SavingAccount(Account): Child of Account. One withdrawal per month. Age: 14+
o	__init__: Initializes the Account attributes inherited.
o	get_monthly_interest: Grabs monthly interest from the Bank class then multiplies it with the account balance.
o	check_amount: Ensures that the amount to be withdrawn is not greater than the account balance.
o	write_and_withdraw_amount: Checks if amount can be withdrawn then saves the transaction to file. Works with check_amount(), withdraw() and record_transaction(). If the returned value from check_amount() is True, it withdraws the amount.
o	okToWithdraw: Filters list of dictionaries. Further filters out types of Transactions. Compares today’s date with date of last withdrawal and returns the Boolean value.
o	__str__: Prints out savings account information as well as inherited __str__ from Account()and __str__ from Customer()
-	CheckingAccount(Account): Can have a negative balance up to specified amount.
o	__init__: Initializes parent and the credit limit.
o	Get function for credit limit.
o	check_amount: Similar to check_amount() in SavingAccount(). 
Ensures balance - amount to be withdrawn is not smaller than credit limit
o	write_and_withdraw _amount: Similar to write_and_withdraw _amount() in SavingAccount()
Has a different output.
o	__str__(): Prints out checking account information as well as the inherited __str__ from Account() and __str__ from Customer()
MAIN FUNCTIONS:
-	ATM(): Main interface for Customers. Allows customers to log in or create their account.
Related functions:
o	enter_customer_details: for ATM() Inputs details of a customer then returns a dictionary with their information.
o	login: Creates a customer class if details found in the customers.txt file.
o	sign_up: Ensures there are no duplicate PIN numbers. Writes new Customer to text file.
-	Account_Choice(): Once Customer logs in it displays a menu and they may choose to view their accounts + total balance between them or create/use either a Savings account or a Checking account 
Related functions:
o	create_acc: forCreates either a SavingAccount or a CheckingAccount if user doesn’t have one.
o	search_acc: Loads accounts into the program if they exist.
-	Menu(): Main Function. Allows user to View their balance, withdraw, deposit, transfer funds, view bank’s and their own interest (if a savings account), view transaction history and delete an account. 
o	transfer_acc: Creates a temporary Account object so that funds may be transferred.
o	amount_verification: Prompts user to enter an amount and will loop until value is numeric (float)
o	case_2_withdrawal: If it’s a Saving account it checks if there can be a withdrawal. Withdraws amount
o	case_3_deposit: Deposits amount
o	case_4_Transfer: Checks if saving account and if transfer is possible. If yes, transfers amount to another account.
o	case_5_viewInterest: Displays interest. Monthly interest if is a saving account
o	case_6_transactionHistory: Displays transaction history of account.
o	case_7_deleteAccount: If account has a balance > 0, or user has a different account, it will ask if they want to transfer their funds. Deletes account and displays bank information when appropriate.
o	remove_from_accountTrans_txt: Removes all instances of account in the accountTransactions.txt file
o	remove_from_accounts_txt: Removes account from accounts.txt file
OTHER FUCNTIONS:
-	Number_Verification: Verifies input is a number and positive
-	openfile: Opens a file and saves contents into a list. Can create a new file if it doesn’t exist.
-	writefile: Writes contents of a list into a text file all of which are in separate lines.
-	search_dic_list: Searches through the list of dictionaries read from a txt file.
-	days_between: Returns absolute difference between two dates

USER MANUAL
Run program and it will call functions and create files as required. To transfer to another account please refer to the accounts.txt file and enter the required Acc_ID value when prompted.
Each transaction and account have a unique ID
‘ID’ = Customer ID
‘AccID’ = Account ID
‘TransID’ = Transaction ID: Changes depending on the type of transaction and the account its from.
Pressing 0 in any of the menus will exit the program
Pressing 9 will Log user out

CHALLENGES
-	The time constraint was one of the biggest challenges to overcome. 
-	I had disproportionately huge issue figuring out how to properly structure the objects. The result worked for what I envisioned. 
-	Having a comprehensive function structure and what I can or cannot implement as a method.
-	I had to abandon plans to improve on the write_and_withdraw_amount() and check_amount() in a way that they would be an Account method due to time constraints.
-	I faced a roadblock when it came to figuring out how to read and write files properly. GeeksforGeeks.org was my savior on that one.
-	Creative part was very difficult to figure out and required a lot of research. I went with a very safe option that I would be able to implement in a timely manner.
-	I had way too many bugs in the okToWithdraw function, where it had a bug where it wouldn’t allow further withdrawals even if the only transaction was a deposit. Patched it once I figured out a suitable approach and I implemented a second filter to filter out Transactions. Main reason why the TransID has the transaction type in it.
-	Testing after structure was changed (I moved functions and made them into methods) was very time consuming.
