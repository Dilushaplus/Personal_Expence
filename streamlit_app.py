import streamlit as st
import pandas as pd
import os

st.title("Personal Expense Tracker")

csv_file = "finance_data.csv"
columns = ['Date', 'Amount', 'Category', 'Description']

# Initialize CSV if not exists
def initialize_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=columns)
        df.to_csv(csv_file, index=False)

initialize_csv()

# Add new transaction
with st.form("Add Transaction"):
    date = st.date_input("Date")
    amount = st.number_input("Amount")
    category = st.selectbox("Category", ["Income", "Expense"])
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add")
    if submitted:
        df = pd.read_csv(csv_file)
        new_entry = {
            'Date': date.strftime('%d-%m-%Y'),
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("Entry added successfully!")

# Show all transactions
df = pd.read_csv(csv_file)
st.subheader("All Transactions")
st.dataframe(df)

# Plot income and expense
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
df = df.dropna(subset=['Date'])
df = df.sort_values('Date')
income = df[df['Category'] == 'Income'].groupby('Date')['Amount'].sum()
expense = df[df['Category'] == 'Expense'].groupby('Date')['Amount'].sum()
st.subheader("Daily Income and Expense")
st.line_chart(pd.DataFrame({'Income': income, 'Expense': expense}))
