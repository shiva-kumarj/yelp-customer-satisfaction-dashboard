import pandas as pd
import numpy as np
import stanza
from IPython.display import display, clear_output
import argparse


# Retrieve the sentiment of each noun from a sentence
def get_noun_sentiment(review, record_count):
    sentiment_map = {}
    for sentence in nlp(review).sentences:
        sentiment = sentence.sentiment
        sentiment_map[sentence.text] = sentiment
    record_count[0] += 1
    # logging.info(f'Processed {record_count[0]} out of {record_count[1]}.')
    # print(f'Processed {record_count[0]} out of {record_count[1]}.')
    # print(f'Time: {end_time_cpu - start_time_cpu}.')
    # Clears the output cell before displaying the next message
    clear_output(wait=True)
    display(f'Processed {record_count[0]} out of {record_count[1]}.')
    return sentiment_map


def write_file_to_disk(df, filename):
    df.to_csv(filename, index=False,)


# File map
business_file_map = {}


def batch_sentiment_extraction(b_id, business_number, processed_b_ids):
    batch_size = len(review_df[review_df['business_id'] == b_id])
    record_count = [0, batch_size]
    print(f'Sentiment Extraction of {b_id} Beginning.')
    print(f'Batch size: {batch_size}.')
    review_df.loc[:, 'review_sentiment'] = review_df[review_df['business_id'] ==
                                                     b_id]['corrected_text'].apply(lambda x: get_noun_sentiment(x, record_count))
    print(f'Sentiment Extraction of {b_id} Complete.')
    print('Writing the file to disk...')
    processed_sentiment = review_df.loc[review_df['business_id'] == b_id]
    write_file_to_disk(processed_sentiment,
                       f'sentence_sentiment/review_b_id_{business_number}.csv')
    processed_b_ids.loc[len(processed_b_ids)] = [b_id, business_number]
    return


def begin_batch_processing(pending_b_ids, processed_b_ids):
    for index, row in pending_b_ids.iterrows():
        if row['business_id'] in processed_b_ids['business_id'].to_list():
            continue
        else:
            batch_sentiment_extraction(row['business_id'], row['serial_num'], processed_b_ids)
            print(f'Writing processed business ids to {args.processed_b_id}')
            write_file_to_disk(processed_b_ids, args.processed_b_id)


if __name__ == '__main__':

    review_df = pd.read_csv(
        "D:\\My-Projects\\yelp-customer-satisfaction-improvement\\review\\review_corrected_text.csv")

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description='runs sentiment analysis on reviews and writes the result to a csv file')

    # add command line arguments
    parser.add_argument('-p', '--pending_b_id',
                        help='path to the pending business ids file')
    parser.add_argument('-d', '--processed_b_id',
                        help='path to the processed business ids file')

    # pending_b_ids = 'sentence_sentiment/pending_b_ids_1.csv'
    # processed_b_ids = 'sentence_sentiment/b_ids_processed_1.csv'

    # parse the arguments
    args = parser.parse_args()

    if args.pending_b_id:
        pending_b_ids = pd.read_csv(args.pending_b_id)

    if args.processed_b_id:
        b_ids_processed = pd.read_csv(args.processed_b_id)

    else:
        print('please input requried paths.')
    # initialize NLP pipeline
    nlp = stanza.Pipeline(processors='tokenize,sentiment',
                          lang='en', use_gpu=True)

    # begin batch processing of reviews.
    begin_batch_processing(pending_b_ids, b_ids_processed)
