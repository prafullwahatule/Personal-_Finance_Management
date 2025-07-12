import os

input_file = r'c:\Users\prafu\OneDrive\Desktop\Personal Finance Management\finance_advisor\dashboard\static\mutual-fund-csv\mutual_fund_data.txt'
output_file = r'c:\Users\prafu\OneDrive\Desktop\Personal Finance Management\finance_advisor\dashboard\static\mutual-fund-csv\Angel One Mutual Fund.csv'

# Replace ; with ,
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(';', ',')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully replaced all ';' with ',' and saved to:", output_file)
