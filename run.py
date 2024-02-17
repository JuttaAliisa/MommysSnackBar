import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mommys_snackbar_helper')

def consumption():
    """
    function for inputtin consumption values
    """
# Select the appropriate worksheet
    worksheet = SHEET.worksheet('usage')

# Get user input
    print('When taking a snack from the stock, please insert correct number for the snack')
    user_choice = input("Enter number: ")

# Define the values based on user input
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
        values_to_add = [0, 1, 0, 0, 0, 1]
        cell_value = worksheet.cell(1, 6).value
    else:
        print("Invalid choice. Please enter a number from 1 through 6")
        consumption()


    # Add the values to the next available row
    next_row = len(worksheet.get_all_values()) + 1
    worksheet.append_row(values_to_add)

    print(f"Thank you! 1pc of {cell_value} deleted from SnackBar stock ")
    print('Do you want to take out another item?')
    user_choice = input("y=yes, n=no: ")
    if user_choice == 'y':
        consumption()
    elif user_choice == 'n':
        start()
    else:
        print("Invalid choice. Please enter y or n: ")
        exit()

def stock():
    """
    Function to check current stock value
    """
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
        print(f"{product}: {amount}pc")
        
def recommendation():
    """
    Function to calculate purchase recommendation
    """
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

def restock():
    """
    Function to perform restock of the snack bar
    """
    print("Welcome to restock feature!")

    # Select the appropriate worksheet
    restock_sheet = SHEET.worksheet('restock')
    usage_sheet = SHEET.worksheet('usage')
    stock_sheet = SHEET.worksheet('stock')

    # Wipe out usage sheet
    # Get all values in the worksheet
    all_values = usage_sheet.get_all_values()
    # Loop through each row starting from the second row
    for i in range(1, len(all_values)):
        # Loop through each cell in the row
        for j in range(len(all_values[i])):
            # Check if the cell value is a number and delete it
            if all_values[i][j].replace('.', '', 1).isdigit():
                usage_sheet.update_cell(i + 1, j + 1, '')

    #request restock amounts
restock()
