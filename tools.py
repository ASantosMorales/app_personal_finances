import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick 
import datetime

csv_file = '/Users/albertosantosmorales/Documents/Personal/finanzas/app/data/finances_2025.csv'

main_options_list = ['Add transaction',
					'See categories distribution',
					'See table',
					'See trend']

transaction_type_list = ['Income',
						'Expense',
						'Transference']

accounts_list = ['BBVA debit',
				'BanRegio debit',
				'Klar',
				'Nu',
				'BBVA credit',
				'BanRegio credit',
				'CETES',
				'GBM',
				'Cash']

categories_list = ['Assurance',
				'Clothes and shoes',
				'Doctor',
				'Donations',
				'Entrepreneurship',
				'Fuel and car',
				'Groceries and food',
				'Home equipment',
				'Home services',
				'Leisure and Pleasure',
				'Medecins',
				'Patrimony',
				'Personal care',
				'Pets',
				'Rent',
				'School',
				'Suscriptions',
				'Tech and equipment',
				'Travels']

income_categories_list = ['Payment',
						'Other incomes']

def page_setup():
	# --- Basic page config ---
	st.set_page_config(
		page_title="Expense Tracker",
		layout="wide",
	)

	# --- Main area ---
	st.title("Finance Control")

	# --- Sidebar (left banner) ---
	st.sidebar.title("Control de gastos")

def user_options():
	menu_option = st.sidebar.radio('Options',
		(
			main_options_list
		)
	)
	return menu_option

def open_db():
	df = None
	any_failure = False
	try:
		df = pd.read_csv(csv_file)
	except FileNotFoundError:
		any_failure = True
		raise FileNotFoundError(f'File {csv_file} not found.')
	except pd.errors.EmptyDataError:
		any_failure = True
		raise ValueError(f'File {csv_file} is empty or invalid.')
	except Exception as e:
		any_failure = True
		raise RuntimeError(f'Unexpected error while opening {csv_file}: {e}')
	return df, any_failure

def update_df(df:pd.DataFrame):
	any_failure = False
	try:
		df.to_csv(csv_file, index=False, encoding='utf-8')
	except PermissionError:
		any_failure = True
		raise PermissionError(f'File cannot be write {csv_file}')
	except OSError as e:
		any_failure = True
		raise OSError(f'System error with {csv_file}: {e}')
	except Exception as e:
		any_failure = True
		raise RuntimeError(f'Unexpected error with {csv_file}: {e}')
	return any_failure

def get_date_range():
	space_1, _, space_2, _, _ = st.columns(5)
	with space_1:
		user_start_date = st.date_input("Start date", datetime.datetime.strptime('2025-08-01', '%Y-%m-%d').date())
	with space_2:
		user_end_date = st.date_input("End date", datetime.date.today())
	return user_start_date, user_end_date

def get_and_filter_df(start_date:datetime.date, end_date:datetime.date, categories:list=[]):
	df_filtered = None
	df, any_failure = open_db()
	if any_failure:
		st.error('Failure with database')
	else:
		#Convert "Date" column to date
		df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
		mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
		df_filtered = df.loc[mask]
		if len(categories) > 0:
			df_filtered = df_filtered[df_filtered['Category'].isin(categories)]
	return df_filtered
