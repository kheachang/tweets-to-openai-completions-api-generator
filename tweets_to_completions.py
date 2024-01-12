import ast
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

    message_list = []
    content_array = []
    date_column = find_date_column(csvFilePath)
    # sys_message = {"role": "system", "content": "You create tweets based on what the prompts are."}

    if date_column:
        with open(csvFilePath, encoding="utf-8-sig") as csvf:
            csvReader = csv.DictReader(csvf)
            row_count = 0
            for rows in csvReader:
                sys_message = {"role": "system", "content": "You create tweets based on what the prompts are."}
                assis_message = {"role": "assistant"}
                content = rows["Content"]
                content_without_emojis = remove_emojis(content)
                content_array.append(content_without_emojis)
                assis_message["content"] = content_without_emojis  # tweet
                message_list.append({"messages": [sys_message, assis_message]})
                row_count += 1
                if row_count >= num_rows:
                    break
        jsonl_filename = f"tweets/tweets_{num_rows}_rows.jsonl"
        with open(jsonl_filename, 'w', encoding='utf-8') as jsonl_file:
            for message in message_list:
                jsonl_file.write(json.dumps(message) + '\n')

        return content_array  # 948 tokens
    else:
        return "No 'Date' column found in the CSV file."


def get_keywords_from_tweet(tweets):
    """Gets up to 3 keywords from tweet to use in training data."""
    tweets_list_to_string = json.dumps(tweets)
    print("Getting keywords...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with an array of strings, and your task is to extract up to 3 keywords from each element of the array. Return a new array with the keywords as strings separated by commas for each original string.",
            },
            {"role": "user", "content": tweets_list_to_string},
        ],
    )
    keywords_list = ast.literal_eval(response.choices[0].message.content)  # ['key1', 'key2, key3']
    fine_tuning_jsonl_file = "tweets/fine_tuning_file.jsonl"

    with open("tweets/tweets_50_rows.jsonl", 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()
        for index, line in enumerate(lines):
            try:
                json_data = json.loads(line.strip())
                user_message = {"role": "user", "content": keywords_list[index]}  # add keywords to each tweet
                if 'messages' in json_data:
                    # Insert the new element at index 1 in the 'messages' array
                    json_data['messages'].insert(1, user_message)

                    # Write the updated JSON data back to the file
                    with open(fine_tuning_jsonl_file, 'a', encoding='utf-8') as output_file:
                        output_file.write(json.dumps(json_data) + '\n')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON at line {index + 1}: {e}")
    
    return "Fine tuning file complete. Check inside the tweets directory."


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


# tweet_make_content_array(CSV_FILEPATH, 50)
tweets = tweet_make_content_array(CSV_FILEPATH, 50)
get_keywords_from_tweet(tweets)
