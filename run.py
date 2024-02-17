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
# Get user input
    print('When taking a snack from the stock, please insert correct number for the snack')
    user_choice = input("Enter number: ")

# Define the values based on user input
    if user_choice == '1':
        values_to_add = [1, 0, 0, 0, 0, 0]
    elif user_choice == '2':
        values_to_add = [0, 1, 0, 0, 0, 0]
    elif user_choice == '3':
        values_to_add = [0, 0, 1, 0, 0, 0]
    elif user_choice == '4':
        values_to_add = [0, 0, 0, 1, 0, 0]
    elif user_choice == '5':
        values_to_add = [0, 0, 0, 0, 1, 0]
    elif user_choice == '6':
        values_to_add = [0, 1, 0, 0, 0, 1]
    else:
        print("Invalid choice. Please enter a number from 1 through 6")
        consumption()

    # Select the appropriate worksheet
    worksheet = SHEET.worksheet('usage')

    # Add the values to the next available row
    next_row = len(worksheet.get_all_values()) + 1
    worksheet.append_row(values_to_add)

    print(f"Thank you! 1pc deleted from SnackBar stock ")
    print('Do you want to take out another item?')
    user_choice = input("y=yes, n=no")
    if user_choice == 'y':
        consumption()
    elif user_choice == 'n':
        start()
    else:
        print("Invalid choice. Please enter y or n: ")
        exit()


consumption()
