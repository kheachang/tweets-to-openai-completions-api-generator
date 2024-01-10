import csv
import json
import os
import re
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


def remove_emojis(text):
    """Remove emojis from text using regex"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "]+",
        flags=re.UNICODE,
    )

    return emoji_pattern.sub(r'', text)

def tweet_make_content_array(csvFilePath, num_rows):
    """Extract 'Content' values from CSV and return as an array"""

    content_array = []
    date_column = find_date_column(csvFilePath)

    if date_column:
        with open(csvFilePath, encoding="utf-8-sig") as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0
            for rows in csvReader:
                content = rows["Content"]
                content_without_emojis = remove_emojis(content)
                content_array.append(content_without_emojis)
                row_count += 1
                if row_count >= num_rows:
                    break

        return content_array  # 948 tokens
    else:
        return ["No 'Date' column found in the CSV file."]


def get_keywords_from_tweet(tweets):
    """Gets up to 3 keywords from tweet to use in training data."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with an array of strings, and your task is to extract up to 3 keywords from each element of the array. Return a new array with the keywords as strings separated by commas for each original string.",
            },
            {"role": "user", "content": tweets},
        ],
    )
    return response  # cats, tweet


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


tweets = tweet_make_content_array(CSV_FILEPATH, 50)
get_keywords_from_tweet(tweets)
