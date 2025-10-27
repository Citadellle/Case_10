def read_csv_file(filename: str) -> list:
    pass


def read_json_file(filename: str) -> list:
    pass


def import_financial_data(filename: str) -> list:
    pass




def create_categories() -> dict:
    pass


def categorize_transaction(description: str, categories: dict) -> str:
    pass


def categorize_all_transactions(transactions: list) -> list:
    pass




def calculate_basic_stats(transactions: list) -> list:
    pass


def calculate_by_category(transactions: list) -> list:
    pass


def analyze_by_time(transactions: list) -> dict:
    pass




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
