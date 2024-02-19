import gspread
from google.oauth2.service_account import Credentials
from os import system, name
from colorama import Fore, Back, Style
from openpyxl import load_workbook

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mommys_snackbar_helper')

def clear():
    '''
    Clears terminal
    '''
    system('cls' if name == 'nt' else 'clear')

def consumption():
    """
    function for inputting consumption values
    """
    #clear terminal for better readability
    clear()

    # Select the appropriate worksheet
    worksheet = SHEET.worksheet('usage')
    stock_sheet = SHEET.worksheet('stock')

    # Get user input
    print(Fore.MAGENTA)
    print(Style.BRIGHT + "Snack Consumption logging \n")
    print(Style.RESET_ALL)
    print(Fore.BLUE)
    print('When taking a snack from the stock, please insert correct number for the snack \n')
    print(Style.RESET_ALL)
    
    products = worksheet.row_values(1)
    numbers = [1, 2, 3, 4, 5, 6]
    for product, number in zip(products, numbers):
        print(Fore.BLUE)
        print(f"{product} = {number}")
        print(Style.RESET_ALL)

    user_choice = input("What did you take? Enter number: ")

    # Define the values based on user input and validating input
    if user_choice == '1':
        values_to_add = [1, 0, 0, 0, 0, 0]
        cell_value = worksheet.cell(1, 1).value
    elif user_choice == '2':
        values_to_add = [0, 1, 0, 0, 0, 0]
        cell_value = worksheet.cell(1, 2).value
    elif user_choice == '3':
        values_to_add = [0, 0, 1, 0, 0, 0]
        cell_value = worksheet.cell(1, 3).value
    elif user_choice == '4':
        values_to_add = [0, 0, 0, 1, 0, 0]
        cell_value = worksheet.cell(1, 4).value
    elif user_choice == '5':
        values_to_add = [0, 0, 0, 0, 1, 0]
        cell_value = worksheet.cell(1, 5).value
    elif user_choice == '6':
        values_to_add = [0, 0, 0, 0, 0, 1]
        cell_value = worksheet.cell(1, 6).value
    else:
        print(Fore.RED)
        print("\nInvalid choice. Please enter a number from 1 through 6 \n")
        print(Style.RESET_ALL)
        print("Press enter to try again")
        input()
        consumption()


    # Add the values to the next available row
    worksheet.append_row(values_to_add)
    # Turn the value negative and add to stock sheet
    negative_values = [-x for x in values_to_add]
    stock_sheet.append_row(negative_values)

    print(f"\nThank you! 1pc of {cell_value} deleted from SnackBar stock \n")
    print('Do you want to take out another item? \n')

    def get_user_choice():
        user_choice = input("y=yes, n=no: ")
        return user_choice.lower()


    while True:
        user_choice = get_user_choice()

        if user_choice == 'y':
            consumption()
            break  # exit the loop after consumption
        elif user_choice == 'n':
            print("Thank you for your contribution!\n")
            print("Press enter to get back to start\n")
            input("")
            start()
            break  # exit the loop after starting again
        else:
            print(Fore.RED)
            print("Invalid choice. Please enter y or n: ")
            print(Style.RESET_ALL)

def stock():
    """
    Function to check current stock value
    """
    #clear terminal for better readability
    clear()
    print(Fore.MAGENTA)
    print(Style.BRIGHT + "The current stock is: \n")
    print(Style.RESET_ALL)
    # Select the appropriate worksheet
    usage_sheet = SHEET.worksheet('usage')
    restock_sheet = SHEET.worksheet('restock').get_all_values()
    stock_sheet = SHEET.worksheet('stock')

    # Get the values from the "usage" and "restock" sheets
    usage_values = usage_sheet.row_values(2)
    restock_values = restock_sheet[-1]

    # Convert the values to integers
    usage_values = [int(value) for value in usage_values]
    restock_values = [int(value) for value in restock_values]

    # Calculate the difference between restock and usage
    stock_values = [restock - usage for restock, usage in zip(restock_values, usage_values)]
    # Add the values to the next available row
    worksheet = SHEET.worksheet('stock')
    next_row = len(worksheet.get_all_values()) + 1
    worksheet.append_row(stock_values)
    
    #print user friendly stock values
    products = stock_sheet.row_values(1)
    stock_sheet = SHEET.worksheet('stock').get_all_values()
    amounts = stock_sheet[-1]
    for product, amount in zip(products, amounts):
        print(Fore.GREEN)
        print(f"{product}: {amount}pc")
        print(Style.RESET_ALL)

    print("\nPress enter to go back to main page")
    input()
    start()
        
