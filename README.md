# Green Index Data Records   
<img src="https://img.shields.io/badge/Google Colab-F9ABOO?style=for-the-badge&logo=Google Colab&logoColor=white" link='https://colab.google/'> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">  
We introduce an indicator called 'green index', based on the google street view (GSV) images in Busan. 

To derive the green index, we collect GSV images, convert to HSV, calculate green index and implement spatial interpolation.   
<p align="center">
  <img src = "README_image/four step process.png" width = "30%"> <br>
  Figure 1. Steps to obtain green index
</p>
        
This four-step process is necessary to effectively compute the green index, and for a detailed explanation, please refer to the [paper](https://doi.org/10.1038/s41598-023-49845-0), and sample data was stored in the *'DATA'* folder to replicate this calculation.   

Data in this repository consists of CSV files:   

- *Calculated Greenness.csv*: Converted value of GSV images in the *DATA* folder
- *Data.csv*: Location of transaction sample data
- *Street Greenness.csv*: Calculated street greenness and its location
- *Green Index_Spatial Interpolation.csv*: Adjusted green index by implementing spatial interpolation

## Image Preprocessing and Calculating Green Index
In order to calculate the green index, it is necessary to convert red, green, and blue color space to hue, satuation, and value color space.    
Street view image obtained from GSV download tool should contain latitude and longitude tokens in file name; thus, the saved image file name is  ‘_latitude_ _longitude_.jpg’.    
These two tokens are required for employing spatial interpolation method. So, the target property should also include the location information, i.e., latitude and longitude.   
After preprocessing, the green index is calculated as follows:   
$$Green \ index_{i} = pixel_{non-zero}/pixel_{total} * 100$$   

The following code is to perform above step:   
```python
import warning
import cv2

warnings.filterwarnings('ignore')

lower_green = (40, 45, 30)
upper_green = (177, 177, 177)

green_indices = []

for i, n in enumerate(os.listdir()):
  lng, lat = i.split(sep=' ')
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

  green_indices.append([lng, lat, green_index])

green_indices = pd.DataFrame(green_indices, columns = ['Longitude', 'Latitude', 'Green Index'])
green_indices.to_csv('Write your save path',index=False,encoding='utf-8-sig')
```   
From this step, we can obtain the street greenness in the view of pedestrian.     
It can be tested with images from the *'GSV IMAGE'* folder, and the resulting image is stored in the *'IMAGE'* folder.   

<p align="center">
  <img src = "/IMAGE/128.831857 35.090245 2017 11.jpg" width = "100%"> <br>
  Figure 2. Visualization of street greenness in the view of pedestrian
</p>

## Spatial Interpolation
Spatial interpolation step can be utilized to remedy the uneven spatial distribution of GSV images.   
To implement the spatial interpolation method, refer to the sample data file named *'Data.csv'* and *Street Greenness.csv*.    
The columns required to effectively manage the green index are as follows:   

*Data.csv*
- x: Longitude in the Cartesian coordinate system
- y: Latitude in the Cartesian coordinate system
   
*Street Greenness.csv*
- Longitude: Longitude of GSV image
- Latitude: Latitude of GSV image
- Green Index: Calculated street greenness

Spatial interpolation requires the distance between two objects based on longitude and latitude. It can be obtained by using haversine formula as follows:
$$d_{\text{haversine}} = 2 \times R \times \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{lat}_p) \cos(\text{lat}_g) \sin^2\left(\frac{\Delta \text{lng}}{2}\right)}\right)$$
   
<p align="center">
  <img src = "/README_image/spatial interpolation.png" width = "60%"> <br>
  Figure 3. Graphical description of spatial interpolation
</p>   

The following code uses above mathematical form and aggregates the green index with 50 images closest to the transaction point. The final result file is in *Green Index_Spatial Interpolation.csv*
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

  # Extract the 50 nearest green indices
  dis_df_50 = dis_df.iloc[:50]

  mean_hgvi_50 = dis_df_50['HGVI'].mean()
  mean_dis_50 = dis_df_50['distance'].mean()

  Aggregated_Green_Index.append(mean_hgvi_50)
  Aggregated_Green_Index_Distance.append(mean_dis_50)

data_df['Green Index'] = Aggregated_Green_Index
data_df['Green Index_d'] = Aggregated_Green_Index_Distance
data_df.to_csv('Write your path',index=False,encoding='utf-8-sig')
```
