from calendar import month

import ru_local as ru
import import_financial_data_ru as fdi
import catigorize as cat
import statistic as stat
import planing as plan


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
        print(f'{ru.PR_MONTH} {ru.month_ru[month]}')
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
    transactions = fdi.import_financial_data(input('enter file name -->'))

    # 2. Role 2: Classify transactions.
    categorized_transactions = cat.categorize_all_transactions(transactions)

    # 3. Role 3: Analyzing statistics.
    stats = stat.calculate_basic_stats(categorized_transactions)
    category_stats = stat.calculate_by_category(categorized_transactions)
    time_stats = stat.analyze_by_time(categorized_transactions)

    # 4. Role 4: Budget planning.
    analysis = plan.analyze_historical_spending(categorized_transactions)
    budget = plan.create_budget_template(time_stats, analysis)
    report_budget = plan.compare_budget_vs_actual(budget)

    # We display the results.
    print_report(stats, category_stats, time_stats, analysis, report_budget)


if __name__ == '__main__':
    main()
