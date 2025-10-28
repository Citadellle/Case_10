import csv
import json
from datetime import datetime
from ru_local import *


def read_csv_file(filename: str) -> list:
    '''
    # 1. Открыть файл с помощью встроенной функции open()
    # 2. Прочитать все строки
    # 3. Разделить каждую строку на части по запятым
    # 4. Преобразовать в удобный формат (список словарей)
    # 5. Вернуть данные

    errors:
    FileNotFoundError
    if split(filename, sep='.')[-1] != 'csv'

    '''
    try:
        with open(filename, mode='r', encoding= 'utf-8') as file:
            if filename.split(sep='.')[-1] != 'csv':
                return ['File is not csv']
            csv_reader = csv.DictReader(file)
            return [lines for lines in csv_reader]
    except FileNotFoundError:
        return ['File is not found']


def read_json_file(filename: str) -> list:
    '''
    # 1. Импортировать модуль json
    # 2. Прочитать файл
    # 3. Использовать json.load() для преобразования
    # 4. Вернуть данные
    '''
    try:
        with open(filename, mode='r', encoding= 'utf-8') as file:
            if filename.split(sep='.')[-1] != 'json':
                return ['File is not json']
            json_reader = json.load(file)
        return list(json_reader['data'])
    except FileNotFoundError:
        return ['File is not found']


