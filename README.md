# Green Index Data Records   
We devised the new index called 'Green Index', based on street image in Busan in 2017 and 2018.   
Four-step process is necessary to effectively implement the green index, and for a detailed explanation, please refer to the paper(https://doi.org/10.1038/s41598-023-49845-0), and sample data was stored in the 'data' folder to facilitate this implementation.   

Data in this repository concists of CSV and Excel files:   

<span style = "background-color: #f6f8fa">busan201819.csv --> 관련 샘플 파일들 쓰기</span>

## Image Preprocessing
In order to calculate the green index, it is necessary to convert GSV images to HSV images.   

## Calculating Green Index
The codename '' is a code that calculating green index as follows: 

$$Green \ index_{i} = pixel_{non-zero}/pixel_{total} * 100$$   

From this step, we can extract the pure greenness from the pedestrian's point of view.

## Spatial Interpolation
The filename 'busan201819.csv' is a dataset collected from hedonic variables used to estimate property prices. What each column means can be seen in detail through the paper as well.   

The columns required for generating the green index are as follows:   
- x: Longitude in the Cartesian coordinate system
- y: Latitude in the Cartesian coordinate system

The mathematical form of haversine formula is implemented by 'ㅇㅇㅇ' as follows:
$$d_{\text{haversine}} = 2 \times R \times \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{lat}_p) \cos(\text{lat}_g) \sin^2\left(\frac{\Delta \text{lng}}{2}\right)}\right)$$

## Green Indices' Spatial Distribution   
The pydeck library is a set of Python binding for making spatial visualizations (https://pydeck.gl/). We used these library for visualization of interpolated green indices and roadside trees in Busan.   

<img src = "/README_image/green_index.png" width = "60%">   

Each white circle indicates the location of roadside tree and the cuboid represents each green index calculated for the property transaction points. The more greenness has the higher height of cuboid. The sample dataset is in    
The related code was wirtten based on the colab.   
