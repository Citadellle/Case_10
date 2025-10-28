def read_csv_file(filename: str) -> list:
    pass


def read_json_file(filename: str) -> list:
    pass


def import_financial_data(filename: str) -> list:
    pass




def create_categories() -> dict:
    """ 
    Creates a dictionary of categories: the key is the category name, 
    The value is a list of keywords.
    """
    return {
        "еда": ["пятерочка", "магнит", "продукты", "еда", "супермаркет", "добрянка"],
        "транспорт": ["метро", "автобус", "такси", "бензин", "яндекс.такси", "ж/д", "билет"],
        "развлечения": ["кино", "ресторан", "кафе", "концерт", "театр", "цирк", "доставка", "самокат"],
        "здоровье": ["аптека", "врач", "больница", "лекарства", "стоматология", "поликлиника"],
        "одежда": ["одежда", "обувь", "wildberries", "ozon"],
        "быт": ["хозтовары", "бытовая техника", "мебель"],
        "образование": ["курсы", "школа", "университет", "учебники", "онлайн-курсы"],
        "переводы": ["перевод", "на карту", "qiwi", "сбербанк онлайн", "tinkoff", "альфа"],
        "доход": ["зарплата", "пенсия", "стипендия", "доход", "возврат", "кэшбэк", "проценты"],
        "другое": []
    }




def categorize_transaction(description: str, categories: dict) -> str:
    """
    Reduce the description to lowercase
    Check if a keyword is included in the description.  
    If found, return the category. If you haven't found it, return "другое"
    """
    if not description or not isinstance(description, str):
        return "другое"
    
    desc_lower = description.lower()
    
    
    for category, keywords in categories.items():
        if category == "доход":
            continue
        if any(keyword in desc_lower for keyword in keywords):
            return category
    
    return "другое"




def categorize_all_transactions(transactions: list) -> list:
    """
    Accepts a list of transactions in the format:
        [ [date, amount, description, type], ... ]
    
    Returns: [ [date, amount, description, type, category], ... ]
    """
    categories = create_categories()
    result = []
    
    for trans in transactions:
        if not isinstance(trans, (list, tuple)) or len(trans) < 4:
            if isinstance(trans, (list, tuple)):
                result.append(list(trans) + ["ошибка"])
            else:
                result.append(["", 0.0, "", "", "ошибка"])
            continue
        
        date, amount, description, trans_type = trans[0], trans[1], trans[2], trans[3]
        
        if trans_type == "доход":
            category = "доход"
        else:
            category = categorize_transaction(description, categories)
        
        new_transaction = [date, amount, description, trans_type, category]
        result.append(new_transaction)
    
    return result





def calculate_basic_stats(transactions_list) -> dict:
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
        if transactions[3] == INCOME:
            total_income += transactions[1]
        else:
            total_expenses += transactions[1]

    balance = total_income - total_expenses

    transactions_quantity = len(transactions_list)

    info = {INCOME:total_income,
            EXPENSES:total_expenses,
            BALANCE:balance,
            TRANSACTIONS_QUANTITY:transactions_quantity}

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
        if transactions[3] != INCOME:
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
    total_expenses = calculate_basic_stats(transactions_list)[EXPENSES]
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
        month_trans = datetime.strptime(transactions[0],'%Y-%m-%d').month

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

        income = calculate_basic_stats(month_list)[INCOME]
        expenses = calculate_basic_stats(month_list)[EXPENSES]

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

        info = {INCOME:income,
                EXPENSES:expenses,
                POPULAR_CATEGORIES:popular_categories}

        month_info[month] = info

    return month_info






def analyze_historical_spending(transactions: list) -> dict:
    pass


def create_budget_template(analysis: dict) -> dict:
    pass


def compare_budget_vs_actual(budget: dict, actual_transactions: list) -> dict:
    pass


def print_report(stats: list, category_stats: list, budget: dict) -> None:
    pass



def main():
    # 1. Роль 1: Импортируем данные
    transactions = import_financial_data("my_money.csv")
    
    # 2. Роль 2: Классифицируем транзакции  
    categorized_transactions = categorize_all_transactions(transactions)
    
    # 3. Роль 3: Анализируем статистику
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)
    
    # 4. Роль 4: Планируем бюджет
    analysis = analyze_historical_spending(categorized_transactions)
    budget = create_budget_template(analysis)
    
    # Выводим результаты
    print_report(stats, category_stats, budget)
