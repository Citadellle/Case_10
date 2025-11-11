import ru_local as ru
from datetime import datetime


def calculate_basic_stats(transactions_list: list) -> dict:
    '''
    This function calculates the total income and expenses,
    the remaining balance and the number of transactions.
    Then generates a dictionary from the received data.
    :param transactions_list:
    :return info:
    '''

    total_income = 0
    total_expenses = 0
    for transactions in transactions_list:
        if transactions[3] == ru.INCOME:
            total_income += transactions[1]
        else:
            total_expenses += transactions[1]

    balance = total_income - total_expenses

    transactions_quantity = len(transactions_list)

    info = {ru.INCOME: total_income,
            ru.EXPENSE: total_expenses,
            ru.BALANCE: balance,
            ru.TRANSACTIONS_QUANTITY: transactions_quantity}

    return info


def sort_by_category(transactions_list) -> dict:
    '''
    This function groups transactions into by categories
    :param transactions_list:
    :return transactions_by_category:
    '''

    transactions_by_category = {}

    for transactions in transactions_list:
        category = transactions[4]
        if transactions[3] != ru.INCOME:
            if category in transactions_by_category:
                transactions_by_category[category].append(transactions)
            else:
                transactions_by_category[category] = [transactions]

    return transactions_by_category


def calculate_by_category(transactions_list) -> dict:
    '''
    This function creates a dictionary with information
    for each category (key - category, value - information)
    :param transactions_list:
    :return category_info:
    '''

    category_info = {}
    total_expenses = calculate_basic_stats(transactions_list)[ru.EXPENSE]
    trans_by_category = sort_by_category(transactions_list)

    for category in trans_by_category:
        category_list = trans_by_category[category]

        total_sum = 0
        for transactions in category_list:
            total_sum += transactions[1]
            transactions_quantity = len(category_list)

        percent = round(total_sum / total_expenses, 2) * 100

        info = [total_sum, transactions_quantity, percent]
        category_info[category] = info

    return category_info


def sort_by_month(transactions_list) -> dict:
    '''
    This function groups transactions into by month
    :param transactions_list:
    :return trans_by_month:
    '''
    trans_by_month = {}

    for transactions in transactions_list:
        month_trans = datetime.strptime(transactions[0], '%Y-%m-%d').month

        if month_trans in trans_by_month:
            trans_by_month[month_trans].append(transactions)
        else:
            trans_by_month[month_trans] = [transactions]

    return trans_by_month


def analyze_by_time(transactions_list) -> dict:
    '''
    This function creates a dictionary with information
    for each month (key - month, value - information)
    :param transactions_list:
    :return month_info:
    '''
    month_info = {}
    trans_by_month = sort_by_month(transactions_list)

    for month in trans_by_month:
        month_list = trans_by_month[month]

        income = calculate_basic_stats(month_list)[ru.INCOME]
        expenses = calculate_basic_stats(month_list)[ru.EXPENSE]

        quantity_category = []
        category_list = []

        for transactions in month_list:
            category = transactions[4]
            if category in category_list:
                quantity_category[category_list.index(category)] += 1
            else:
                quantity_category.append(1)
                category_list.append(category)

        n = max(quantity_category)
        popular_categories = []
        for index_category in range(len(category_list)):
            if quantity_category[index_category] == n:
                popular_categories.append(category_list[index_category])

        info = {ru.INCOME: income,
                ru.EXPENSE: expenses,
                ru.POPULAR_CATEGORIES: popular_categories}

        month_info[month] = info

    return month_info