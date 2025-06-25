from datetime import datetime

date_format = '%d-%m-%Y'
CATEGORIES = {'I': 'Income', 'E': 'Expense'}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if not date_str and allow_default:
        return datetime.now().strftime(date_format)
    
    try:
        vaild_date = datetime.strptime(date_str, date_format)
        return vaild_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please use 'dd-mm-yyyy'.")
        return get_date(prompt, allow_default)


def get_amount(prompt, allow_default=False):
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount(prompt, allow_default)


def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ")
    if category in CATEGORIES:
        return CATEGORIES[category]
    else:
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
        return get_category()

def get_description():
    return input("Enter a description: ")