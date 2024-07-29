
# Downscaling a Satellite Thermal Image from 1000m to 10m Processing Methodology

This repository contains the methodology for processing Sentinel data. Follow the steps outlined below to download, process, and analyze Sentinel-3 data and upscale it to 10m resolution using Sentinel-2 data.

## Steps for Processing Sentinel Data

### Step 1: Identify the Site and Download the Sentinel Data
There are different ways to download the data. Choose the one that suits you best:
- Through Sentinel API
- Using the “Copernicus DataSpace”
- Pystac

### Step 2: Unzip the Data
Unzip the downloaded data. If you use SNAP or any other Sentinel toolbox to analyze the data, ensure you keep the default file name with the respective file extension. 

**Example:** For Sentinel-3: `S3A_SL_2_LST____20231031T165315_20231031T165615_20231031T174845_0180_105_112_0360_PS1_O_NR_004.SEN3`

### Step 3: Processing with SNAP
#### Step 3(a): Processing NetCDF Files
Sentinel-3 files usually come in the NetCDF format. You can process and export them using the SNAP toolbox.

#### Step 3(b): Download SNAP
If you do not have SNAP, download it from [here](https://step.esa.int/main/download/snap-download/).

### Step 4: Load the Product in SNAP
Load the XML file of the downloaded product in SNAP. It will display all the products (bands, masks, etc.).

### Step 5: Load the Band
Load the band of your choice (LST in this case).

### Step 6: Reproject the Band
Reproject the band to a desirable projection using the reprojection tool in SNAP.

### Step 7: Export as TIFF
After reprojecting, export the layer as a .tiff file for further analysis.

## Upscaling Sentinel-3 LST Band from 1000m to 10m

Reference: [Downscaling a Satellite Thermal Image from 1000m to 10m](https://towardsdatascience.com/downscaling-a-satellite-thermal-image-from-1000-m-to-10-m-python-3b2ed19ff103)

### Step 1: Load Sentinel-2 Band
Load the Sentinel-2 band and check the CRS. Reproject the Sentinel-3 image according to the Sentinel-2 band CRS.

### Step 2: Clip the Image
Clip the reprojected Sentinel-3 image to the bounds of the Sentinel-2 image or the NDVI image. This might be memory and computation expensive. Alternatively, use GIS software to clip the image and then load it in Python for smoother processing.

### Step 3: Polygonize the Band
Polygonize the clipped LST band and store the NDVI values in the same shapefile. Fill NA values with the mean estimate using the zonal statistic tool.

### Step 4: Find Correlation
Since the upscaling is based on the correlation concept, find the slope and intercept.

### Step 5: Apply Correlation Equation
This techni
Use the correlation equation with NDVI to produce a sharp LST band image and rescale it to 10m resolution.

### Step 6: Export as Raster TIFF
Write the rescaled image as a raster TIFF file for visualization or further use.


## Acknowledgements
This methodology is based on resources and tools provided by the European Space Agency (ESA) and contributions from the open-source community.

 - Copernicus Sentinel data [2024] for Sentinel data
 - Copernicus Service information [2024] for Copernicus Service Information.
 - Agam, N., Kustas, W. P., Anderson, M. C., Li, F., Neale, C. M. U. (2007). A vegetation index-based technique for spatial sharpening of thermal imagery. Remote Sensing of Environment, 107(4), 545–558. ISSN 0034–4257.
- Gao, F., Kustas, W. P., Anderson, M. C. (2012). A Data Mining Approach for Sharpening Thermal Satellite Imagery over Land. Remote Sensing, 4, 3287–3319.
- Huryna, H., Cohen, Y., Karnieli, A., Panov, N., Kustas, W. P., Agam, N. (2019). Evaluation of TsHARP Utility for Thermal Sharpening of Sentinel-3 Satellite Images Using Sentinel-2 Visual Imagery. Remote Sensing, 11, 2304.

