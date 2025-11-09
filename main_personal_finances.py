from tools import *
from add_transaction import add_transaction_page
from see_table import see_table_page
from see_distribution import see_distribution_page
from see_trend import see_trend_page

def main():
	page_setup()
	user_option = user_options()
	if user_option == 'Add transaction':
		add_transaction_page()
	elif user_option == 'See table':
		see_table_page()
	elif user_option == 'See categories distribution':
		see_distribution_page()
	elif user_option == 'See trend':
		see_trend_page()

if __name__ == '__main__':
    main()