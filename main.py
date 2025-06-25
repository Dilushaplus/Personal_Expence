import pandas as pd
import csv
from datetime import datetime

date_format = '%d-%m-%Y'
CATEGORIES = {'I': 'Income', 'E': 'Expense'}

class FinanceCSV:
    csv_file = 'finance_data.csv'
    columns = ['Date', 'Amount', 'Category', 'Description']
    format = date_format

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.csv_file, index=False)

    @classmethod
    def add_entry(cls, data, amount, category, description):
        new_entry = {
            'Date': data,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        with open(cls.csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(new_entry)
        print("Entry added successfully.")

    @classmethod
    def get_entries_by_date_range(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df['Date'] = pd.to_datetime(df['Date'], format=cls.format)
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        return df.loc[mask]

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if not date_str and allow_default:
        return datetime.now().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please use 'dd-mm-yyyy'.")
        return get_date(prompt, allow_default)

def get_amount(prompt, allow_default=False):
    try:
        amount = float(input(prompt))
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

def add():
    FinanceCSV.initialize_csv()
    data = get_date("Enter the date of transaction (dd-mm-yyyy): ", allow_default=True)
    amount = get_amount("Enter the amount: ", allow_default=True)
    category = get_category()
    description = get_description()
    FinanceCSV.add_entry(data, amount, category, description)

    # Show summary after adding
    df = pd.read_csv(FinanceCSV.csv_file)
    print("\n--- Last Transaction ---")
    print(df.tail(1).to_string(index=False))
    # Calculate totals
    income = df[df['Category'] == 'Income']['Amount'].sum()
    expense = df[df['Category'] == 'Expense']['Amount'].sum()
    balance = income - expense
    print("\n--- Summary ---")
    print(f"Total Income: {income}")
    print(f"Total Expense: {expense}")
    print(f"Net Balance: {balance}")

def show_all_entries():
    FinanceCSV.initialize_csv()
    df = pd.read_csv(FinanceCSV.csv_file)
    print("\n--- All Transactions ---")
    print(df.to_string(index=False))

if __name__ == "__main__":
    add()