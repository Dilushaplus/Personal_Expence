import os
import pandas as pd
import pytest
from unittest import mock
from main import FinanceCSV

def test_initialize_csv(tmp_path):
    test_csv = tmp_path / "test_finance_data.csv"
    FinanceCSV.csv_file = str(test_csv)
    # Remove file if exists
    if test_csv.exists():
        test_csv.unlink()
    FinanceCSV.initialize_csv()
    assert test_csv.exists()
    df = pd.read_csv(test_csv)
    assert list(df.columns) == FinanceCSV.columns

def test_add_entry(tmp_path):
    test_csv = tmp_path / "test_finance_data.csv"
    FinanceCSV.csv_file = str(test_csv)
    FinanceCSV.initialize_csv()
    FinanceCSV.add_entry("01-01-2024", 100, "Food", "Lunch")
    df = pd.read_csv(test_csv)
    assert len(df) == 1
    assert df.iloc[0]['Amount'] == 100
    assert df.iloc[0]['Category'] == "Food"
    assert df.iloc[0]['Description'] == "Lunch"

def test_get_entries_by_date_range(tmp_path):
    test_csv = tmp_path / "test_finance_data.csv"
    FinanceCSV.csv_file = str(test_csv)
    FinanceCSV.initialize_csv()
    FinanceCSV.add_entry("01-01-2024", 100, "Food", "Lunch")
    FinanceCSV.add_entry("05-01-2024", 200, "Transport", "Bus")
    FinanceCSV.add_entry("10-01-2024", 300, "Other", "Book")
    start = pd.to_datetime("02-01-2024", format=FinanceCSV.format)
    end = pd.to_datetime("09-01-2024", format=FinanceCSV.format)
    result = FinanceCSV.get_entries_by_date_range(start, end)
    assert len(result) == 1
    assert result.iloc[0]['Category'] == "Transport"

# Optionally, test the add() function with mocks for user input
@mock.patch("main.get_date", return_value="01-01-2024")
@mock.patch("main.get_amount", return_value=100)
@mock.patch("main.get_category", return_value="Food")
@mock.patch("main.get_description", return_value="Lunch")
def test_add_function(mock_desc, mock_cat, mock_amt, mock_date, tmp_path):
    test_csv = tmp_path / "test_finance_data.csv"
    FinanceCSV.csv_file = str(test_csv)
    FinanceCSV.initialize_csv()
    from main import add
    add()
    df = pd.read_csv(test_csv)
    assert len(df) == 1
    assert df.iloc[0]['Category'] == "Food"
