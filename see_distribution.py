from tools import *

def see_distribution_page():
	st.header('Database visualization')

	user_start_date, user_end_date = get_date_range()

	selected_categories = st.multiselect(
	'Select one or more categories to visualize',
	options=categories_list,
	default=categories_list
	)

	if st.button('See distribution'):
		plot_distribution(start_date=user_start_date,
						end_date=user_end_date,
						categories=selected_categories)


def plot_distribution(start_date:datetime.date, end_date:datetime.date, categories:list=[]):
	df = get_and_filter_df(start_date=start_date,
							end_date=end_date,
							categories=categories)
	category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
	fig, ax = plt.subplots(figsize=(8, 4))
	bars = ax.bar(category_totals.index, category_totals.values, color='mediumturquoise')

	for bar in bars:
		height = bar.get_height()
		ax.text(
			bar.get_x() + bar.get_width()/2,
			height,
			f'${height:,.2f}',
			ha ='center', va='bottom', color='azure', fontsize=4, fontweight='bold')
	ax.set_facecolor('dimgray')
	ax.yaxis.set_visible(False)
	plt.xticks(rotation=90, fontsize=5)
	st.pyplot(fig)