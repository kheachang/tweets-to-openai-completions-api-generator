import csv
import json
import os

CSV_FILEPATH = r"tweets/tweets.csv"


def find_date_column(csvFilePath):
    """Handles BOM"""

    with open(csvFilePath, encoding="utf-8-sig") as csvf:
        csvReader = csv.DictReader(csvf)
        if '\ufeff"Date"' in csvReader.fieldnames:
            return '\ufeff"Date"'
        elif "Date" in csvReader.fieldnames:
            return "Date"
        else:
            return None

def tweet_make_json(csvFilePath, num_rows):
    """Convert csv into json"""

    data = {}
    date_column = find_date_column(csvFilePath)

    if date_column:
        json_file_name = f"tweets_{num_rows}_rows.json"
        jsonFilePath = os.path.join("tweets", json_file_name)
        with open(csvFilePath, encoding="utf-8-sig") as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0
            for rows in csvReader:
                key = rows[date_column]
                data[key] = rows
                row_count += 1
                if row_count >= num_rows:
                    break

        with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
            jsonf.write(json.dumps(data, indent=4))

        print(f"JSON file '{json_file_name}' created successfully at '{jsonFilePath}'.")
    else:
        print("No 'Date' column found in the CSV file.")

def get_keywords_from_tweet():
    """Gets keywords from tweet to use in training data."""


def create_dataset():
    """Creates dataset in the format of openai chat completions api."""

    """
        "message": [
            {"role": "system", "content": "You output tweets based on what the prompts are."},
            {"role": "user", "content": "<prompts from the tweets>"},
            {"role": "assistant", "content": "<the tweet>"}
            ]
    """
    messages = []
    data = {}
    
    # should output json file



def check_dataset_format():
    """Runs checks to ensure formatting for chat completions api is correct."""

tweet_make_json(CSV_FILEPATH, 50)
