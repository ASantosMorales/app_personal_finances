from tools import *

def see_table_page():
	st.header('Database visualization')

	user_start_date, user_end_date = get_date_range()

	if st.button('See database range'):
		get_table_info(start_date=user_start_date,
						end_date=user_end_date)

def get_table_info(start_date:datetime.date, end_date:datetime.date):
	df = get_and_filter_df(start_date=start_date,
						end_date=end_date)

	st.dataframe(df.style.format({
			'Date': lambda x: x.strftime("%Y-%m-%d"),
			'Amount': lambda x: f'${x:,.2f}'}), hide_index=True)