"""
DataFrame Cleaning Script for Sentiment Analysis Results

This script reads a CSV file containing sentiment analysis results and performs cleaning operations on the DataFrame. It includes functions to extract nouns and sentiment values from a sentiment dictionary, as well as cleaning operations to fix date types, drop unnecessary columns, explode lists, and write the cleaned DataFrame to a new file.

Usage:
- Run the script with the required command-line arguments to clean the DataFrame.
- The cleaned DataFrame will be saved to a new file in the 'processed_reviews' directory.

Dependencies:
- pandas: Required for DataFrame operations.
- argparse: Required for command-line argument parsing.

Author: Shiva Kumar
Date: July 12, 2023

Usage example:
python sentiment_cleaning.py -i input_file.csv

Command-line arguments:
  -i, --input    Input file path: Specify the path to the CSV file containing sentiment analysis results.

"""

# ... Rest of the script ...


import json
import pandas as pd 
import sys
import argparse

def get_sentiment_noun(sentiment_dict):
  """
    Extracts the nouns (keys) from a sentiment dictionary.

    Parameters:
        sentiment_dict (str or dict): A sentiment dictionary representing the sentiment analysis results.

    Returns:
        list: A list of nouns (keys) extracted from the sentiment dictionary.

    Example:
        sentiment_dict = "{'forget the others.': 1, 'jim steaks offers the best cheese steak in philly.': 2}"
        nouns = get_sentiment_noun(sentiment_dict)
        print(nouns)
        # Output: ['forget the others.', 'jim steaks offers the best cheese steak in philly.']
  """
  sentiment_dict = eval(sentiment_dict)
  return sentiment_dict.keys()

def get_sentiment_value(sentiment_dict):
  """
    Extracts the sentiment values from a sentiment dictionary.

    Parameters:
        sentiment_dict (str or dict): A sentiment dictionary representing the sentiment analysis results.

    Returns:
        list: A list of sentiment values extracted from the sentiment dictionary.

    Example:
        sentiment_dict = "{'forget the others.': 1, 'jim steaks offers the best cheese steak in philly.': 2}"
        values = get_sentiment_value(sentiment_dict)
        print(values)
        # Output: [1, 2]
  """
  sentiment_dict = eval(sentiment_dict)
  return sentiment_dict.values()

def clean_dataframe(df):
  # fix date type
  df['date'] = pd.to_datetime(df['date'])
  df = df.drop(['text', 'corrected_text'], axis=1)
  df['noun'] = df['review_sentiment'].apply(get_sentiment_noun)
  df['value'] = df['review_sentiment'].apply(get_sentiment_value)

  df = df.explode(['noun', 'value'])

  df = df.drop('review_sentiment', axis=1)
  
  return df

def write_file_to_disk(df, filename):
    df.to_csv(filename, index=False,)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='read file input and parse dictionary type columns into separate ones')

  parser.add_argument('-i', '--input', help='review file with sentiment extracted by stanza')
  # 
  args = parser.parse_args()

  if args.input:
      review_df = pd.read_csv(args.input)
      review_df = clean_dataframe(review_df)
      write_file_to_disk(review_df, f'processed_reviews/{args.input}')

  else:
      print('please provide input file path')
# df = pd.read_csv(sys.argv[1])

# docs = [{'data': {'text': text}} for text in df['noun']] 

# print(json.dumps(docs))