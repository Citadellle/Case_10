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
