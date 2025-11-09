from tools import *

def add_transaction_page():
	st.header('Add transaction')

	# row 1
	space_1, _ = st.columns([1, 5])
	with space_1:
		user_transaction_type = st.selectbox('Transaction type', transaction_type_list)
		user_date = st.date_input("Date", datetime.date.today())

	# row 2
	space_4, space_5 = st.columns([2, 1])
	with space_4:
		user_description = st.text_input('Description (Do not use accents)')
	with space_5:
		user_amount = st.number_input('Amount', min_value=0.0)

	if user_transaction_type == 'Transference':
		# row 3
		space_6, space_7, _ = st.columns(3)
		with space_6:
			user_source_account = st.selectbox('Source account', accounts_list)
		with space_7:
			user_destination_account = st.selectbox('Destination account', accounts_list)
		transference = True
	elif user_transaction_type == 'Income':
		# row 3
		space_6, space_7, _ = st.columns(3)
		with space_6:
			user_category = st.selectbox('Category', income_categories_list)
		with space_7:
			user_account = st.selectbox('Account', accounts_list)
		transference = False
	else:
		# row 3
		space_6, space_7, _ = st.columns(3)
		with space_6:
			user_category = st.selectbox('Category', categories_list)
		with space_7:
			user_account = st.selectbox('Account', accounts_list)
		transference = False

	if st.button('Save transaction'):
		if transference:
			any_failure = add_transference_to_db(date=user_date,
												description=user_description,
												amount=user_amount,
												source_account=user_source_account,
												destination_account=user_destination_account)
		else:
			any_failure = add_transaction_to_db(date=user_date,
												description=user_description,
												amount=user_amount,
												transaction_type=user_transaction_type,
												account=user_account,
												category=user_category)
		if not(any_failure):
			st.success('Transaction saved!')

def add_transaction_to_db(date:datetime.date, description:str, amount:float, transaction_type:str, account:str, category:str):
	df, any_failure = open_db()
	if any_failure:
		st.error('Failure with database')
	else:
		next_index = df['Index'].max() + 1 # It does not work with the first index
		df.loc[len(df)] = {'Index': next_index,
							'Date': date,
							'Description': description,
							'Amount': amount,
							'TransactionType': transaction_type,
							'Account': account,
							'Category': category}
	any_failure = update_df(df)
	return any_failure

def add_transference_to_db(date:datetime.date, description:str, amount:float, source_account:str, destination_account:str):
	df, any_failure = open_db()
	if any_failure:
		st.error('Failure with database')
	else:
		next_index = df['Index'].max() + 1 # It does not work with the first index
		df.loc[len(df)] = {'Index': next_index,
							'Date': date,
							'Description': description,
							'Amount': amount,
							'TransactionType': 'Expense',
							'Account': source_account}
		next_index = df['Index'].max() + 1
		df.loc[len(df)] = {'Index': next_index,
							'Date': date,
							'Description': description,
							'Amount': amount,
							'TransactionType': 'Income',
							'Account': destination_account}
	any_failure = update_df(df)
	return any_failure