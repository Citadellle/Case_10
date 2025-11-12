import tqdm
import csv
import json


def read_csv_file(filename: str) -> list:
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
    '''
    Reads JSON file and returns list of dictionaries
    '''
    try:
        # Check file extension
        if not filename.endswith('.json'):
            return ['File is not json']
        
        with open(filename, mode='r', encoding='UTF-8') as file:
            # Load JSON data directly
            result = json.load(file)
            
            # Validate that data is list of dictionaries
            if not isinstance(result, list) or not all(isinstance(item, dict) for item in result):
                return ['Invalid data format: expected list of dictionaries']
            
            return result
    # In case incorrect name. 
    except FileNotFoundError:
        return ['File not found']


def import_financial_data(filename: str) -> list:
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

    exit data example (lang='ru'):
    ['2024-01-18', -780.9, 'Продукты в Магните', 'расход']
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
    k_type = ''

    # We run through the first element of the dictionary,
    # finding the keys we need.
    for need_keys in read_data[0].keys():
        if 'amount' in need_keys:
            k_amount = need_keys
        if 'date' in need_keys:
            k_date = need_keys
        if 'description' in need_keys:
            k_description = need_keys
        if 'type' in need_keys:
            k_type = need_keys

    if k_type != '':
        # Loop for generating lists of lists.
        exit_list = []
        # Use tqdm for printing status bar.
        for dictionary in tqdm.tqdm(read_data):
            inter_list = [dictionary[k_date], float(dictionary[k_amount]),
                          dictionary[k_description], dictionary[k_type]]
            exit_list.append(inter_list)

        return exit_list

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
