import sys
import time
import random
from atmUser import User

allUsers = []
currentUser = {}

class Auth(User):
    def __init__(self):
        User.__init__(self)
        selectOption = input("""Welcome to {} ATM CENTER. Located at {}. 
        Select an option to continue
        1. Register 
        2. Login
        3. Exit
        """.format(self.username.upper(), self.location.upper()))
        
        if selectOption == '1':
            self.register()
        elif selectOption == '2':
            self.login()
        elif selectOption == '3':
            sys.exit()
        else:
            print('Invalid option selected, retry')
            auth = Auth()

    def register(self):
        print('REGISTER NEW ACCOUNT')
        name = input('Enter your name >> ')
        password = input('Enter your new password >> ')
        balance = 0
        actNum = '19'

        for num in range(8):
            actNum = actNum + str(random.randint(0, 9))
            
        userDetails = { 'name': name, 
                        'password': password,
                        'actNum': actNum, 
                        'balance': balance
                    }
        for user in allUsers:
            if user['name'] == name:
                print('Name already exist, try again')
                self.register()
        
        allUsers.extend([userDetails])
        print('Dear {}, you have been registered successfully, your acccount number is {} \n'.format(name.upper(), actNum))
        self.login()
        
    def login(self):
        proceedOption = input("Enter 'R' to Register or 'L' to Login >> ")
        if proceedOption.upper() == 'R':
            self.register()
        elif proceedOption.upper() == 'L':
            print('LOGIN \n Fill in your details to Login')
            userId = input('Enter your name or account number >> ')
            password = input('Enter your password >> ')
            
            for user  in allUsers:
                if user['name'] == userId or user['actNum'] == userId:
                    if user['password'] != password:
                        print('Incorrect Password')
                        self.login()
                    else:
                        print('Login Successfull. Application logging in...')
                        currentUser.update(user)
                        time.sleep(2)
                        transact = Transact()
            else:
                if not currentUser:
                    print('User not found')
                    self.register()   
        else:
            print('Invalid selected option, try again')
            self.login()
            
