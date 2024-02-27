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

<img src = "/README_image/spatial interpolation.png" width = "100%"> 

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
The final result file is in *Green Index.csv*
