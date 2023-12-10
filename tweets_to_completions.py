import csv
import json
import os

CSV_FILEPATH = r'tweets/tweets.csv'

def find_date_column(csvFilePath):
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        if '\ufeff"Date"' in csvReader.fieldnames:
            return '\ufeff"Date"'  # Return the correct header name if found
        elif 'Date' in csvReader.fieldnames:
            return 'Date'  # Return 'Date' as the header name
        else:
            return None  # Return None if the column header is not found

def make_json(csvFilePath, num_rows=50):  # Accept num_rows as an argument
    data = {}
    date_column = find_date_column(csvFilePath)  # Get the date column header

    if date_column:
        json_file_name = f"tweets_{num_rows}_rows.json"  # Create JSON file name dynamically
        jsonFilePath = os.path.join("tweets", json_file_name)  # Construct the JSON file path
        with open(csvFilePath, encoding='utf-8-sig') as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0  # Initialize row counter
            for rows in csvReader:
                key = rows[date_column]  # Use the identified date column header
                data[key] = rows
                row_count += 1
                if row_count >= num_rows:  # Check if the specified number of rows is reached
                    break  # Exit the loop if the specified number of rows is processed

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

        print(f"JSON file '{json_file_name}' created successfully at '{jsonFilePath}'.")
    else:
        print("No 'Date' column found in the CSV file.")

make_json(CSV_FILEPATH, num_rows=50)  # Call make_json with the specified number of rows (50 in this case)
