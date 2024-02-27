# Green Index Data Records   
<img src="https://img.shields.io/badge/Google Colab-F9ABOO?style=for-the-badge&logo=Google Colab&logoColor=white" link='https://colab.google/'> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">  
We devised the new index called 'Green Index', based on street image in Busan in 2017 and 2018. 

To derive the green index, we went through the process of collecting GSV images, converting to HSV, calculating green index, and spatial interpolation.
  
This four-step process is necessary to effectively implement the green index, and for a detailed explanation, please refer to the [paper](https://doi.org/10.1038/s41598-023-49845-0), and sample data was stored in the 'data' folder to facilitate this implementation.   

Data in this repository concists of CSV and Excel files:   

- *Data.csv*: Location of transaction sample data
- *Green.csv*: Roadside trees location and green index sample data
- *Green Index.csv*: Final green index using spatial interpolation method

## Image Preprocessing and Calculating Green Index
In order to calculate the green index, it is necessary to convert GSV images to HSV images.    
For ease of data mapping, the name of the roadside tree image file was saved as longitude, latitude, and transaction date.   
After preprocessing, the green index was calculated using the following method:   
$$Green \ index_{i} = pixel_{non-zero}/pixel_{total} * 100$$   

The following code is to perform this step:   
```python
import warning
import cv2

warnings.filterwarnings('ignore')

lower_green = (40, 45, 30)
upper_green = (177, 177, 177)

green_indices = []

for i, n in enumerate(os.listdir()):
  lng, lat, year, month = i.split(sep=' ')
  month = month[:-4]
  img = mpimg.imread(i, cv2.IMREAD_COLOR)

  img_copy = img.copy()
  
  img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  img_mask = cv2.inRange(img_hsv, lower_green, upper_green)
  img_result = cv2.bitwise_and(img, img, mask=img_mask)

  nonmasked_index = np.where((img_result[:,:,0] != 0) & (img_result[:,:,1] != 0) & (img_result[:, :, 2] != 0))

  green_pixels = len(img_result[nonmasked_index])
  total_pixels = img_result.shape[0] * img_result.shape[1]

  #Calculate Green Index
  green_index = (green_pixels/total_pixels) * 100

  # if green_index < cutoff:
  green_indices.append([lng, lat, year, month, green_index])
  if (n % 100000) == 0:
    print(f'''{n} ing...''')

green_indices = pd.DataFrame(green_indices, columns = ['Longitude', 'Latitude', 'Year', 'Month', 'Green Index'])
green_indices.to_csv('Write your save path',index=False,encoding='utf-8-sig')
```   
From this step, we can extract the pure greenness from the pedestrian's point of view    
It can be tested with images from the *'GSV IMAGE'* folder, and the resulting image is stored in the *'IMAGE'* folder.   

<img src = "/IMAGE/128.831857 35.090245 2017 11.jpg" width = "100%"> 

## Spatial Interpolation
Spatial interpolation step is necessary to address the challenges caused by uneven spatial distribution of green index.   
To take advantage of spatial interpolation, use the sample file named *'Data.csv'* and *Green.csv*.    
The columns required to effectively manage the green index are as follows:   
- x: Longitude in the Cartesian coordinate system
- y: Latitude in the Cartesian coordinate system
- Longitude: Longitude of roadside trees
- Latitude: Latitude of roadside trees
- Green Index: Index calculated by the above steps

The mathematical form of haversine formula to use spatial interpolation is as follows:
$$d_{\text{haversine}} = 2 \times R \times \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{lat}_p) \cos(\text{lat}_g) \sin^2\left(\frac{\Delta \text{lng}}{2}\right)}\right)$$

