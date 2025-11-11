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


def inter_list_en(dictionary: dict, k_date: str, k_amount: str,
                  k_description: str, k_category: str) -> list:
    from googletrans import Translator
    translator = Translator()
    inter_list = [dictionary[k_date], float(dictionary[k_amount]),
                  translator.translate(dictionary[k_description],
                                       dest='ru').text]
    if str(dictionary[k_amount])[0] == '-':
        inter_list += ['расход']
    else:
        inter_list += ['доход']
    # Add category information.
    inter_list.append(translator.translate(dictionary[k_category],
                                           dest='ru').text)
    return inter_list


def import_financial_data(filename: str) -> list:
    import time
    import tqdm
    from googletrans import Translator
    import ru_local as ru
    '''
    Function:
    1. Determine the file type by extension (.csv or .json)
    2. Call the appropriate read function
    3. Check that the data has the correct structure
    4. Return a list of transactions in a list of lists format
    5. If dataset is English, function take description information
    from dataset.
    
    input data example:
    
        "date": "2024-01-15",
        "amount": -1500.50,
        "description": "Продукты в Пятерочке",
        "type": "расход"


        "date": "2024-01-10",
        "amount": 50000.00,
        "description": "Зарплата",
        "type": "доход"
    
    exit data example (lang='en'):
    ['2024-06-11T10:37:22', -54.23, 
    'Покупка продуктов FreshMart - еженедельные поставки', 
    'расход', 'супермаркет']
    
    exit data example (lang='ru'):
    ['2024-01-18', -780.9, 'Продукты в Магните', 'расход']
    ================================
    
    !Notice!
    please, for correct work this function, use this version of googletrans:
    Name: googletrans
    Version: 4.0.0rc1
    Summary: Free Google Translate API for Python.
    Home-page: https://github.com/ssut/py-googletrans
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

    k_category = ''
    # We run through the first element of the dictionary,
    # finding the keys we need.
    for need_keys in read_data[0].keys():
        if 'amount' in need_keys:
            k_amount = need_keys
        if 'date' in need_keys:
            k_date = need_keys
        if 'description' in need_keys:
            k_description = need_keys
        if 'category' in need_keys:
            k_category = need_keys

    # Loop for generating lists of lists.
    exit_list = []
    # Language check. If it's English, we translate it on Russian.
    # Need to initialize an instance of Translator.
    translator = Translator()
    if translator.detect(read_data[0][k_description]).lang != 'ru':
        print(ru.PROGRESS_BAR_EN)
        # Use tqdm for printing status bar.
        for dictionary in tqdm.tqdm(read_data):
            try:
                exit_list.append(inter_list_en(dictionary, k_date, k_amount,
                                               k_description, k_category))
            # If Translator have to many request error.
            except AttributeError:
                time.sleep(5)
                print('Too many request\'s on Google translate server.'
                      '5 seconds pause.')
                exit_list.append(inter_list_en(dictionary, k_date, k_amount,
                                               k_description, k_category))

    else:
        print(ru.PROGRESS_BAR_RU)
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


lst = import_financial_data('test_data.csv')
print(lst)



                      
def create_categories() -> dict:
    """
    Creates a dictionary of categories: the key is the category name,
    The value is a list of keywords.
    """
    return {
        "еда": ["пятерочка", "магнит", "продукты", "еда", "супермаркет",
 "добрянка",  "мария-ра", "ярче", "мясо", "кондитерская", "пекарня",
 "овощи", "фрукты", "окей", "дикси", "ярмарка", "фермер", "лавка",
"Ашан", "Лента", "Перекресток", "ВкусВилл", "Глобус", "Светофор",
"колбаса", "сыр", "молоко", "хлеб", "масло", "яйца", "чай", "кофе",
"сахар", "соль", "специи", "крупы", "макароны", "консервы",
"полуфабрикаты", "соусы", "напитки", "сок", "вода", "алкоголь",
"пицца", "суши", "бургер", "салат", "стейк", "рыба", "курица", "торт",
"пирожное", "конфеты", "шоколад", "чипсы", "орехи", "мороженое", 
"Бристоль", "Красное и Белое", "Самокат", "Яндекс.Еда", "Delivery Club",
"Сбермаркет", "Впрок", "выпечка", "ингредиенты", "рецепт"],
        "транспорт": ["метро", "автобус", "такси", "бензин",
 "аренда самоката", "ж/д","билет", "дизель", "газ", "поезд",
 "электричка", "авиабилет", "аэрофлот", "велосипед", "газель",
"каршеринг", "платная дорога", "парковка", "автомойка", "шиномонтаж",
"автосервис", "техосмотр", "страховка авто", "эвакуатор", "бензовоз",
    "проездной", "автовокзал", "автостанция", "заправка", "азс",
"автобусный тур", "аренда авто", "такси Uber", "Яндекс Такси", "Ситимобил",
"чартер","вокзал", "порт", "аэропорт", "стоянка",  "запчасти", "автоэлектрик",
"кузовной ремонт", "балансировка колес", "замена масла", "тонировка стекол",
"диагностика двигателя","штраф ГИБДД", "водительское удостоверение", "СТС", "ПТС"],
        "развлечения": ["кино", "атракцион", "выступление", 
"концерт", "театр", "выставка", "боулинг", "квест", "игровая", "парк",
 "зоопарк", "музей", "галерея", "аквапарк", "каток", "караоке", "бильярд",
"сауна", "баня", "спа", "массаж", "бассейн", "отдых", "путешествие", "тур",
"экскурсия", "билеты", "видео", "музыка", "фестиваль", "праздник", "конкурс",
"игры", "парки аттракционов",  "клуб", "бар", "караоке-бар", "кальянная",
"библиотека","дискотека", "стендап", "цирк", "дельфинарий", "планетарий", 
"премьера", "фестиваль", "салют", "карнавал", "хеллоуин", "новый год",
"день рождения", "юбилей", "детский праздник","поход", "рыбалка", "охота",
"дайвинг", "снорклинг", "альпинизм", "скалолазание", "сплав", "пейнтбол",
"лазертаг", "картинг", "онлайн-кинотеатр", "подписка", "стриминг", "игры онлайн"],
        "здоровье": ["аптека", "врач", "больница", "лекарства", 
"стоматология", "поликлиника", "анализы", "стоматология",
 "зуб", "лечение", "медицин",  "диагностика", "инвитро",
 "хеликс", "лаборатория",  "очки", "линзы", "витамины", "бады",
"медицинская техника", "массажер", "бандаж", "ортез", "пластика",
"косметолог", "санаторий", "реабилитация", "вакцинация", "страховка дмс",
"скорая помощь", "медсестра", "доктор", "медосмотр", "клиника", "реабилитация",
"спортивная медицина", "гомеопатия", "терапевт", "педиатр", "хирург", "офтальмолог",
"гинеколог", "уролог", "кардиолог", "невролог", "эндокринолог", "аллерголог",
"дерматолог", "психолог", "психотерапевт", "логопед", "вакцина", "прививка", "узи",
"рентген", "мрт", "кт", "массаж", "физиотерапия", "иглоукалывание", "мануальная терапия",
"протезирование", "ортодонтия", "брекеты", "отбеливание зубов", "эпиляция", "шугаринг", 
"пилинг", "чистка лица", "ботокс", "филлеры", "пластический хирург", "ингалятор",
"тонометр", "глюкометр", "термометр", "грелка", "компресс", "пластырь", "бинт", "вата",
"йод", "зеленка", "перекись водорода"],
        "одежда": ["одежда", "обувь", "wildberries", "ozon",
 "спортмастер", "zolla", "o'stin", "adidas", "Rieker", "виктор",
 "lacoste", "brand", "befree", "футболка", "штаны", "носки",
 "рубашка", "zara", "h&m", "bershka", "куртка", "пальто", "платье",
"юбка", "джинсы", "кофта", "свитер", "толстовка", "брюки", "шорты",
"купальник", "нижнее белье", "пижама", "халат", "костюм", "ботинки",
"сапоги", "кроссовки", "туфли", "босоножки", "сланцы", "тапки",
"аксессуары", "сумка", "ремень", "перчатки", "шапка", "шарф", "очки",
"зонт", "украшения", "серьги", "кольцо", "браслет", "ткани", "фурнитура",
"шить", "ателье", "ремонт одежды", "химчистка", "распродажа", "стилист",
"сумка", "перчатки", "шляпа", "обувь", "пуховик", "жилет", "комбинезон",
"боди", "топ", "блузка", "водолазка", "леггинсы", "шорты", "комбинезон",
"корсет", "пеньюар","классика", "спорт", "кэжуал", "винтаж", "этно", "милитари",
"рок", "панк", "гламур", "хлопок", "шерсть", "шелк", "лен", "синтетика", "кожа",
"замша", "джинс", "вельвет", "бархат", "XS", "S", "M", "L", "XL", "XXL", "plus size",
"детская одежда", "подростковая одежда", "одежда для беременных"],
        "быт": ["хозтовары", "бытовая техника", "мебель",
 "порошок", "средство для стирки", "мыло", "шампунь",
"гель для душа", "зубная паста", "щётка", "бритва","салфетки",
"туалетная бумага", "бумага","губки", "мочалка", "перчатки",
"средство для посуды", "средство для унитаза", "освежитель", "аромат",
"отбеливатель", "пылесос", "утюг", "чайник", "стиральная машина", "холодильник",
"плита","микроволновка", "телевизор", "компьютер", "телефон", "наушники",
"зарядка", "батарейки", "флешка", "кабель", "посуда", "сковорода", "кастрюля",
"тарелка", "чашка", "ложка", "вилка", "нож", "полотенце", "постельное белье",
"подушка", "одеяло", "плед", "шторы", "жалюзи", "ковёр", "кресло", "стол", "стул",
"зеркало", "лампа", "батарейки", "семена", "рассада", "удобрения", "инструменты",
"садовая мебель", "грунт", "декор", "средства для уборки", "диспенсер", "сушилка",
"холодильник", "освежитель воздуха", "пылесос", "садовый инвентарь","электроника",
 "фен", "плойка", "триммер", "эпилятор", "весы", "швейная машинка", "оверлок",
"морозильник", "духовка", "кофемашина", "блендер", "миксер", "мясорубка",
"соковыжималка", "хлебопечка", "мультиварка", "блендер", "робот-пылесос",
"игровая консоль", "принтер", "сканер", "проектор"],
        "жильё": ["аренда", "квартира", "коммунал", "электроэнергия",
 "вода", "газ", "отопление", "интернет", "wi-fi", "мтс", "билайн",
 "мегафон", "домру", "ростелеком", "жкх", "управляющая компания",
 "ипотека",   "квартплата", "содержание жилья", "домофон", "охрана", "консьерж",
"вывоз мусора", "капитальный ремонт", "счетчик", "обслуживание", "страхование жилья",
"ремонт", "недвижимость", "агентство", "освещение", "обстановка", "благоустройство",
"въезд", "выезд", "жилищный", "домофон", "интерком", "пульт охраны", "отопление",
"кондиционирование", "водоснабжение", "водоотведение", "электроснабжение", "газоснабжение",
"утилизация отходов", "вывоз мусора", "обслуживание лифтов", "обслуживание домофонов",
"обслуживание ворот", "обслуживание шлагбаумов", "освещение подъезда", "уборка подъезда", 
"обслуживание придомовой территории", "уход за зелеными насаждениями", "озеленение",
"благоустройство территории", "охрана территории", "видеонаблюдение", "противопожарная безопасность",
"содержание общего имущества", "сантехник", "электрик", "маляр", "штукатур", "плиточник", "столяр",
"плотник", "сварщик", "кровельщик", "фасадчик", "оконщик", "дверник", "стекольщик", "мебельщик",
"дизайнер интерьера", "архитектор", "инженер", "сметчик", "прораб", "строитель", "отделочник",
"установщик", "настройщик", "ремонтник", "обслуживающий персонал", "новостройка", "вторичка", "земля",
"дача", "дом", "коттедж", "таунхаус", "апартаменты", "комната", "доля", "пай", "гараж", "машиноместо",
"кладовка", "подвал", "чердак", "мансарда", "земельный участок", "оценка недвижимости", "страхование ипотеки",
"залог", "задаток", "аванс", "ипотечный калькулятор", "ипотечная ставка", "первый взнос", "ежемесячный платеж",
"досрочное погашение", "рефинансирование ипотеки", "ипотечные каникулы", "ипотечный договор",
"реестр недвижимости","свидетельство о собственности"],
        "образование": ["курсы", "школа", "университет", "онлайн-курсы", "колледж",
"училище", "повышение квалификации","обучение", "вебинар", "учебник", "канцелярия",
"канцтовары", "репетитор", "тренинг", "мастер-класс", "семинар", "стажировка",
"литература", "пособие", "тетрадь", "ручка", "карандаш", "ластик", "циркуль",
"линейка", "краски", "кисти", "альбом", "папка", "рюкзак", "портфель", "детский сад",
"ясли", "центр развития", "подготовительные курсы", "музыкальная школа", "художественная школа",
"спортивная школа", "языковая школа", "автошкола", "академия", "институт", "консерватория", "лицей",
"гимназия", "кадетский корпус", "военное училище", "духовная семинария", "монашеский орден",
"центр повышения квалификации", "научно-исследовательский институт", "лаборатория", "обсерватория",
"музей", "библиотека", "архив", "галерея", "театр", "киностудия", "телецентр", "радиостанция",
"издательство", "типография", "книжный магазин", "антикварный магазин", "онлайн-школа",
"дистанционное обучение", "вечерняя школа", "заочное обучение", "экстернат", "самообразование",
"семейное образование", "бакалавриат", "магистратура", "аспирантура", "докторантура", "ординатура",
"интернатура", "профессиональная переподготовка", "повышение квалификации", "стажировка", "практика",
"летняя школа", "зимняя школа", "языковые курсы", "компьютерные курсы", "курсы дизайна", "курсы фотографии",
"курсы видеомонтажа", "курсы актерского мастерства", "курсы вождения", "курсы массажа", "курсы"],
        "переводы": ["перевод", "на карту", "qiwi", "сбер", "втб", "альфа",
 "т-банк", "газпромбанк", "россельхозбанк", "комиссия", "обмен валюты", "paypal",
"яндекс деньги", "webmoney", "western union", "swift", "корпоративный",
"благотворительность", "пожертвование", "перевод денег", "криптовалюта", "оплата",
"финансовые услуги", "перевод с пластиковой карты", "чек", "наличные", "пополнение счета", "снятие наличных",
"оплата картой",  "Золотая Корона"]       
    }


def categorize_transaction(description: str, categories: dict) -> str:
    """
    Reduce the description to lowercase
    Check if a keyword is included in the description.
    If found, return the category. If you haven't found it, return "другое"
    """
    description_lower = description.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category
    return "другое"
  

def categorize_all_transactions(transactions: list) -> list:
    """
    Accepts a list of transactions in the format:
        [[date, amount, description, type], ... ]

    Returns: [[date, amount, description, type, category], ... ]
    """
    categories = create_categories()
    result = []

    for trans in transactions:
        date, amount, description, trans_type = trans[0], trans[1], trans[2], trans[3]
        if trans_type == 'доход':
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
    # Получаем данные о транзакциях по месяцам. Данные в виде: 
    # {номер месяца : [[первая транзакция], [вторая транзакция], ...], }
    all_transactions_by_months = sort_by_month(transactions)

    #Количество анализируемых месяцев
    number_of_months = len(all_transactions_by_months)

    # Проходимся по всем данным за каждый месяц. Объединяем данные о транзакциях в одинаковых категориях.
    # Словарь с данными, приведенными к нужному виду выглядит как:
    # {номер месяца : {категория_1 : траты, категория_2 : траты, ...}, ...}
    months_data = {}
    for month_number in all_transactions_by_months:
        # Транзакции за месяц: [[первая транзация], [вторая транзация], ...]
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
    
    # Суммарные траты в категориях за все время:
    # {категория_1 : суммарные_траты, категория_2 : суммарные_траты, ...}
    total_expenses_in_categories = {}
    for month in months_data:
        # Данные за месяц: {категория_1 : траты, категория_2 : траты, ...}
        month_data = months_data[month]

        for category in month_data:
            # Траты в одной категории за один месяц
            expense_in_category = month_data[category]

            if category in total_expenses_in_categories:
                total_expenses_in_categories[category] += expense_in_category
            else:
                total_expenses_in_categories[category] = expense_in_category
    
    # Средние траты по категориям за месяц:
    # {категория_1 : средние траты, категория_2 : средние траты, ...}
    average_expenses_by_category = {}
    for category in total_expenses_in_categories:
        average_expenses_by_category[category] = \
            round(total_expenses_in_categories[category] / number_of_months, 2)
    
    # Отсортированные по убыванию суммарные траты в категориях:
    # [(категория_1 : траты), (категория_2 : траты), ...]
    total_expenses_in_categories_sorted = sorted(total_expenses_in_categories.items(),
                                          key= lambda i: i[1],
                                          reverse= True)
    
    # 3 категории с самыми большими тратами:
    # {категория_1 : траты, категория_2 : траты, категория_3 : траты}
    top_3_category = {}
    for i in range(3):
        category = total_expenses_in_categories_sorted[i][0]
        expense_val = total_expenses_in_categories_sorted[i][1]
        top_3_category[category] = expense_val

    # Общие расходы за каждый месяц:
    # {месяц_1 : траты, месяц_2 : траты, ...}
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

    # Общие траты за сезоны:
    # {Лето : траты, Весна : траты, ...}
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
    

    # Общие траты за сезоны, отсортированные по убыванию
    seasonal_data_sorted = sorted(seasonal_data.items(),
                                  key=lambda i: i[1],
                                  reverse= True)
    
    # Величина максимальных трат, название сезона с данной величиной
    max_exp, max_exp_name = seasonal_data_sorted[0][1], seasonal_data_sorted[0][0]
    # Величина минимальных трат, название сезона с данной величиной
    min_exp, min_exp_name = seasonal_data_sorted[-1][1], seasonal_data_sorted[-1][0]

    seasonal_patterns = [(max_exp_name, max_exp), (min_exp_name, min_exp)]

    # Категория с максимальными тратами: (категория, траты)
    max_exp_category = total_expenses_in_categories_sorted[0]
    #Категория со средними затратами: (категория, траты)
    several_exp_category = total_expenses_in_categories_sorted[len(total_expenses_in_categories_sorted) // 2]
    # Рекомендуемое уменьшение трат для категории с максимальными тратами
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
    # Словарь с данными трат в категориях по месяцам:
    # {номер месяца : {категория_1 : траты, категория_2 : траты, ...}, ...}
    months_data = analysis['category data by month']
    
    # time_stats - словарь с данным за каждый месяц:
    # {номер_месяца : {доход : значени, расход : значение, популярные категории : список}, ...}

    # Сбережения за каждый месяц
    saving_dict = {}
    for month in time_stats:
        data_month = time_stats[month]
        income = data_month[ru.INCOME]
        expense = data_month[ru.EXPENSE]
        saving = income - expense

        saving_dict[month] = saving

    # Распределение бюджета на 3 укрупненные категории
    budget_allocation_percentage = {1: 0, 2: 0, 3: 0}
    for month in months_data:
        month_data = months_data[month]

        for category in month_data:
            value = month_data[category]
            if category in ['жилье', 'быт', 'еда', 'транспорт', 'здоровье']:
                budget_allocation_percentage[1] += value
            if category in ['развлечения', 'одежда', 'образование']:
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


def print_report(stats: list,
                 category_stats: list,
                 time_stats: list,
                 analysis: dict,
                 budget: dict
                 ) -> None:
    '''
    Beautiful design and print of analyzed data.
    '''

    print(ru.PR_FINANCIAL_REPORT, end= '\n\n')

    print(ru.PR_KEY_INDICATORS,
          f'{ru.PR_INCOME} {stats[ru.INCOME]} {ru.PR_RUB}',
          f'{ru.PR_EXPENSE}: {stats[ru.EXPENSE]} {ru.PR_RUB}',
          f'{ru.PR_BALANCE} {stats[ru.BALANCE]} {ru.PR_RUB}',
          f'{ru.PR_NUM_TRANS} {stats[ru.TRANSACTIONS_QUANTITY]}',
          sep='\n', end= '\n\n')

    print(ru.PR_CATEGORY_EXPENSES)
    for category in category_stats:
        print(f'{ru.PR_CATEGORY} {category}')
        print(f'{ru.PR_EXPENSES}: {category_stats[category][0]}',
              f'{ru.PR_TRANSACTION_COUNT}: {category_stats[category][1]}',
              f'{ru.PR_PERCENT_OF_TOTAL}: {category_stats[category][2]}',
              sep=', ', end= '\n\n')

    print(ru.PR_MONTHLY_EXPENSES)
    for month in time_stats:
        print(f'{ru.PR_MONTH} {month}')
        print(f'{ru.PR_INCOMES}: {time_stats[month][ru.INCOME]}',
              f'{ru.PR_EXPENSES}: {time_stats[month][ru.EXPENSE]}',
              f'{ru.PR_POPULAR_CATEGORIES}: {time_stats[month][ru.POPULAR_CATEGORIES]}',
              sep='\n', end= '\n\n')

    print(ru.PR_HISTORICAL_ANALYSIS)
    print(f'{ru.PR_AVERAGE_COSTS}:')
    for category in analysis['average costs']:
        value = analysis['average costs'][category]
        print(f'{category} : {value}')
    print()
        
    print(f'{ru.PR_SEASONAL_PATTERNS}:')
    print(f'{ru.PR_SEASON_PAT_HIGH_COSTS} {analysis['seasonal patterns'][0][0]}',
          f'{ru.PR_SEASON_PAT_EQUAL} {analysis['seasonal patterns'][0][1]} {ru.PR_RUB}')
    print(f'{ru.PR_SEASON_PAT_SMALL_COSTS} {analysis['seasonal patterns'][1][0]}',
          f'{ru.PR_SEASON_PAT_EQUAL} {analysis['seasonal patterns'][1][1]} {ru.PR_RUB}',
          end= '\n\n')
    
    print(f'{ru.PR_BIGGEST_EXPENSES}:')
    for category in analysis['biggest expenses']:
        value = analysis['biggest expenses'][category]
        print(f'{category} : {value}')
    print()

    print(f'{ru.PR_RECOMMENDATIONS}:')
    print(f'{ru.PR_RECOMMEND_PLAN} {analysis['recommendations'][0]} ' \
          f'{ru.PR_BY} {analysis['recommendations'][1]}%',
          end= '\n\n')

    print(ru.PR_BUDGET,
          ru.PR_BUDGET_DISTRIBUTION,
          ru.PR_BUDGET_ESSENTIALS,
          ru.PR_BUDGET_LIFESTYLE,
          ru.PR_BUDGET_SAVINGS,
          sep='\n')

    if budget[0]:
        print(ru.PR_BUDGET_SUCCESS)
    else:
        print(ru.PR_BUDGET_FAILURE)
        print(f'{ru.PR_BUDGET_CATEGORY_1} {budget[1]}',
              f'{ru.PR_BUDGET_CATEGORY_2} {budget[2]}',
              f'{ru.PR_BUDGET_CATEGORY_3} {budget[3]}',
              sep= '\n')


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

    # 2. Role 2: Classify transactions.
    categorized_transactions = categorize_all_transactions(transactions)

    # 3. Role 3: Analyzing statistics.
    stats = calculate_basic_stats(categorized_transactions)
    category_stats = calculate_by_category(categorized_transactions)
    time_stats = analyze_by_time(categorized_transactions)

    # 4. Role 4: Budget planning.
    analysis = analyze_historical_spending(categorized_transactions)
    budget = create_budget_template(time_stats, analysis)
    report_budget = compare_budget_vs_actual(budget)

    # We display the results.
    print_report(stats, category_stats, time_stats, analysis, report_budget)


if __name__ == '__main__':
    main()
