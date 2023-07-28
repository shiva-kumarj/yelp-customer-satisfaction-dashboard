import sys
import json
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='convert input data to json format suitable for label studio ML backend')
parser.add_argument('-i', '--input', help='path to the processed reviews file containing sentiment')

args = parser.parse_args()

if args.input:
  df = pd.read_csv(args.input)
  docs = [{'data': {'text': text}} for text in df['noun']]

  print(json.dumps(docs))

else:
  print('please provide required file as input')