```python
import pandas as pd
from haversine import haversine

data_df = pd.read_('Write your path\Data.csv')
green_df = pd.read_csv('Write your path\Green.csv')


Aggregated_Green_Index = []
Aggregated_Green_Index_Distance = []


num = 1
for y, x, ind in zip(data_df['y'], data_df['x'], data_df.index):
  distance = []

  for gr_y, gr_x, hgvi in zip(green_df['Latitude'], green_df['Longitude'], green_df['Green Index']):
    dis = haversine([y,x], [gr_y, gr_x], unit='km')
    distance.append([x,y,gr_x,gr_y,dis,hgvi])
  dis_df = pd.DataFrame(distance)
  dis_df.columns = ['x','y','gr_x','gr_y','distance','HGVI']
  dis_df = dis_df.sort_values('distance', ascending=True)

  # Extract the 50 nearest roadside trees
  dis_df_50 = dis_df.iloc[:50]

  mean_hgvi_50 = dis_df_50['HGVI'].mean()
  mean_dis_50 = dis_df_50['distance'].mean()

  Aggregated_Green_Index.append(mean_hgvi_50)
  Aggregated_Green_Index_Distance.append(mean_dis_50)

  if (ind % 10000) == 0:
    print(f'''{ind} ing...''')

data_df['Green Index'] = Aggregated_Green_Index
data_df['Green Index_d'] = Aggregated_Green_Index_Distance
data_df.to_csv('Write your path',index=False,encoding='utf-8-sig')
```
The result file is in *Green Index.csv*.

## Green Indices' Spatial Distribution   
[The pydeck library](https://pydeck.gl/) (version 0.8.0) is a set of Python binding for making spatial visualizations. We used these library for visualization of interpolated green indices and roadside trees in Busan.   

Each white circle indicates the location of roadside tree and the cuboid represents each green index calculated for the property transaction points. The more greenness has the higher height of cuboid. The sample dataset is in the filenamed *'Green Index.csv'* and *'Green.csv'*.  
The related code is as follows:
```python
!pip install pydeck
!pip install geemap
!pip install imgkit
!pip install selenium
```
```python
import pydeck as pdk
import pandas as pd
import csv
import json

mapbox_key =  'Write your mapbox key'

#convert csv to json
street_path = 'Your path' + 'Green.csv'
street = pd.read_csv(street_path)

with open(street_path, 'r') as f:
  reader = csv.reader(f)
  next(reader)

  data = []
  for line in reader:
    d = {'latitude': line[0], 'longitude': line[1]}
    data.append(d)

json_string = json.dumps(data, ensure_ascii=False, indent=2)
txt_file_path = directory + 'data.txt'

with open(txt_file_path, 'w', encoding='utf-8') as f:
  f.write(json_string)

with open(txt_file_path, 'r') as f:
  geo_street = json.load(f)

# convert green index csv to json
path = directory + 'Green Index.csv' # green index file
hedonic = pd.read_csv(path)

with open(path, 'r') as f:
  reader = csv.reader(f)
  next(reader)

  data = []
  for line in reader:
    d = {
      'latitude': line[0]  # latitude column
      'longitude': line[1]  # longitude column
      'properties': {'green index': line[2]}  # green index column}
    data.append(d)

json_string = json.dumps(data, ensure_ascii=False, indent=2)

txt_file_path = directory + 'green_data.txt'

with open(txt_file_path, 'w', encoding='utf-8') as f:
  f.write(json_string)

with open(txt_file_path, 'r') as f:
  geo = json.load(f)

# plotting value as point and cuboid
data_mini = data[['x', 'y', 'Green Index']].copy()

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
    for item in geo_street]

geo_transformed_2 = [
    {"longitude": float(item["longitude"]), "latitude": float(item["latitude"]), "color": calculate_color(item), "elevation": calculate_elevation(item)}
    for item in geo]

elevation_values = [int(item['elevation']) for item in geo_transformed_2]
max_elevation = max(elevation_values)

color_values = [item['color'] for item in geo_transformed_2]

data_mini['elevation'] = elevation_values
data_mini['color'] = color_values

lon, lat = 129.0708802, 35.1153616 # Choose a point of view to visualize

# Visualize the values of two layers at once
layer11 = pdk.Layer(
    'ScatterplotLayer',
    geo_street_transformed_2,
    get_position = '[longitude, latitude]',
    get_color = '[255, 255, 255, 255]',
    get_radius=100)

layer22 = pdk.Layer(
    'ColumnLayer',
    data_mini,
    extruded=True,
    get_position='[x,y]',
    get_fill_color = 'color',
    get_elevation='elevation',
    elevation_scale=1,
    elevation_range=[0, max_elevation],
    pickable=True,
    auto_highlight=True,
    radius=100,
    opacity= 0.01)

view_state = pdk.ViewState(longitude= lon, latitude= lat, zoom=12.5, pitch=70, bearing=-27.36)
r = pdk.Deck(layers=[layer11, layer22], initial_view_state=view_state)
data_result = r.to_html('result.html',as_string=True)
```   

<img src = "/README_image/green_index.png" width = "60%">   
