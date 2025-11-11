import ru_local as ru


def create_categories() -> dict:
    """
    Creates a dictionary of categories: the key is the category name,
    The value is a list of keywords.
    """
    return {
        "еда": ["пятерочка", "магнит", "продукты", "еда", "супермаркет",
 "добрянка",  "мария-ра", "ярче", "мясо", "кондитерская", "пекарня",
 "овощи", "фрукты", "окей", "дикси", "ярмарка", "фермер", "лавка", "обед", "ужин", "завтрак"],
        "транспорт": ["метро", "автобус", "такси", "бензин",
 "аренда самоката", "ж/д","билет", "дизель", "газ", "поезд",
 "электричка", "авиабилет", "аэрофлот", "велосипед", "газель"],
        "развлечения": ["кино", "атракцион", "выступление",
"концерт", "театр", "выставка", "боулинг", "квест", "игровая", ],
        "здоровье": ["аптека", "врач", "больница", "лекарства",
"стоматология", "поликлиника", "анализы", "стоматология",
 "зуб", "лечение", "медицин",  "диагностика", "инвитро",
 "хеликс", "лаборатория",  "очки", "линзы"],
        "одежда": ["одежда", "обувь", "wildberries", "ozon",
 "спортмастер", "zolla", "o'stin", "adidas", "Rieker", "виктор",
 "lacoste", "brand", "befree", "футболка", "штаны", "носки",
 "рубашка", "zara", "h&m", "bershka"],
        "быт": ["хозтовары", "бытовая техника", "мебель",
 "порошок", "средство для стирки", "мыло", "шампунь",
                "гель для душа", "зубная паста", "щётка", "бритва",
 "салфетки", "туалетная бумага", "бумага",
                "губки", "мочалка", "перчатки", "средство для посуды",
"средство для унитаза", "освежитель", "аромат", "отбеливатель"],
        "жильё": ["аренда", "квартира", "коммунал", "электроэнергия",
 "вода", "газ", "отопление", "интернет", "wi-fi", "мтс", "билайн",
 "мегафон", "домру", "ростелеком", "жкх", "управляющая компания",
 "ипотека",   "квартплата", "содержание жилья"],
        "образование": ["курсы", "школа", "университет",
 "онлайн-курсы", "колледж", "училище", "повышение квалификации",
     "обучение", "вебинар", "учебник", "канцелярия", "канцтовары"],
        "переводы": ["перевод", "на карту", "qiwi", "сбер", "втб", "альфа",
 "т-банк", "газпромбанк", "россельхозбанк"]
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
        if trans_type == ru.INCOME:
            category = ru.INCOME
        else:
            category = categorize_transaction(description, categories)

        new_transaction = [date, amount, description, trans_type, category]
        result.append(new_transaction)
    return result
