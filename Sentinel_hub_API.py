import geopandas as gpd
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, bbox_to_dimensions, BBox, CRS, MimeType
import rasterio
import os

# Set Sentinel Hub credentials
config = SHConfig()
config.sh_client_id = '4df8c1a9-3e48-47c1-baf4-e4b3e0811ef8'
config.sh_client_secret = '6f2OarP8Da41sr5boB1HWoJWZf8C3vJx'


fiona.supported_drivers['ESRI Shapefile'] = 'raw'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

time_range = ('2024-06-01', '2024-06-15')

resolution = 10  # meters


input_folder = '../Data/Grids_Final/'
output_folder = '../Data/sentinel_hub_1x1_leastCC/'

os.makedirs(output_folder, exist_ok=True)

for i, filename in enumerate(os.listdir(input_folder)):
    if filename.endswith('.shp'):
         shapefile
        shapefile_path = os.path.join(input_folder, filename)

        
        gdf = gpd.read_file(shapefile_path)

        
        if gdf.crs is None or gdf.crs == {}:
            gdf.set_crs(epsg=4326, inplace=True)

        
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs(epsg=4326)

        
        for index, row in gdf.iterrows():
            geometry = row.geometry  

            
            bbox = geometry.bounds
            bbox = BBox(bbox, crs=CRS.WGS84)

            
            size = bbox_to_dimensions(bbox, resolution=resolution)

            request = SentinelHubRequest(
                data_folder=output_folder,
                evalscript='''
                    //VERSION=3
                    function setup() {
                        return {
                            input: ["B02", "B03", "B04"],
                            output: { bands: 3, sampleType: "FLOAT32" }
                        };
                    }
                    function evaluatePixel(sample) {
                        return [sample.B04 * 2.0, sample.B03 * 2.0, sample.B02 * 2.0];
                    }
                ''',
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.SENTINEL2_L2A,
                        time_interval=time_range,
                        mosaicking_order='leastCC',
                        other_args={
                            'filters': {
                                'maxCloudCover': 5 
                            }
                        }
                    )
                ],
                responses=[
                    SentinelHubRequest.output_response('default', MimeType.TIFF)
                ],
                bbox=bbox,
                size=size,
                config=config
            )

            # Get the data
            response = request.get_data(save_data=True)

            # Save the TIFF file
            image = response[0]
            width, height = size
            transform = rasterio.transform.from_bounds(*bbox, width, height)

            # Save TIFF file with name grid_{i}.tif
            tiff_file_path = os.path.join(output_folder, f'grid_{i}.tif')
            with rasterio.open(tiff_file_path, 'w', driver='GTiff', width=width, height=height, count=3, dtype=np.float32, crs='EPSG:4326', transform=transform) as dataset:
                dataset.write(image[:, :, 0], 1)
                dataset.write(image[:, :, 1], 2)  
                dataset.write(image[:, :, 2], 3)  
            print(f"GeoTIFF saved to: {tiff_file_path}")