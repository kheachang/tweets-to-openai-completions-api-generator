import csv
import json

CSV_FILEPATH = r'tweets/tweets.csv'
JSON_FILEPATH = r'tweets/tweets.json'

def find_date_column(CSV_FILEPATH):
    with open(CSV_FILEPATH, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        if '\ufeff"Date"' in csvReader.fieldnames:
            return '\ufeff"Date"'  # Return the correct header name if found
        elif 'Date' in csvReader.fieldnames:
            return 'Date'  # Return 'Date' as the header name
        else:
            return None  # Return None if the column header is not found

def make_json(CSV_FILEPATH, JSON_FILEPATH, num_of_rows):
    data = {}
    date_column = find_date_column(CSV_FILEPATH)  # Get the date column header

    if date_column:
        with open(CSV_FILEPATH, encoding='utf-8-sig') as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0  # Initialize row counter
            for rows in csvReader:
                key = rows[date_column]  # Use the identified date column header
                data[key] = rows
                row_count += 1
                if row_count >= num_of_rows:  # Check if the specified number of rows is reached
                    break  # Exit the loop if the specified number of rows is processed
        with open(JSON_FILEPATH, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

        print(f"JSON file '{JSON_FILEPATH}' created successfully.")
    else:
        print("No 'Date' column found in the CSV file.")
		

make_json(CSV_FILEPATH, JSON_FILEPATH, 50)
