# Bank Management System

import csv


class User:
    def __init__(self, ID, name, username, password, balance):
        self.ID = ID
        self.name = name
        self.username = username
        self.password = password
        self.balance = balance


def main():
    print("WELCOME TO BANK MANAGEMENT SYSTEM!")
    print("==================================")

    mainMenuSelection()


def displayMainMenu():
    """ Shows the main menu."""

    print("\n==============================")
    print("MENU")
    print("1) Login")
    print("2) Crate an account")
    print("3) View Customers' information")
    print("4) Exit System")
    print("==============================\n")


def mainMenuSelection():
    """ Displays the main menu and ask for user's choice."""

    displayMainMenu()

    choice = 0
    while not (choice in [1, 2, 3, 4]):
        choice = int(input("Enter your choice: "))

        if not (choice in [1, 2, 3, 4]):
            print("Invalid choice. Please try again.")


    if choice == 1:
        login()
    elif choice == 2:
        createAccount()
    elif choice == 3:
        viewCustomersInfo()
    else:
        print("Thank you for using the system. Goodbye!")


def readAccountsCSV():
    """ Read data from accounts.csv. """

    user_info = []

    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, newline="") as account_file:
        rows = csv.reader(account_file)

        for row in rows:
            user_info.append(User(row[0], row[1], row[2], row[3], row[4]))


    return user_info


def createAccount():
    """ A function to create an account. Accounts.csv will be updated."""

    # Get user's ID card number and validate
    ID = ""
    id_valid = False

    while not id_valid:
        ID = input("Enter your ID card number: ")

        id_valid = validateID(ID)
        if not id_valid:
            print("Invalid ID number. Please try again.")


    # Get user's name
    name = ""
    while name == "":
        name = input("Enter your name: ")


    # Get user's user name and validate
    username = ""
    username_valid = False

    while not username_valid:
        username = input("Enter your user name (at least 6 characters): ")

        username_valid = validateUserName(username)
        if not username_valid:
            print("Invalid user name. Please try again.")


    # Get user's password and validate
    password = ""
    password_valid = False

    while not password_valid:
        password = input("Your password should consist of at least one number and at least one capital letter.\n"
                         "Enter your password: ")

        password_valid = validatePassword(password)
        if not password_valid:
            print("Invalid password. Please try again.")


    # Write account information into accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "a", newline="") as account_file:
        writer = csv.writer(account_file)

        writer.writerow([ID, name, username, password, 0])


    print("Account created successfully.")


    mainMenuSelection()     # Go back to main menu


def validateID(ID):
    """ Validate the ID entered by user."""

    validFlag = True

    if not ID[0].isalpha():
        validFlag = False

    for i in range(1, len(ID)):
        if not ID[i].isnumeric():
            validFlag = False

    return validFlag


def validateUserName(username):
    """ Validate the user name and check if it is taken by someone else already."""

    validFlag = True

    # The user name should consist of at least 6 characters
    if len(username) < 6:
        print("The user name should consist of at least 6 characters. Please try again.")
        validFlag = False

    # Read accounts.csv to get all the existing user names
    existing_usernames = []

    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, newline="") as accounts_file:
        rows = csv.reader(accounts_file)

        for info in rows:
            existing_usernames.append(info[2])

        existing_usernames.pop(0)       # Pop the header

    #print(existing_usernames)  # For debugging

    # The user name entered by user should be unique
    if username in existing_usernames:
        validFlag = False
        print("The user name is already taken. Please try again.")


    return validFlag


def validatePassword(password):
    """ Validates the password entered by the user."""

    validFlag = True

    if len(password) < 8:
        print("The password should consist of at least 8 characters. Please try again.")
        validFlag = False


    # Check if the password contains at least one number and one capital letter
    number_exist = False
    capital_exist = False

    for char in password:
        if char.isnumeric():
            number_exist = True

        if char.isupper():
            capital_exist = True


    if not number_exist:
        print("Your password should consist of at least one number.")
        validFlag = False

    if not capital_exist:
        print("Your password should consist of at least one capital number.")
        validFlag = False

    if number_exist and capital_exist:
        validFlag = True

    return validFlag


def login():
    """ A function to let user to login to the system."""

    # Get user name
    username = ""
    while username == "":
        username = input("Enter your user name: ")

    # Get password
    password = ""
    while password == "":
        password = input("Enter your password: ")


    # Read data from accounts.csv
    user_info = readAccountsCSV()

    # Check if the user name and password matches one of the fields in user_info
    match = False

    for field in user_info:
        if username == field.username:
            if password == field.password:
                match = True


    if match:
        print("You have successfully logged in.")
        userMenuSelection(username)  # Proceed to user menu after user login successfully
    else:
        print("The user name and password does not match. Please try again.")
        mainMenuSelection()     # Proceed to main menu when user fail to login


def displayUserMenu():
    """ Displays the user menu."""

    print("\n===========================")
    print("User Menu")
    print("1) Withdraw money")
    print("2) Deposit money")
    print("3) View Account Information")
    print("4) Edit Account Information")
    print("5) Erase Account")
    print("===========================\n")


def userMenuSelection(username):
    """ Display the user menu and ask for user's choice."""

    displayUserMenu()

    choice = 0
    while not (choice in [1, 2, 3, 4, 5]):
        choice = int(input("Enter your choice: "))


    if choice == 1:
        withdrawMoney(username)
    elif choice == 2:
        depositMoney(username)
    elif choice == 3:
        viewAccountInfo(username)
    elif choice == 4:
        editAccountInfo(username)
    else:
        eraseAccount(username)


