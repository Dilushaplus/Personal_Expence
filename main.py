import pandas as pd
import csv
from datetime import datetime
from dataentry import get_date, get_amount, get_category, get_description

class FinanceCSV:
    csv_file = 'finance_data.csv'
    columns = ['Date', 'Amount', 'Category', 'Description']
    format = '%d-%m-%Y'

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

    # To give all the transactions within a date range
    @classmethod
    def get_entries_by_date_range(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        #df data refers to the dataframe on finance_data.csv
        df['Date'] = pd.to_datetime(df['Date'], format=cls.format)
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        return df.loc[mask]

def add():
    FinanceCSV.initialize_csv()
    data = get_date("Enter the date of transaction (dd-mm-yyyy): ", allow_default=True)
    amount = get_amount("Enter the amount: ", allow_default=True)
    category = get_category()
    description = get_description()
    FinanceCSV.add_entry(data, amount, category, description)

if __name__ == "__main__":
    add()