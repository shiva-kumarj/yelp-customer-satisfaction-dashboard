import openai
import time
import os
import pandas as pd

from tenacity import (
  retry,
  stop_after_attempt,
  wait_random_exponential
)

def get_review_label(input_text, categories):
  prompt = f"when asked classify the input text into one of the following categories: {', '.join(categories)}. your only response should be one of the categories. here is the text: \"{input_text}\""
  
  message = [
      # {"role": "system", "content": prompt},
      {"role": "user", "content": prompt}
  ]

  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-0613",
  messages=message,
  temperature=0,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )

  return response['choices'][0].message['content'].strip()

# labels for review classification
categories = ['experience', 'foodquality', 'atmosphere', 'price', \
              'location', 'decor', 'staff', 'hygiene', 'speedofservice',\
              'drinks', 'noise', 'entertainment', 'noneoftheabove', 'timing', \
              'wrongorder', 'service']

openai.api_key = os.environ.get('OPENAI_API_KEY')

# review = 'used to be a nice late night stop for greasy food after hitting some bars in the area.'

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
  return get_review_label(**kwargs)

def write_to_disk(df, directory_path, file_name):
  file_path = os.path.join(directory_path, file_name)
  df.to_csv(file_path, index=False)


if __name__ == '__main__':

  # Directory of the source data.
  input_directory_path = '../cleaned_review_dataset/'
  output_directory_path = './review_data_annotated'

  # Check which files are already processed.
  previously_annotated_files = os.listdir(output_directory_path)
  # print(previously_annotated_files)
  # loop through list of already annotated files and find the last annotated file
  latest_serial_num = 0
  for f in previously_annotated_files:
    current_serial_num = int(f.split('.')[0][14:])
    if current_serial_num > latest_serial_num:
      # serial numnber of the last anntated file
      latest_serial_num = int(current_serial_num)


  try:
    for i in range(latest_serial_num+1, 101):
      file_name = f'cleaned_data_{i}.csv'
      file_path = os.path.join(input_directory_path, file_name)

      data = pd.read_csv(file_path)

      # Get classification label from OpenAPI
      print(f'Processing file {file_name}')
      data['label'] = data['noun'].apply(lambda text: completion_with_backoff(input_text=text, categories=categories))

      # 
      write_to_disk(data, directory_path=output_directory_path, file_name=f'annotated_b_id{i}.csv')
      print(f'Writing file {file_name} to disk')
  
  except KeyboardInterrupt:
    print('Keyboard interrupt detected. Stopping the process..')
  
  except Exception as e:
    print('an error occurred: ', e)

