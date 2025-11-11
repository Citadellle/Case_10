import ru_local as ru
import statistic as stat
import budget_category


def analyze_historical_spending(transactions: list) -> dict:
    '''
    Analyzes historical financial transactions and returns spending statistics.

    Args:
        transactions (list): List of transactions where each transaction is a list containing:
                            [amount, description, date, type, category]

    Returns:
        dict: Dictionary containing:
            - 'average costs': Average monthly expenses by category
            - 'seasonal patterns': Seasonal spending patterns (highest and lowest spending seasons)
            - 'biggest expenses': Top 3 spending categories
            - 'recommendations': Budget optimization recommendations
            - 'category data by month': Monthly spending data organized by category
    '''
    # Get transaction data by month. Data format:
    # {month number : [[first transaction], [second transaction], ...], }
    all_transactions_by_months = stat.sort_by_month(transactions)

    # Number of analyzed months
    number_of_months = len(all_transactions_by_months)

    # Process data for each month. Combine transaction data for same categories.
    # Dictionary with data converted to required format looks like:
    # {month number : {category_1 : expenses, category_2 : expenses, ...}, ...}
    months_data = {}
    for month_number in all_transactions_by_months:
        # Monthly transactions: [[first transaction], [second transaction], ...]
        month_data = all_transactions_by_months[month_number]

        expenses_month_for_categories = {}

        for transaction in month_data:
            expense_val = transaction[1]
            transaction_type = transaction[3]
            category = transaction[4]

            if transaction_type == ru.EXPENSE:
                if category in expenses_month_for_categories:
                    expenses_month_for_categories[category] += expense_val
                else:
                    expenses_month_for_categories[category] = expense_val

        months_data[month_number] = expenses_month_for_categories

    # Total expenses by categories for all time:
    # {category_1 : total_expenses, category_2 : total_expenses, ...}
    total_expenses_in_categories = {}
    for month in months_data:
        # Monthly data: {category_1 : expenses, category_2 : expenses, ...}
        month_data = months_data[month]

        for category in month_data:
            # Expenses in one category for one month
            expense_in_category = month_data[category]

            if category in total_expenses_in_categories:
                total_expenses_in_categories[category] += expense_in_category
            else:
                total_expenses_in_categories[category] = expense_in_category

    # Average monthly expenses by category:
    # {category_1 : average expenses, category_2 : average expenses, ...}
    average_expenses_by_category = {}
    for category in total_expenses_in_categories:
        average_expenses_by_category[category] = \
            round(total_expenses_in_categories[category] / number_of_months, 2)

    # Total expenses by categories sorted in descending order:
    # [(category_1 : expenses), (category_2 : expenses), ...]
    total_expenses_in_categories_sorted = sorted(total_expenses_in_categories.items(),
                                                 key=lambda i: i[1],
                                                 reverse=True)

    # 3 categories with highest expenses:
    # {category_1 : expenses, category_2 : expenses, category_3 : expenses}
    top_3_category = {}
    for i in range(3):
        category = total_expenses_in_categories_sorted[i][0]
        expense_val = total_expenses_in_categories_sorted[i][1]
        top_3_category[category] = expense_val

    # Total expenses for each month:
    # {month_1 : expenses, month_2 : expenses, ...}
    total_expenses_by_month = {}
    for month in months_data:
        month_data = months_data[month]
        expense_per_month = sum(list(month_data.values()))
        total_expenses_by_month[month] = expense_per_month

    seasons = {
        ru.WINTER: [12, 1, 2],
        ru.SPRING: [3, 4, 5],
        ru.SUMMER: [6, 7, 8],
        ru.AUTUMN: [9, 10, 11]
    }

    # Total expenses by seasons:
    # {Summer : expenses, Spring : expenses, ...}
    seasonal_data = {}
    for month in total_expenses_by_month:
        expense_by_month = total_expenses_by_month[month]
        if month in seasons[ru.WINTER]:
            if ru.WINTER in seasonal_data:
                seasonal_data[ru.WINTER] += expense_by_month
            else:
                seasonal_data[ru.WINTER] = expense_by_month
        elif month in seasons[ru.SPRING]:
            if ru.SPRING in seasonal_data:
                seasonal_data[ru.SPRING] += expense_by_month
            else:
                seasonal_data[ru.SPRING] = expense_by_month
        elif month in seasons[ru.SUMMER]:
            if ru.SUMMER in seasonal_data:
                seasonal_data[ru.SUMMER] += expense_by_month
            else:
                seasonal_data[ru.SUMMER] = expense_by_month
        else:
            if ru.AUTUMN in seasonal_data:
                seasonal_data[ru.AUTUMN] += expense_by_month
            else:
                seasonal_data[ru.AUTUMN] = expense_by_month

    # Total expenses by seasons sorted in descending order
    seasonal_data_sorted = sorted(seasonal_data.items(),
                                  key=lambda i: i[1],
                                  reverse=True)

    # Maximum expenses value, season name with this value
    max_exp, max_exp_name = seasonal_data_sorted[0][1], seasonal_data_sorted[0][0]
    # Minimum expenses value, season name with this value
    min_exp, min_exp_name = seasonal_data_sorted[-1][1], seasonal_data_sorted[-1][0]

    seasonal_patterns = [(max_exp_name, max_exp), (min_exp_name, min_exp)]

    # Category with maximum expenses: (category, expenses)
    max_exp_category = total_expenses_in_categories_sorted[0]
    # Category with average expenses: (category, expenses)
    several_exp_category = total_expenses_in_categories_sorted[len(total_expenses_in_categories_sorted) // 4]
    # Recommended expense reduction for category with maximum expenses
    recommended_decrease = ((max_exp_category[1] - several_exp_category[1]) \
                            / max_exp_category[1]) * 100

    recommendations_for_planning = (max_exp_category[0], round(recommended_decrease, 2))

    return {
        'average costs': average_expenses_by_category,
        'seasonal patterns': seasonal_patterns,
        'biggest expenses': top_3_category,
        'recommendations': recommendations_for_planning,
        'category data by month': months_data
    }


def create_budget_template(time_stats: dict, analysis: dict) -> dict:
    '''
    Creates a budget template based on historical spending analysis.

    Args:
        time_stats (dict): Time-based statistics containing income and expense data
        analysis (dict): Analysis data from analyze_historical_spending function

    Returns:
        dict: Budget allocation percentages for three categories:
            - 1: Essential expenses (housing, utilities, food, transport, health)
            - 2: Non-essential expenses (entertainment, clothing, education)
            - 3: Savings
    '''
    # Dictionary with expense data by categories by months:
    # {month number : {category_1 : expenses, category_2 : expenses, ...}, ...}
    months_data = analysis['category data by month']

    # time_stats - dictionary with data for each month:
    # {month_number : {income : value, expense : value, popular categories : list}, ...}

    # Savings for each month
    saving_dict = {}
    for month in time_stats:
        data_month = time_stats[month]
        income = data_month[ru.INCOME]
        expense = data_month[ru.EXPENSE]
        saving = income - expense

        saving_dict[month] = saving

    # Budget distribution across 3 consolidated categories
    budget_allocation_percentage = {1: 0, 2: 0, 3: 0}
    for month in months_data:
        month_data = months_data[month]

        for category in month_data:
            value = month_data[category]
            if category in budget_category.first_group:
                budget_allocation_percentage[1] += value
            if category in budget_category.second_group:
                budget_allocation_percentage[2] += value

        budget_allocation_percentage[3] += saving_dict[month]

    return budget_allocation_percentage


def compare_budget_vs_actual(budget: dict) -> bool:
    '''
    Compares actual budget allocation with recommended percentages.

    Args:
        budget (dict): Budget allocation dictionary with three categories:
                      - 1: Essential expenses percentage
                      - 2: Non-essential expenses percentage
                      - 3: Savings percentage

    Returns:
        bool: True if budget allocation is outside recommended ranges, False otherwise

    Recommended ranges:
        - Category 1 (Essentials): 45-55%
        - Category 2 (Non-essentials): 25-35%
        - Category 3 (Savings): 15-25%
    '''
    amount = sum(budget)
    shares = {}
    error = False

    for i in budget:
        shares[i] = round(budget[i] / amount, 2) * 100

    if shares[1] not in [i for i in range(45, 56)]:
        error = True
    if shares[2] not in [i for i in range(25, 36)]:
        error = True
    if shares[3] not in [i for i in range(15, 25)]:
        error = True

    return (error, shares)