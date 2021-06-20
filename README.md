## Larger Google Sat2Map dataset

This dataset extends the aerial &#10231; Maps dataset used in [pix2pix (Isola et al., CVPR17)](https://arxiv.org/abs/1611.07004).
The provide script ` download_sat2maps.py` scrapes pairs of matching Maps and Satellite images using the Google Maps API from the 22 most populous cities in the United States. 

Following pix2pix, the pair of satellite and map images are concatenated side-by-side into one image like below.

![Houston](./samples/000002_Houston_29.62732_-95.41556.png?raw=true)

![Charlotte](./samples/000008_Charlotte_35.19615_-80.94875.png?raw=true)

![Indianapolis](./samples/000019_Indianapolis_39.78022_-86.16545.png?raw=true)

Occasionally, the satellite or the map image are not provided by the API, or simply not interesting like entirely water or forest. 
`prune_out_uninteresting_regions.py` prunes away these uninteresting regions using simple thresholding on the standard deviation on the color distribution of the Map images. 

Using this script, an example dataset of roughly 100k images were gathered and pruned, and it can be downloaded from [this link](http://efrosgans.eecs.berkeley.edu/datasets/larger_sat2maps_cleaned.tar). 
The samples were random split into train / val set of size 92376 / 275. Since the coordinates of each image are randomly and independently sampled, it is possible that there exists overlap between the splits. 

