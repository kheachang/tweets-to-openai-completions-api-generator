
# tweets-to-openai-completions-api-generator

JSONL generator for your tweets and its keywords. Designed to be used to fine-tune OpenAI models. 

## Background
Read more about OpenAI fine tuning [here](https://platform.openai.com/docs/guides/fine-tuning).

This script fine tunes `gpt-3.5-turbo`. OpenAI requires the data set to be in the format of:
```json
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
```

This script uses the tweet as `completion` and uses OpenAI chat completion to extract keywords of the tweet as `prompt`. 

## Prerequisites
This script requires you to have a csv file of your tweets. OpenAI recommends fine-tuning on 50 to 100 training examples with `gpt-3.5-turbo`. 

## How to Run
##### 1. Install OpenAI API and get an API key. 
##### 2. Put your csv file of tweets into the `tweets` folder.
##### 3. Run `generate.py`.
##### 4. Result file will be saved in the `tweets` folder as `fine_tuning_file.jsonl`.