def withdrawMoney(username):
    """ This function performs money withdrawal."""

    # Read data from accounts.csv
    user_info = readAccountsCSV()

    # Ask for withdrawal amount
    withdrawal_amount = 0
    while not (0 < withdrawal_amount <= 20000):
        withdrawal_amount = float(input("Enter withdrawal amount (maximum $20000): "))


    # Update account balance
    for user in user_info:
        if username == user.username:
            balance = float(user.balance)
            balance -= withdrawal_amount
            user.balance = balance


    # Write back to accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "w", newline="") as update_file:
        writer = csv.writer(update_file)

        for field in user_info:
            writer.writerow([field.ID, field.name, field.username, field.password, field.balance])


    print("Money is withdrawn from you account.")

    # Proceed to user menu
    userMenuSelection(username)


def depositMoney(username):
    """ This function performs money deposit."""

    # Read data from accounts.csv
    user_info = readAccountsCSV()

    # Ask for deposit amount
    deposit_amount = 0
    while deposit_amount == 0:
        deposit_amount = float(input("Enter deposit amount: "))


    # Update account balance
    for user in user_info:
        if username == user.username:
            balance = float(user.balance)
            balance += deposit_amount
            user.balance = balance


    # Write back to accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "w", newline="") as update_file:
        writer = csv.writer(update_file)

        for field in user_info:
            writer.writerow([field.ID, field.name, field.username, field.password, field.balance])


    print("Money is deposited to you account.")

    # Proceed to user menu
    userMenuSelection(username)


def viewCustomersInfo():
    """ Displays customers' information."""

    # Login as admin

    admin_password = "123456"

    password = ""
    while password == "":
        password = input("Enter administrator password: ")

        if password != admin_password:
            print("Wrong password. Try again.")


    # Read customers' information from accounts.csv
    user_info = readAccountsCSV()

    print("\nCustomers' Information")
    print("{:15} {:20} {:20}".format("Name", "User name", "Balance"))
    print("==========================================================")

    for user in range(len(user_info)):
        if user != 0:   # Skip the header
            print("{:15} {:20} ${:20}\n".format(user_info[user].name, user_info[user].username, user_info[user].balance))


    key = 0
    while not (key in [1]):
        key = int(input("Enter 1 to exit"))

    mainMenuSelection()


def editAccountInfo(username):
    """ Edit account information of a user."""

    # Choose whether they would like to edit id number or password
    print("\n==========================")
    print("1) Update ID number")
    print("2) Change account password")
    print("==========================\n")

    choice = 0
    while not (choice in [1, 2]):
        choice = int(input("Enter your choice: "))


    # Read data from accounts.csv
    user_info = readAccountsCSV()


    if choice == 1:         # Edit ID number
        editID(username)
    else:                   # Edit account password
        changeAccountPassword(username)


def eraseAccount(username):
    """ Erase an account."""

    # Read data from accounts.csv
    user_info = readAccountsCSV()


    # Get the details of the user
    user_id_number = ""
    user_password = ""

    for user in user_info:
        if username == user.username:
            user_id_number = user.ID
            user_password = user.password


    # Enter ID card number
    ID = ""
    ID_correct = False
    while not ID_correct:
        ID = input("Enter the ID card number for the account: ")
        if ID == user_id_number:
            ID_correct = True


    # Enter password
    password = ""
    password_correct = False
    while not password_correct:
        password = input("Enter password for the account: ")
        if password == user_password:
            password_correct = True


    # Write updated account information into accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "w", newline="") as account_file:
        writer = csv.writer(account_file)

        for user in user_info:
            if user.username != username:
                writer.writerow([user.ID, user.name, user.username, user.password, user.balance])


    print("Account erased successfully.")


def viewAccountInfo(username):
    """ Displays the account information of the user."""

    # Read data from accounts.csv
    user_info = readAccountsCSV()

    for user in user_info:
        if username == user.username:
            print("\nAccount Information")
            print("{:15} {:20} {:20}".format("Name", "User name", "Balance"))
            print("{:15} {:20} ${:20}\n".format(user.name, user.username, user.balance))


    # Proceed to user menu
    userMenuSelection(username)


def editID(username):

    # Read data from accounts.csv
    user_info = readAccountsCSV()

    # Get new ID card number
    new_id = ""
    new_id_valid = False

    while not new_id_valid:
        new_id = input("Enter new ID card number: ")
        new_id_valid = validateID(new_id)

        if not new_id_valid:
            print("Invalid ID number. Please try again.")


    # Replace the old ID number by the new one
    for user in user_info:
        if user.username == username:
            user.ID = new_id


    # Write back to accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "w", newline="") as update_file:
        writer = csv.writer(update_file)

        for field in user_info:
            writer.writerow([field.ID, field.name, field.username, field.password, field.balance])


    print("Your ID card number has been updated.")
    userMenuSelection()


def changeAccountPassword(username):
    # Read data from accounts.csv
    user_info = readAccountsCSV()

    # Get new password
    new_password = ""
    new_password_valid = False

    while not new_password_valid:
        new_password = input("Enter new password: ")
        new_password_valid = validatePassword(new_password)


    # Replace the old ID number by the new one
    for user in user_info:
        if user.username == username:
            user.password = new_password

    # Write back to accounts.csv
    path = "D:/1/Code/Python/Projects/Bank Management System/accounts.csv"
    with open(path, "w", newline="") as update_file:
        writer = csv.writer(update_file)

        for field in user_info:
            writer.writerow([field.ID, field.name, field.username, field.password, field.balance])

    print("Your password has been updated.")
    userMenuSelection()



main()
