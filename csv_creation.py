import csv

column_names = ['Index',
				'Date',
				'Description',
				'Amount',
				'TransactionType',
				'Account',
				'Category']

file_name = 'finances_2025.csv'

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(column_names)