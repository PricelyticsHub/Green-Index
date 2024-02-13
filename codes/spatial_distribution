# Saptial Distribution Codes
# !pip install pydeck
import pydeck
import pandas as pd
import csv
import json

# convert csv to json
street_path = directory + '부산가로수.csv' # csv file for street trees location
street = pd.read_csv(street_path)

with open(street_path, 'r') as f:
  reader = csv.reader(f)
  next(reader)

  data = []
  for line in reader:
    d = {
      'latitude': line[0] # latitude column
      'longitude': line[1] # longitude column
    }
    data.append(d)

json_string = json.dumps(data, ensure_ascii=False, indent=2)
text_file_path = directory + 'data.txt'

with open(text_file_path, 'w', encoding='utf-8') as f:
