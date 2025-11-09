from tools import *

def see_trend_page():
	st.header('Time series visualization')

	user_start_date, user_end_date = get_date_range()

	selected_accounts = st.multiselect(
	'Select one or more accounts to visualize',
	options=accounts_list,
	default=['Klar']
	)

	if st.button('See time series'):
		plot_trend(start_date=user_start_date,
				end_date=user_end_date,
				accounts=selected_accounts)


def plot_trend(start_date:datetime.date, end_date:datetime.date, accounts:list):
	df, any_failure = open_db()
	if any_failure:
		st.error('Failure with database')
	else:
		df = get_and_filter_df(start_date=start_date, 
							end_date=end_date)
		df_work = df[df['Account'].isin(accounts)].copy()
		df_work = df_work[['Date', 'Amount', 'TransactionType', 'Account']]
		df_work = df_work.sort_values('Date')
		df_work.loc[df_work['TransactionType'] == 'Expense', 'Amount'] *= -1
		series = []
		for account in accounts:
			df_copy = df_work[df_work['Account'] == account].copy()
			daily = df_copy.groupby('Date', as_index=False)['Amount'].sum().sort_values('Date')
			daily[f'{account} cumulative'] = daily['Amount'].cumsum()
			series.append(daily)

		fig, ax = plt.subplots(figsize=(8, 4))

		for serie in series:
			ax.plot(serie['Date'], serie[serie.columns[-1]], label=serie.columns[-1])
		ax.legend()
		ax.grid(linestyle='--', alpha=0.5)
		ax.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.8)
		ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
		plt.xticks(rotation=90, fontsize=8)
		plt.yticks(fontsize=8)
		st.pyplot(fig)