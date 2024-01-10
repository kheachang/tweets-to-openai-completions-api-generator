import csv
import json
import os
from openai import OpenAI

CSV_FILEPATH = r"tweets/tweets.csv"

client = OpenAI()

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

def tweet_make_content_array(csvFilePath, num_rows):
    """Extract 'Content' values from CSV and return as an array"""

    content_array = []
    date_column = find_date_column(csvFilePath)

    if date_column:
        with open(csvFilePath, encoding="utf-8-sig") as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0
            for rows in csvReader:
                content_array.append(rows["Content"])
                row_count += 1
                if row_count >= num_rows:
                    break

        return content_array
    else:
        return ["No 'Date' column found in the CSV file."]

def get_keywords_from_tweet():
    """Gets up to 3 keywords from tweet to use in training data."""

    content = "This is a tweet about cats."  # the tweet
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with an array of strings, and your task is to extract up to 3 keywords from each element of the array.",
            },
            {"role": "user", "content": content},
        ]
    )
    return response.choices[0].message.content  # cats, tweet

def create_dataset():
    """Creates dataset in the format of openai chat completions api."""

    """
        "message": [
            {"role": "system", "content": "You output tweets based on what the prompts are."},
            {"role": "user", "content": "<keywords from the tweets>"},
            {"role": "assistant", "content": "<the tweet>"}
            ]
    """
    messages = []
    data = {}

    # should output json file


def check_dataset_format():
    """Runs checks to ensure formatting for chat completions api is correct."""


# tweet_make_json(CSV_FILEPATH, 50)
get_keywords_from_tweet()


