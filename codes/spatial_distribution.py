# Saptial Distribution Codes
# !pip install pydeck
# !pip install geemap
# !pip install imgkit
# !pip install selenium
import pydeck as pdk
import pandas as pd
import csv
import json
from IPython.display import HTML
import colorsys

mapbox_key =  # write your mapbox key
directory = # write your directory

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
txt_file_path = directory + 'data.txt'

with open(txt_file_path, 'w', encoding='utf-8') as f:
  f.write(json_string)

with open(txt_file_path, 'r') as f:
  geo_street = json.load(f)

# convert green index csv to json
path = directory + 'busan201819.csv' # green index file
hedonic = pd.read_csv(path)

with open(path, 'r') as f:
  reader = csv.reader(f)
  next(reader)

  data = []
  for line in reader:
    d = {
      'latitude': line[6]  # latitude column
      'longitude': line[5]  # longitude column
      'properties': {
        'green index': line[32]}  # green index column
    }
    data.append(d)

json_string = json.dumps(data, ensure_ascii=False, indent=2)

txt_file_path = directory + 'green_data.txt'

with open(txt_file_path, 'w', encoding='utf-8') as f:
  f.write(json_string)

with open(txt_file_path, 'r') as f:
  geo = json.load(f)

# plotting value as point and cuboid
busan_mini = busan[['x', 'y', 'HGVI_50']].copy()

max_index_value = max(float(item["properties"]["green index"]) for item in geo)
min_index_value = min(float(item["properties"]["green index"]) for item in geo)

pdk.settings.mapbox_key = mapbox_key

# Scaling values
def minmax(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

# Value-based color assignment
def calculate_color(item):
    index_value = float(item["properties"]["green index"])
    minmax_value = minmax(index_value, min_index_value, max_index_value)
    return [0, 255*minmax_value, 255*(1-minmax_value), 255]

# Value-based height assignment
def calculate_elevation(item):
    index_value2 = float(item["properties"]["green index"])
    minmax_value = minmax(index_value2, min_index_value, max_index_value)
    return minmax_value * 3000

geo_street_transformed_2 = [
    {"longitude": float(item["longitude"]), "latitude": float(item["latitude"])}
    for item in geo_street
]

geo_transformed_2 = [
    {
        "longitude": float(item["longitude"]),
        "latitude": float(item["latitude"]),
        "color": calculate_color(item),
        "elevation": calculate_elevation(item)  # elevation은 집값
    }
    for item in geo
]

elevation_values = [int(item['elevation']) for item in geo_transformed_2]
max_elevation = max(elevation_values)

color_values = [item['color'] for item in geo_transformed_2]

busan_mini['elevation'] = elevation_values
busan_mini['color'] = color_values

lon, lat = 129.0708802, 35.1153616 # Choose a point of view to visualize

# Visualize the values of two layers at once
layer11 = pdk.Layer(
    'ScatterplotLayer',
    geo_street_transformed_2,
    get_position = '[longitude, latitude]',
    get_color = '[255, 255, 255, 255]',
    get_radius=100
)

layer22 = pdk.Layer(
    'ColumnLayer',
    busan_mini,
    extruded=True,
    get_position='[x,y]',
    get_fill_color = 'color',
    get_elevation='elevation',
    elevation_scale=1,
    elevation_range=[0, max_elevation],
    pickable=True,
    auto_highlight=True,
    radius=100,
    opacity= 0.01
)

view_state = pdk.ViewState(longitude= lon, latitude= lat, zoom=12.5, pitch=70, bearing=-27.36)
r = pdk.Deck(layers=[layer11, layer22], initial_view_state=view_state)
data_result = r.to_html('result.html',as_string=True)

# save the picture
import imgkit
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
# 해상도 조정하기:)
driver.set_window_size(2560, 1440)

file_path = '/content/result.html'
driver.get('file://' + file_path)

time.sleep(10)

screenshot_path = '/content/screenshot.png'
driver.save_screenshot(screenshot_path)
driver.quit()

from google.colab import files
files.download(screenshot_path)
