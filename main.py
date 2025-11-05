import csv
import json
from datetime import datetime
import tqdm
import ru_local as ru


def read_csv_file(filename: str) -> list:
    import csv
    '''
    Function:
    1. Opens a file using the built-in open function
    2. Reads all lines
    3. Splits each line into parts by commas
    4. Converts it to a list of dictionaries and returns the data
    5. Checks the data for correctness

    errors:
    FileNotFoundError
    if split(filename, sep='.')[-1] != 'csv'

    check:
    right data format - list of dictionaries
    '''
    try:
        with (open(filename, mode='r', encoding='UTF-8') as file):
            # Check on correct file extension.
            if filename.split(sep='.')[-1] != 'csv':
                return ['File is not csv']
            csv_reader = csv.DictReader(file)
            result = [lines for lines in csv_reader]

            # Check on correctness.
            if not isinstance(result, list) or not all(isinstance(item, dict)
                                                       for item in result):
                return ['Invalid data format: expected list of dictionaries']

            return result
    # In case incorrect name.
    except FileNotFoundError:
        return ['File is not found']


def read_json_file(filename: str) -> list:
    import json
    '''
    Function:
    1. Imports the json module
    2. Reads a file
    3. Use json.load() to convert
    4. Returns a list of dictionaries
    
    errors:
    FileNotFoundError
    if split(filename, sep='.')[-1] != 'json'

    check:
    right data format - list of dictionaries
    '''
    try:
        with open(filename, mode='r', encoding='UTF-8') as file:
            if filename.split(sep='.')[-1] != 'json':
                return ['File is not json']
            json_reader = json.load(file)
            result = list(json_reader['data'])

            # Check on correctness.
            if not isinstance(result, list) or not all(isinstance(item, dict)
                                                       for item in result):
                return ['Invalid data format: expected list of dictionaries']

            return result

    # In case incorrect name.
    except FileNotFoundError:
        return ['File is not found']


def import_financial_data(filename: str) -> list:
    import tqdm
    '''
    Function:
    1. Determine the file type by extension (.csv or .json)
    2. Call the appropriate read function
    3. Check that the data has the correct structure
    4. Return a list of transactions in a list of lists format

        "date": "2024-01-15",
        "amount": -1500.50,
        "description": "Продукты в Пятерочке",
        "type": "расход"

        "date": "2024-01-10",
        "amount": 50000.00,
        "description": "Зарплата",
        "type": "доход"
    '''

    if filename.split(sep='.')[-1] == 'json':
        read_data = read_json_file(filename)
    elif filename.split(sep='.')[-1] == 'csv':
        read_data = read_csv_file(filename)
    else:
        return ['unknown data format']

    # Create empty variables for keys.
    k_amount = ''
    k_date = ''
    k_description = ''
    # We run through the first element of the dictionary,
    # finding the keys we need.
    for need_keys in read_data[0].keys():
        if 'amount' in need_keys:
            k_amount = need_keys
        if 'date' in need_keys:
            k_date = need_keys
        if 'description' in need_keys:
            k_description = need_keys

    # Loop for generating lists of lists.
    exit_list = []

    # Use tqdm for printing status bar.
    for dictionary in tqdm.tqdm(read_data):
        inter_list = [dictionary[k_date], float(dictionary[k_amount]),
                    dictionary[k_description]]
        if str(dictionary[k_amount])[0] == '-':
            inter_list += ['расход']
        else:
            inter_list += ['доход']
        exit_list.append(inter_list)

    return exit_list


def create_categories() -> dict:
    """
    Creates a dictionary of categories: the key is the category name,
    The value is a list of keywords.
    """
    return {
        "еда": ["пятерочка", "магнит", "продукты", "еда", "супермаркет", "добрянка", "мария-ра", "ярче", "мясо",
                "кондитерская", "пекарня", "овощи", "фрукты", "окей", "дикси", "ярмарка", "фермер", "лавка"],
        "транспорт": ["метро", "автобус", "такси", "бензин", "аренда самоката", "ж/д", "билет", "дизель", "газ",
                      "поезд", "электричка", "авиабилет", "аэрофлот", "велосипед", "газель"],
        "развлечения": ["кино", "атракцион", "выступление", "концерт", "театр", "выставка", "боулинг", "квест",
                        "игровая", ],
        "питание в общественных местах": ["ресторан", "кафе", "столовая", "закусочная", "кофейня", "пельменная",
                                          "шаурма", "чикен", "донер", "лаваш", "чайхона"],
        "здоровье": ["аптека", "врач", "больница", "лекарства", "стоматология", "поликлиника", "анализы",
                     "стоматология", "зуб", "лечение", "медицин", "диагностика", "инвитро", "хеликс", "лаборатория",
                     "очки", "линзы"],
        "одежда": ["одежда", "обувь", "wildberries", "ozon", "спортмастер", "zolla", "o'stin", "adidas", "Rieker",
                   "виктор", "lacoste", "brand", "befree", "футболка", "штаны", "носки", "рубашка", "zara", "h&m",
                   "bershka"],
        "быт": ["хозтовары", "бытовая техника", "мебель", "порошок", "средство для стирки", "мыло", "шампунь",
                "гель для душа", "зубная паста", "щётка", "бритва", "салфетки", "туалетная бумага", "бумага",
                "губки", "мочалка", "перчатки", "средство для посуды", "средство для унитаза", "освежитель", "аромат",
                "отбеливатель"],
        "жильё": ["аренда", "квартира", "коммунал", "электроэнергия", "вода", "газ", "отопление", "интернет", "wi-fi",
                  "мтс", "билайн", "мегафон", "домру", "ростелеком", "жкх", "управляющая компания", "ипотека",
                  "квартплата", "содержание жилья"],
        "образование": ["курсы", "школа", "университет", "онлайн-курсы", "колледж", "училище", "повышение квалификации",
                        "обучение", "вебинар", "учебник", "канцелярия", "канцтовары"],
        "переводы": ["перевод", "на карту", "qiwi", "сбер", "втб", "альфа", "т-банк", "газпромбанк", "россельхозбанк"]
    }


def categorize_transaction(description: str, categories: dict) -> str:
    '''
    Reduce the description to lowercase
    Check if a keyword is included in the description.
    If found, return the category. If you haven't found it, return 'другое'
    '''
    description_lower = description.lower()

    for keyword in categories.items():
        if keyword in description_lower:
            return
    # If code didn't find category.
    else:
        return 'другое'


