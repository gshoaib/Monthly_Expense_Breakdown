#https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#https://console.developers.google.com/apis/dashboard?project=soy-haven-217621&pageState=(%22duration%22:(%22groupValue%22:%22PT12H%22))
#https://gspread.readthedocs.io/en/latest/oauth2.html
#https://gspread.readthedocs.io/en/latest/user-guide.html
#https://docs.google.com/spreadsheets/d/1Yp64aBkfooPxUoaxUG6IDbFmhhv_kJIjgQz-kko5WTU/edit#gid=0

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# use creds to create a client to interact with the Google Drive API
#Step 1: Connect gspread to google sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#Step 2: Mapping Bank Reports
file3 = client.open("Spreadsheet name here").worksheet("Debit_card_data")
file2 = client.open("Spreadsheet name here").worksheet("Debit_card_data")
file1 = client.open("Spreadsheet name here").worksheet("Credit_card_data")
file4 = client.open("Spreadsheet name here").worksheet("Credit_card_data")

#Step 3: Run the Code
file1 = pd.DataFrame(file1.get_all_records())
file2 = pd.DataFrame(file2.get_all_records())
file3 = pd.DataFrame(file3.get_all_records())
file4 = pd.DataFrame(file4.get_all_records())


file1['Transaction Date'] = pd.to_datetime(file1['Transaction Date'])
file1['Post Date'] = pd.to_datetime(file1['Post Date'])
file1['Year_Month'] = file1['Transaction Date'].dt.strftime('%Y-%m')
file2['Posting Date'] = pd.to_datetime(file2['Posting Date'])
file2['Year_Month'] = file2['Posting Date'].dt.strftime('%Y-%m')
file3['Posting Date'] = pd.to_datetime(file3['Posting Date'])
file3['Year_Month'] = file3['Posting Date'].dt.strftime('%Y-%m')
file4['Transaction Date'] = pd.to_datetime(file4['Transaction Date'])
file4['Post Date'] = pd.to_datetime(file4['Post Date'])
file4['Year_Month'] = file4['Transaction Date'].dt.strftime('%Y-%m')

# Modify the Data Column Names so they all match
file1 = file1.rename(columns ={"Transaction Date": "Posting Date"})
# Remove all unused columns
file1 = file1.drop(columns=['Post Date', 'Category'])
file2 = file2.drop(columns=['Details', 'Balance'])
file3 = file3.drop(columns=['Details', 'Balance'])
file4 = file4.rename(columns ={"Transaction Date": "Posting Date"})
file4 = file4.drop(columns=['Post Date', 'Category'])

frames = [file1, file2, file3, file4]
f_data = pd.concat(frames) # Combines all the transaction reports together. 

findata_exp = f_data # Creating findata_exp to Focus on Expense Charges. Potentially linking to an Expense Table. 
findata_exp = findata_exp[findata_exp.Type != 'ACCT_XFER'] #Begining to filter out certain transactions 
findata_exp = findata_exp[findata_exp.Type != "ACH_CREDIT"]
findata_exp = findata_exp[findata_exp.Type != "Adjustment"]
findata_exp = findata_exp[findata_exp.Type != "Payment"]
findata_exp = findata_exp[findata_exp.Type != "QUICKPAY_CREDIT"]
findata_exp = findata_exp[findata_exp.Type != "QUICKPAY_DEBIT"]
findata_exp = findata_exp[findata_exp.Category1 != 'Ignore ']
#findata_exp = findata_exp[findata_exp.Type != "ATM"]

findata2_exp_group = findata_exp.groupby('Year_Month').sum().sort_values(by='Year_Month')
print(findata2_exp_group)

#Step 3: Monthly Expense Breakdown
FinData_Category_Mar = findata_exp.loc[findata_exp['Year_Month'] == '2021-03']
grouped_df_Mar = FinData_Category_Mar.groupby(['Category1'])[['Amount']].sum().reset_index()
grouped_df_Mar['Amount'] = grouped_df_Mar['Amount'].abs()
fig_Mar = px.pie(grouped_df_Mar, values='Amount', names='Category1', title='Expense Breakdown')
fig_Mar.show()

# Monthly Expense Line Graph
df = px.data.gapminder()
fig = px.line(grouped_df_lg, x='Year_Month', y='Amount', color='Category1',
        line_shape="spline", render_mode="svg")
fig.show()


