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


def remove_emojis_special_char(text):
    """Remove emojis and decode apostrophes from text using regex"""
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

    # Replace encoded apostrophes with standard representation
    text_with_standard_apostrophes = text.replace("’", "'")

    text_with_replaced_ellipsis = text_with_standard_apostrophes.replace("…", "...")

    # Remove emojis using regex
    revised_text = emoji_pattern.sub(r'', text_with_replaced_ellipsis)

    return revised_text


def tweet_make_content_array(csvFilePath, num_rows):  # TODO: alter to be more based on tone.
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
                content_without_emojis = remove_emojis_special_char(content)
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
                return "Fine tuning file complete. Check inside the tweets directory."
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON at line {index + 1}: {e}")
    

def upload_training_file():   
    """Uploads training file via Files API. Returns uploaded File Object."""
    try:
        f = client.files.create(
            file=open("tweets/fine_tuning_file.jsonl", "rb"),  # TODO: make file names dynamic possibly
            purpose="fine-tune"
        )
        return f

    except IOError as e:
        return f"Error: {e}"

def create_fine_tuning_job(file_id):
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )
    return job

def generate_tweet():  # TODO: at least a certain number of char. 
    prompt = input("Enter keywords separated by comma: ")
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0613:personal::8hUtzBjE",
        messages=[
            {"role": "system", "content": "You are a tweet generator."},
            {"role": "user", "content": prompt.replace(", ", ",")}  # prompt: "key1,key2"
        ]
    )
    print(prompt + ": " + response.choices[0].message.content) 

# tweets = tweet_make_content_array(CSV_FILEPATH, 50)
# get_keywords_from_tweet(tweets)
generate_tweet()