def categorize_all_transactions(transactions: list) -> list:
    '''
    Accepts a list of transactions in the format:
        [[date, amount, description, type], ... ]

    Returns: [[date, amount, description, type, category], ... ]
    '''
    categories = create_categories()
    result = []

    # Add in lists of list category item
    for trans in transactions:
        date, amount, description, trans_type = (trans[0], trans[1], trans[2],
                                                 trans[3])
        if trans_type == ru.INCOME:
            continue
        category = categorize_transaction(description, categories)

        new_transaction = [date, amount, description, trans_type, category]
        result.append(new_transaction)

    return result


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
    trans_by_month = sort_by_month(transactions)
    months_data = {}

    for month_number in trans_by_month:
        month_data = trans_by_month[month_number]

        expenses_month_for_category = {}

        for transaction in month_data:
            category = transaction[4]
            expense = transaction[1]
            transaction_type = transaction[3]

            if transaction_type == ru.INCOME:
                if category in expenses_month_for_category:
                    expenses_month_for_category[category] += expense
                else:
                    expenses_month_for_category[category] = expense
        
        months_data[month_number] = expenses_month_for_category


    expenses_per_category = {}
    for month in months_data:
        month_data = months_data[month]

        for category in month_data:
            expense_by_category = month_data[category]

            if category in expenses_per_category:
                expenses_per_category[category] += expense_by_category
            else:
                expenses_per_category[category] = expense_by_category
    

    average_expenses_by_category_per_month = {}
    for category in expenses_per_category:
        average_expenses_by_category_per_month[category] = \
            round(expenses_per_category[category] / 12, 2)
        
    
    expenses_per_category_sorted = sorted(expenses_per_category.items(),
                                          key= lambda i: i[1],
                                          reverse= True)
    top_3_category = []
    for i in range(3):
        top_3_category.append(expenses_per_category_sorted[i][0])
    


    expenses_by_month = []
    for month in months_data:
        month_data = months_data[month]
        expense_per_month = sum(list(month_data.values()))
        expenses_by_month.append(expense_per_month)
        

    seasons = {
        'winter': [12, 1, 2],
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'autumn': [9, 10, 11]
    }

    seasonal_data = {}
    i = 0
    for expense_by_month in expenses_by_month:
        i += 1
        if i in seasons['winter']:
            if 'winter' in seasonal_data:
                seasonal_data['winter'] += expense_by_month
            else:
                seasonal_data['winter'] = expense_by_month
        elif i in seasons['spring']:
            if 'spring' in seasonal_data:
                seasonal_data['spring'] += expense_by_month
            else:
                seasonal_data['spring'] = expense_by_month
        elif i in seasons['summer']:
            if 'summer' in seasonal_data:
                seasonal_data['summer'] += expense_by_month
            else:
                seasonal_data['summer'] = expense_by_month
        else:
            if 'autumn' in seasonal_data:
                seasonal_data['autumn'] += expense_by_month
            else:
                seasonal_data['autumn'] = expense_by_month

    seasonal_data_sorted = sorted(seasonal_data.items(),
                                  key= lambda i: i[1])
    max_exp, max_exp_name = seasonal_data_sorted[-1][1], seasonal_data_sorted[-1][0]
    min_exp, min_exp_name = seasonal_data_sorted[0][1], seasonal_data_sorted[0][0]
    seasonal_patterns = (f'{ru.pr_season_pat_high_costs} {max_exp_name} {ru.pr_season_pat_equal} {max_exp}',
                         f'{ru.pr_season_pat_small_costs} {min_exp_name} {ru.pr_season_pat_equal} {min_exp}')


    max_exp_category = expenses_per_category_sorted[0]
    several_exp_category = expenses_per_category_sorted[len(expenses_per_category_sorted)//2]
    recommended_decrease = ((max_exp_category[1] - several_exp_category[1]) \
                            / max_exp_category[1]) * 100

    recommendations_for_planning = (f'{ru.PR_RECOMMEND_PLAN} {max_exp_category[0]} ' \
                                    f'{ru.BY} {round(recommended_decrease, 2)}%')

    return {
        'average costs' : average_expenses_by_category_per_month,
        'seasonal patterns' : seasonal_patterns,
        'biggest expenses' : top_3_category,
        'recommendations' : recommendations_for_planning,
        'category data by month' : months_data
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
    months_data = analysis['category data by month']

    saving_dict = {}
    for month in time_stats:
        info_month = time_stats[month]
        income = info_month['income']
        expense = info_month[ru.INCOME]
        saving = income - expense

        saving_dict[month] = saving
    
    budget_allocation_percentage = {1: 0, 2: 0, 3: 0}
    for month in months_data:
        month_data = months_data[month]
        
        for category in month_data:
            data = month_data[category]
            if category in ['жилье', 'быт', 'еда', 'транспорт', 'здоровье']:
                budget_allocation_percentage[1] += data
            if category in ['развлечения', 'одежда', 'образование']:
                budget_allocation_percentage[2] += data

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

    return error

def print_report(stats: list, 
                 category_stats: list,
                 time_stats: list,
                 analysis: dict, 
                 budget: dict
                 ) -> None:
    '''
    Beautiful design and print of analyzed data.
    '''

    print(ru.PR_FINANCIAL_REPORT)

    print(ru.PR_KEY_INDICATORS,
          f'{ru.PR_INCOME} {stats[ru.INCOME]} {ru.PR_RUB}',
          f'{ru.PR_EXPENSE}: {stats[ru.EXPENSE]} {ru.PR_RUB}',
          f'{ru.PR_BALANCE} {stats[ru.BALANCE]} {ru.PR_RUB}',
          f'{ru.PR_NUM_TRANS} {stats[ru.TRANSACTIONS_QUANTITY]}',
          sep = '\n')
    
    print(ru.PR_CATEGORY_EXPENSES)
    for category in category_stats:
        print(f'{ru.PR_CATEGORY} {category}')
        print(f'{ru.PR_EXPENSES}: {category_stats[category][0]}',
              f'{ru.PR_TRANSACTION_COUNT}: {category_stats[category][1]}',
              f'{ru.PR_PERCENT_OF_TOTAL}: {category_stats[category][2]}',
              sep='\n')
        
    print(ru.PR_MONTHLY_EXPENSES)
    for month in time_stats:
        print(f'{ru.PR_MONTH} {month}')
        print(f'{ru.PR_INCOME}: {time_stats[month][ru.INCOME]}',
              f'{ru.PR_EXPENSES}: {time_stats[month][ru.INCOME]}',
              f'{ru.PR_POPULAR_CATEGORIES}: {time_stats[month][ru.POPULAR_CATEGORIES]}',
              sep='\n')
    
    print(ru.PR_HISTORICAL_ANALYSIS)
    print(f'{ru.PR_AVERAGE_COSTS}: {analysis['average costs']}',
          f'{ru.PR_SEASONAL_PATTERNS}: {analysis['seasonal patterns']}',
          f'{ru.PR_BIGGEST_EXPENSES}: {analysis['biggest expenses']}',
          f'{ru.PR_RECOMMENDATIONS}: {analysis['recommendations']}',
          sep='\n')

    print(ru.PR_BUDGET,
      ru.PR_BUDGET_DISTRIBUTION,
      ru.PR_BUDGET_ESSENTIALS,
      ru.PR_BUDGET_LIFESTYLE,
      ru.PR_BUDGET_SAVINGS,
      sep='\n')
                     
    if budget:
        print(ru.PR_BUDGET_SUCCESS)
    else:
        print(ru.PR_BUDGET_FAILURE)



def main():
    '''
    The main function of the program is the accounting of income, expenses, analysis and budget planning.
    
    The function performs a sequence of actions according to 4 roles:
    1. Imports the data file and brings it to a format convenient for processing
    2. Processes the received data and assigns a category to each expense transaction
    3. Performs basic data analysis: total income, total expenses, balance, number of transactions. Detailed analysis by month and category.
    4. Performs a detailed analysis of the data: average expenses, seasonal patterns, categories with the largest expenses. Output of recommendations for the user. Calculation of the recommended budget.
    
    
    Functions used:
    - import_financial_data(): importing data and converting it to a format convenient for processing.
    
    - categorize_all_transactions(): Transaction analysis and categorization.
    
    - calculate_basic_stats(): calculation of total income, total expense, balance, number of transactions.
    - calculate_by_category(): Calculates the amount of expenses, the number of transactions, and the percentage of total expenses for each category.
    - analyze_by_time(): Calculates the amount of expenses, the number of transactions, and the percentage of total expenses for each month.
    
    - analyze_historical_spending(): calculation of average monthly expenses, identification of seasonal patterns, identification of 3 categories with the largest expenses, return of recommendations for planning.
    - create_budget_template(): calculating and returning savings, returning the budget template.
    - compare_budget_vs_actual(): determination of user satisfaction in the budget and return of data on penalties to the budget.
    
    - print_report(): beautiful design and return of analyzed data.
    '''
    
    # 1. Role 1: Importing data.
    transactions = import_financial_data(input('enter file name -->'))
    
    #2. Role 2: Classify transactions.
    categorized_transactions = categorize_all_transactions(transactions)
    
    # 3. Role 3: Analyzing statistics.
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)
    time_stats = analyze_by_time(categorized_transactions)
    
    #4. Role 4: Budget planning.
    analysis = analyze_historical_spending(categorized_transactions)
    budget = create_budget_template(time_stats, analysis)
    report_budget = compare_budget_vs_actual(budget)

    #We display the results.
    print_report(stats, category_stats, time_stats, analysis, report_budget)


if __name__ == '__main__':
    main()