def recommendation():
    """
    Function to calculate purchase recommendation
    """
    #clear terminal for better readability
    clear()
    print(Fore.MAGENTA)
    print(Style.BRIGHT + "Restock recommendations for a shopping trip \n")
    print(Style.RESET_ALL)
    print("Please consider purchasing the following snacks to make sure the stock lasts:")
    print(Fore.GREEN)

    # Select the appropriate worksheet
    usage_sheet = SHEET.worksheet('usage')
    stock_sheet = SHEET.worksheet('stock').get_all_values()
    recommendation_sheet = SHEET.worksheet('recommendation')

    # Get the values from the "usage" and "stock" sheets
    usage_values = usage_sheet.row_values(2)
    stock_values = stock_sheet[-1]
    
    # Convert the values to integers
    usage_values = [int(value) for value in usage_values]
    stock_values = [int(value) for value in stock_values]

    # Calculate the difference between usage and stock
    recommendation_values = [usage - stock for usage, stock in zip(usage_values, stock_values)]

    # Add the values to the next available row
    worksheet = SHEET.worksheet('recommendation')
    next_row = len(worksheet.get_all_values()) + 1
    worksheet.append_row(recommendation_values)

    #print user friendly recommendation list
    products = recommendation_sheet.row_values(1)
    recommendation_sheet = SHEET.worksheet('recommendation').get_all_values()
    amounts = recommendation_sheet[-1]
    amounts = [int(value) for value in amounts]
    for product, amount in zip(products, amounts):
        if amount > 0:
            print(f"{product}: {amount}pc")
        else:
            print(f"{product} has enough stock")
    print(Style.RESET_ALL)
    print("\nPress enter to go back to main page")
    input()
    start()

def restock():
    """
    Function to perform restock of the snack bar
    """
    #clear terminal for better readability
    clear()
    print(Fore.MAGENTA)
    print(Style.BRIGHT + "Welcome to restock feature!")
    print(Style.RESET_ALL)
    print(Fore.BLUE)
    print("Please add stocked amount for every item")
    print(Style.RESET_ALL)
    print(Fore.GREEN)

    # Select the appropriate worksheet
    restock_sheet = SHEET.worksheet('restock')
    usage_sheet = SHEET.worksheet('usage')
    stock_sheet = SHEET.worksheet('stock')

    # Get the header row as a list of Cell objects
    header_row = restock_sheet.row_values(1)
    header_cells = restock_sheet.range(2, 1, 2, len(header_row))

    # List to store restock quantities
    restock_values = []

    # Get all values in the usage sheet
    all_usage_values = usage_sheet.get_all_values()

    # Get restock amounts from the user with input validation
    for i, product in enumerate(header_row):
        while True:
            try:
                quantity = int(input(f"How many {product}s restocked: "))
                # Check if the input is non-negative
                if quantity >= 0:
                    break
                else:
                    print("Please enter a non-negative number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Check if the input is non-zero before updating the cells
        if quantity != 0:
            header_cells[i].value = quantity
            for j in range(2, len(all_usage_values)):
                if all_usage_values[j][i].replace('.', '', 1).isdigit():
                    usage_sheet.update_cell(j + 1, i + 1, '')
        
        restock_values.append(quantity)

    # Update the cells with the new values
    restock_sheet.update_cells(header_cells)
    stock_sheet.append_row(restock_values)

    print(Style.RESET_ALL)
    print("Restock logged. Thank you for restocking!\n")
    print("Press enter to go back to main page")
    input()
    start()

def start():
    clear()
    print("Welcome to Mommy's SnackBar Stock Helper")
    print("Help Mom and log your activity around snack bar.")
    print("This way we can make sure none of is left with out a snack aver again!")
    print("")
    print("Would you like to:")
    print("1: Take a snack")
    print("2: Restock snacks")
    print("3: Check current stock")
    print("4: Get shopping recommendations")
    user_choice = input("Enter number: ")

    # Define the values based on user input
    if user_choice == '1':
        consumption()
    elif user_choice == '2':
        restock()
    elif user_choice == '3':
        stock()
    elif user_choice == '4':
        recommendation()
    else:
        print("Invalid choice. Please enter a number between 1 and 4")
        exit()

start()
