# Green Index Data Records   
<img src="https://img.shields.io/badge/Google Colab-F9ABOO?style=for-the-badge&logo=Google Colab&logoColor=white" link='https://colab.google/'> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">  
We devised the new index called 'Green Index', based on street image in Busan in 2017 and 2018. 

To derive the green index, we went through the process of collecting GSV images, converting to HSV, calculating green index, and spatial interpolation.
  
This four-step process is necessary to effectively implement the green index, and for a detailed explanation, please refer to the [paper](https://doi.org/10.1038/s41598-023-49845-0), and sample data was stored in the 'data' folder to facilitate this implementation.   

Data in this repository concists of CSV and Excel files:   

- *Data.csv*: Location of transaction sample data
- *Green.csv*: Roadside trees location and green index sample data
- *Green Index.csv*: Final green index using spatial interpolation method

## Image Preprocessing
In order to calculate the green index, it is necessary to convert GSV images to HSV images:    

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
  

```

## Calculating Green Index
The codename **OOO** is a code that calculates the green index with the HSV image as follows:

$$Green \ index_{i} = pixel_{non-zero}/pixel_{total} * 100$$   

From this step, we can extract the pure greenness from the pedestrian's point of view.

## Spatial Interpolation
The filename **OOO** is a dataset collected from hedonic variables used to estimate property prices. What each column means can be seen in detail through the paper as well.   

The columns required to effectively manage the green index are as follows:   
- x: Longitude in the Cartesian coordinate system
- y: Latitude in the Cartesian coordinate system
- HGVI: The degree of street greenness from the pedestrian perspective

The mathematical form of haversine formula is implemented by **OOO** as follows:
$$d_{\text{haversine}} = 2 \times R \times \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{lat}_p) \cos(\text{lat}_g) \sin^2\left(\frac{\Delta \text{lng}}{2}\right)}\right)$$

## Green Indices' Spatial Distribution   
[The pydeck library](https://pydeck.gl/) (version 0.8.0) is a set of Python binding for making spatial visualizations. We used these library for visualization of interpolated green indices and roadside trees in Busan.   

<img src = "/README_image/green_index.png" width = "60%">   

Each white circle indicates the location of roadside tree and the cuboid represents each green index calculated for the property transaction points. The more greenness has the higher height of cuboid. The sample dataset is in the filenamed **OOO**.  
The related code was wirtten based on the colab and the relevant libraries and code details were detailed in the codename ```spatial_distribution.py```.   