def import_financial_data(filename: str) -> list:
    '''
    # 1. Определить тип файла по расширению (.csv или .json)
    # 2. Вызвать соответствующую функцию чтения
    # 3. Проверить, что данные имеют правильную структуру
    # 4. Вернуть список транзакций в ЕДИНОМ ФОРМАТЕ (Формат - список списков)

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

    #if read_data[0] is not dict:
    #    return ['incorrect data format', type(read_data[0])]

    # Создаем пустые переменные для ключей
    k_amount = ''
    k_date = ''
    k_description = ''
    k_type = ''
    # Бегаем по первому элементу словаря, находим нужные нам ключи
    for need_keys in read_data[0].keys():
        if 'amount' in need_keys:
            k_amount = need_keys
        if 'date' in need_keys:
            k_date = need_keys
        if 'description' in need_keys:
            k_description = need_keys
        if 'type' in need_keys:
            k_type = need_keys

    #Проверка на отсутствие ключей
    #if k_type or k_date or k_category or k_amount == '':
    #    return ['data is not full', fr'keys {read_data[0].keys}']

    # Цикл для формирования списков списков
    exit_list = []
    for dictionary in read_data:
        inter_list = [dictionary[k_date], float(dictionary[k_amount]), dictionary[k_description], dictionary[k_type]]
        exit_list.append(inter_list)
    return exit_list




def create_categories() -> dict:
    """ 
    Creates a dictionary of categories: the key is the category name, 
    The value is a list of keywords.
    """
    return {
         "еда": ["пятерочка", "магнит", "продукты", "еда", "супермаркет", "добрянка", "мария-ра", "ярче", "мясо", "кондитерская", "пекарня", "овощи", "фрукты",  "окей", "дикси", "ярмарка", "фермер", "лавка"],
        "транспорт": ["метро", "автобус", "такси", "бензин", "аренда самоката", "ж/д", "билет", "дизель", "газ", "поезд", "электричка", "авиабилет", "аэрофлот", "велосипед", "газель"],
        "развлечения": ["кино", "атракцион", "выступление", "концерт", "театр", "выставка",  "боулинг", "квест", "игровая",],
        "питание в общественных местах": [ "ресторан", "кафе", "столовая", "закусочная", "кофейня", "пельменная", "шаурма", "чикен", "донер", "лаваш","чайхона"]
        "здоровье": ["аптека", "врач", "больница", "лекарства", "стоматология", "поликлиника", "анализы",  "стоматология", "зуб", "лечение", "медицин", "диагностика", "инвитро", "хеликс", "лаборатория", "очки", "линзы"],
        "одежда": ["одежда", "обувь", "wildberries", "ozon", "спортмастер", "zolla", "o'stin", "adidas", "Rieker", "виктор", "lacoste", "brand", "befree", "футболка", "штаны", "носки", "рубашка", "zara", "h&m", "bershka"],
        "быт": ["хозтовары", "бытовая техника", "мебель",  "порошок", "средство для стирки", "мыло", "шампунь", "гель для душа",  "зубная паста", "щётка", "бритва", "салфетки", "туалетная бумага", "бумага",
                "губки", "мочалка", "перчатки", "средство для посуды", "средство для унитаза", "освежитель", "аромат","отбеливатель"],
         "жильё": [ "аренда", "квартира", "коммунал", "электроэнергия", "вода", "газ", "отопление", "интернет", "wi-fi", "мтс", "билайн", "мегафон","домру", "ростелеком", "жкх", "управляющая компания", "ипотека",
                   "квартплата", "содержание жилья"],
        "образование": ["курсы", "школа", "университет", "онлайн-курсы", "колледж", "училище", "повышение квалификации", "обучение",  "вебинар", "учебник", "канцелярия", "канцтовары"],
        "переводы": ["перевод", "на карту", "qiwi", "сбер", "втб", "альфа", "т-банк", "газпромбанк", "россельхозбанк"]
    }


def categorize_transaction(description: str, categories: dict) -> str:
    """
    Reduce the description to lowercase
    Check if a keyword is included in the description.  
    If found, return the category. If you haven't found it, return "другое"
    """    
    description_lower = description.lower()
      
    for category, keywords in categories.items():
        if category == "доход":
            continue
        
        for keyword in keywords:
            if keyword in description_lower:
                return category


def categorize_all_transactions(transactions: list) -> list:
    """
    Accepts a list of transactions in the format:
        [[date, amount, description, type], ... ]
    
    Returns: [[date, amount, description, type, category], ... ]
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
    trans_by_month = sort_by_month(transactions)
    months_data = []

    for month_number in trans_by_month:
        month = trans_by_month[month_number]

        expenses_month_for_category = {}

        for transaction in month:
            category = transaction[4]
            expense = transaction[1]
            transaction_type = transaction[3]

            if transaction_type == 'расход':
                if category in expenses_month_for_category:
                    expenses_month_for_category[category] += expense
                else:
                    expenses_month_for_category[category] = expense
        
        months_data.append(expenses_month_for_category)


    expenses_per_category = {}
    for month in months_data:
        for category in month:
            expense_by_category = month[category]

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
    top_3_category_with_biggest_expenses = []
    for i in range(3):
        top_3_category_with_biggest_expenses.append(expenses_per_category_sorted[i][0])
    


    expense_by_month = []
    for month in months_data:
        expenses_per_month = sum(list(month.values()))
        expense_by_month.append(expenses_per_month)
        

    seasons = {
        'Зима': [12, 1, 2],
        'Весна': [3, 4, 5],
        'Лето': [6, 7, 8],
        'Осень': [9, 10, 11]
    }

    seasonal_data = {}
    i = 0
    for expense_by_month in expense_by_month:
        i += 1
        if i in seasons['Зима']:
            if 'Зима' in seasonal_data:
                seasonal_data['Зима'] += expense_by_month
            else:
                seasonal_data['Зима'] = expense_by_month
        elif i in seasons['Весна']:
            if 'Весна' in seasonal_data:
                seasonal_data['Весна'] += expense_by_month
            else:
                seasonal_data['Весна'] = expense_by_month
        elif i in seasons['Лето']:
            if 'Лето' in seasonal_data:
                seasonal_data['Лето'] += expense_by_month
            else:
                seasonal_data['Лето'] = expense_by_month
        else:
            if 'Осень' in seasonal_data:
                seasonal_data['Осень'] += expense_by_month
            else:
                seasonal_data['Осень'] = expense_by_month

    seasonal_data_sorted = sorted(seasonal_data.items(),
                                  key= lambda i: i[1])
    max_exp, max_exp_name = seasonal_data_sorted[-1][1], seasonal_data_sorted[-1][0]
    min_exp, min_exp_name = seasonal_data_sorted[0][1], seasonal_data_sorted[0][0]
    seasonal_patterns = (f'Наибольшие затраты наблюдаются в сезон {max_exp_name} и равны {max_exp}',
                         f'Наименьшие затраты наблюдаются в сезон {min_exp_name} и равны {min_exp}')


    max_exp_category = expenses_per_category_sorted[0]
    several_exp_category = expenses_per_category_sorted[len(expenses_per_category_sorted)//3]
    recommended_decrease = ((max_exp_category[1] - several_exp_category[1]) \
                            / max_exp_category[1]) * 100

    recommendations_for_planning = (f'Попробуйте сократить траты на {max_exp_category[0]} ' \
                                    f'на {round(recommended_decrease, 2)}%')

    return {
        'cредние затраты' : average_expenses_by_category_per_month,
        'cезонные закономерности' : seasonal_patterns,
        'cамые большие траты' : top_3_category_with_biggest_expenses,
        'рекомендации' : recommendations_for_planning
            }


def create_budget_template(analysis: dict) -> dict:
    savings = {}
    for month in analysis:
        info_month = analysis[month]
        income = info_month[INCOME]
        expense = info_month[EXPENSES]
        saving = income - expense

        savings[month] = saving

    return savings


def compare_budget_vs_actual(budget: dict) -> list:
    report = {}
    budget_compliance = True
    for month in budget:
        saving_month = budget[month]

        if saving_month < 0:
            report[month] = abs(saving_month)
            budget_compliance = False
    
    return list(report, budget_compliance)


def print_report(stats: list, category_stats: list, analysis: dict, budget: dict) -> None:
    print('=== ФИНАНСОВЫЙ ОТЧЕТ ===')

    print('ОСНОВНЫЕ ПОКАЗАТЕЛИ:',
          f'💰 Доходы: {stats[INCOME]} руб.',
          f'💸 Расходы: {stats[EXPENSES]} руб.',
          f'⚖️ Баланс: {stats[BALANCE]} руб.',
          f'Количество транзакций за год: {stats[TRANSACTIONS_QUANTITY]}',
          sep = '\n')
    
    print('РАСХОДЫ ПО КАТЕГОРИЯМ:',
          '',
          '',
          '',
          '',
          sep = '\n')
    
    print(f'Средние затраты по категориям, за месяц: {analysis['cредние затраты']}',
          f'Сезонные закономерности: {analysis['cезонные закономерности']}',
          f'Самые большие траты в категориях: {analysis['cамые большие траты']}',
          f'Рекомендации для планирования: {analysis['рекомендации']}',
          sep = '\n')

    if budget[1]:
        print('✅ Отлично! Вы укладываетесь в бюджет')
    else:
        print('❌ К сожалению, Вы не усложись в бюджет...')
        print('Номера месяцев, в которые Вы не уложились в бюджет:')
        for month in budget[0]:
            print(f'{month} месяц, превышение бюджета \
                   в размере {budget[0][month]} руб.')



def main():
    # 1. Роль 1: Импортируем данные.
    transactions = import_financial_data("test_data.csv")
    
    # 2. Роль 2: Классифицируем транзакции. 
    categorized_transactions = categorize_all_transactions(transactions)
    
    # 3. Роль 3: Анализируем статистику.
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)
    time_stats = analyze_by_time(categorized_transactions)
    
    #4. Роль 4: Планируем бюджет.
    analysis = analyze_historical_spending(categorized_transactions)
    budget = create_budget_template(time_stats)
    report_budget = compare_budget_vs_actual(budget)

    #Выводим результаты.
    print_report(stats, category_stats, analysis, report_budget)


if __name__ == '__main__':
    main()