class Transact:        
    def __init__(self):
        self.username = currentUser['name'].upper()
        self.actNum = currentUser['actNum']
        
        transactOptions = input('Welcome {}, \n What do you want to do? \n 1. Deposit \n 2. Withdraw \n 3. Transfer \n 4. Check Balance \n 5. Logout \n 00. Exit \n '.format(self.username))
        
        if transactOptions == '1':
            self.deposit()
        elif transactOptions == '2':
            self.withdraw()
        elif transactOptions == '3':
            self.transfer()
        elif transactOptions == '4':
            self.checkBalance()
        elif transactOptions == '5':
            currentUser.clear()
            auth = Auth()
        elif transactOptions == '00':
            sys.exit()
        else:
            print('Invalid option selected, try again')
            transact = Transact()
    
    def checkBalance(self):
        balanceOption = input('Dear {}, your current balance is {}. \n Select option \n 0. Back \n '
                              .format(self.username, currentUser['balance']))
        
        if balanceOption == '0':
            transact = Transact()
        else:
            print('Invalid selected option')    
            transact = Transact()
            
    def deposit(self):
        try:
            amount = int(input(""""How much do you want to deposit:
            1. N1,000
            2. N2,000
            3. N3,000
            4. Others
            0. Back
            """))
        except ValueError:
            print('Invalid amount entered, enter a valid figure to deposit')
            self.deposit()
        
        depositOption = { 1: 1000, 2: 2000, 3: 3000 }
        
        if amount == 1 or amount == 2 or amount == 3:
            depositAmount = depositOption[amount]
        elif amount == 4:
            try:
                depositAmount = int(input('Enter the amount you want to deposit in figure: N'))
            except ValueError:
                print('Invalid amount entered, try again')
                self.deposit()
        elif amount == 0:
            transact = Transact()
        else:
            print('Invalid selected option, try again')
            self.deposit()
            
        proceedOption = input("""Dear {}, you are about to deposit {} to your account of account number {}. 
            Select an option to conitnue
            1. Proceed
            2. Cancel
            3. Exit
            """ .format(self.username, depositAmount, self.actNum))
        
        if proceedOption == '1':
            currentUser['balance'] = currentUser['balance'] + depositAmount
            for user in allUsers:
                if user['actNum'] == self.actNum:
                    user['balance'] = currentUser['balance']
            
            option = input("""Dear {}, your deposit of {} is successful. 
            Thank you for banking with us {}.
            You new account balance is {}. 
            Select an option to continue
            1. Make another Deposit
            2. Main Menu
            3. Exit
            """ 
            .format(self.username, depositAmount, self.username, currentUser['balance']))
            
            if option == '1':
                self.deposit()
            elif option == '2':
                transact = Transact()
            elif option == '3':
                sys.exit()
            else:
                print('Invalid selected option')    
                transact = Transact()
                
        elif proceedOption == '2':
            transact = Transact()
        elif (proceedOption == '3'):
            sys.exit()
        else:
            print('Invalid option selected, try again')
            self.deposit()
        
    def withdraw(self):
        try:
            amount = int(input("""How much do you want to withdraw:            
            1. N1000
            2. N2000
            3. N3000
            4. Others
            0. Back
            """))
        except ValueError:
            print('Invalid option selected, try again')
            self.withdraw()
            
        withdrawOption = { 1: 1000, 2: 2000, 3: 3000 }
        
        if amount == 1 or amount == 2 or amount == 3:
            withdrawAmount = withdrawOption[amount]
        elif amount == 4:
            try:
                withdrawAmount = int(input('Enter the amount you want to withdraw in figure: N'))
            except ValueError:
                print('Invalid amount entered, try again')
                self.withdraw()
        elif amount == 0:
            transact = Transact()
        else:
            print('Invalid selected option, try again')
            self.withdraw()
        
        proceedOption = input("""Dear {}, you are about to withdraw {} from your account of account number {}. 
            Select an option to conitnue
            1. Proceed
            2. Cancel
            3. Exit
            """ .format(self.username, withdrawAmount, self.actNum))
        
        if proceedOption == '1':
            if currentUser['balance'] < withdrawAmount:
                print("Dear {}, your balance is insufficient for the amount you want to withdraw. Your balance is {}. Deposit to your account and try again ".format(self.username, currentUser['balance']))
                transact = Transact()
            else:
                currentUser['balance'] = currentUser['balance'] - withdrawAmount
                for user in allUsers:
                    if user['actNum'] == self.actNum:
                        user['balance'] = currentUser['balance']
                
                option = input("""Dear {}, your withdraw of {} is successful.
                Thank you for banking with us {}.
                Your new account balance is {}.
                Select an option to continue:
                1. Make another Withdraw
                2. Main Menu
                3. Exit 
                """
                .format(self.username, withdrawAmount, self.username, currentUser['balance']))
                if option == '1':
                    self.withdraw()
                elif option == '2':
                    transact = Transact()
                elif option == '3':
                    sys.exit()
                else:
                    print('Invalid selected option')
                    transact = Transact()
        elif proceedOption == '2':
            transact = Transact()
        elif proceedOption == '3':
            sys.exit()
        else:
            print('Invalid selected option')
            transact = Transact()
        
    def transfer(self):
        try:
            receiverActNum = int(input('Enter receiver account number >> '))
        except ValueError:
            print('Enter a valid account number')
            self.transfer()
        
        try:
            amount = int(input("""How much do you want to transfer:
                1. N1000
                2. N2000
                3. N3000
                4. Others
                0. Back
                """))
        except ValueError:
            print('Invalid option selected, try again')
            self.transfer()
        
        transferOption = { 1: 1000, 2: 2000, 3: 3000 }

        if amount == 1 or amount == 2 or amount == 3:
            transferAmount = transferOption[amount]
        elif amount == 4:
            try:
                transferAmount = int(input('Enter the amount you want to transfer in figure: N'))
            except ValueError:
                print('Invalid amount entered, try again')
                self.transfer()
        elif amount == 0:
            transact = Transact()
        else:
            print('Invalid selected option, try again')
            self.transfer()
        
        if transferAmount > currentUser['balance']:
            print(""""Dear {}, your balance is insufficient for the transfer you want to make. 
            You can deposit and try again. 
            Your current balance is {} """ .format(self.username, currentUser['balance']))
            transact = Transact()
        else:
            proceedOption = input("""Dear {}, you are about to transfer the sum of {} to account number {}.
            Select an option to continue:
            1. Proceed
            2. Cancel
            0. Exit
            """ .format(self.username, transferAmount, receiverActNum))
            
            if proceedOption == '1':
                receiverName = ''
                for user in allUsers:
                    if user['actNum'] == str(receiverActNum):
                        user['balance'] = user['balance'] + transferAmount
                        receiverName = user['name']
                else:
                    if not receiverName:
                        print("Can't find User with the account number you entered, try again")
                        self.transfer()
                
                for user in allUsers:
                    if user['actNum'] == self.actNum:
                        user['balance'] = user['balance'] - transferAmount

                currentUser['balance'] = currentUser['balance'] - transferAmount
                
                option = input("""Dear {}, your transfer of {} to {} of {} is successful.
                Thank you for banking with us.
                Your new account balance is {}.
                Select an option to continue
                1. Make another Transfer
                2. Main Menu
                3. Exit        
                """ .format(self.username, transferAmount, receiverName.upper(), receiverActNum, currentUser['balance']))
                
                if option == '1':
                    self.transfer()
                elif option == '2':
                    transact = Transact()
                elif option == '3':
                    sys.exit()
                else:
                    print('Invalid selected Option')
                    transact = Transact()
                    
            elif proceedOption == '2':
                self.transfer()
            elif proceedOption == '0':
                sys.exit()
            else:
                print('Invalid selected option, try again')
                self.transfer()
                    
        
auth = Auth()