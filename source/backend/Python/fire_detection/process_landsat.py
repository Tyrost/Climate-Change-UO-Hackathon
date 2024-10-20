import json
import os
import tarfile
import sys
import os
import json
import pdb
import numpy as np
import tiffile
import pyproj
import time
import matplotlib.pyplot as plt
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search(lat,lon,start_date,end_date,cloud_cover=10):
    username = os.getenv('EE_USERNAME')
    password = os.getenv('EE_PASSWORD')
    api = API(username, password)

    # Landsat 8 Collection 2 Level 1	landsat_ot_c2_l1
    # Landsat 8 Collection 2 Level 2	landsat_ot_c2_l2
    # Landsat 9 Collection 2 Level 1	landsat_ot_c2_l1
    # Landsat 9 Collection 2 Level 2	landsat_ot_c2_l2
    
    scenes = api.search(
        dataset='landsat_ot_c2_l2',
        latitude=lat,
        longitude=lon,
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=cloud_cover
    )
    print(f'{len(scenes)} scenes found. in search')
    return scenes

def login():
    username = os.getenv('EE_USERNAME')
    password = os.getenv('EE_PASSWORD')
    ee = EarthExplorer(username, password)
    return ee

def download_scene(ee,scene_id,output_dir):
    try: 
        ee.download(scene_id, output_dir=output_dir)
        print('{} succesful'.format(scene_id))    
    except:
        if os.path.isfile('./'+output_dir+'/{}.tar'.format(scene_id)):
            print('{} error but file exists'.format(scene_id))
        else:
            print('{} error'.format(scene_id))

def open_landsat(in_file,lat,lon,pixels):
    if not os.path.exists(in_file):
        raise FileNotFoundError(f"The file {in_file} does not exist.")
    
    if not tarfile.is_tarfile(in_file):
        raise tarfile.ReadError(f"The file {in_file} is not a valid tar archive.")
    
    basename=os.path.basename(in_file).replace('.tar','')
    tar = tarfile.open(in_file, 'r:*')
    
    meta_data=json.load(tar.extractfile(basename+'_MTL.json'))
    pr=pyproj.Proj(proj='utm', zone= meta_data['LANDSAT_METADATA_FILE']['PROJECTION_ATTRIBUTES']['UTM_ZONE'],
                   ellps=meta_data['LANDSAT_METADATA_FILE']['PROJECTION_ATTRIBUTES']['ELLIPSOID'],
                   preserve_units=True)
#    print(lon,lat)
    x,y=pr(lon,lat)
    res=float(meta_data['LANDSAT_METADATA_FILE']['PROJECTION_ATTRIBUTES']['GRID_CELL_SIZE_REFLECTIVE'])
    
    central_pixel_x=  (x-float(meta_data['LANDSAT_METADATA_FILE']['PROJECTION_ATTRIBUTES']['CORNER_UL_PROJECTION_X_PRODUCT']))/res
    central_pixel_y=  (float(meta_data['LANDSAT_METADATA_FILE']['PROJECTION_ATTRIBUTES']['CORNER_UL_PROJECTION_Y_PRODUCT'])-y)/res


    
    out_data={}
    for in_file in tar:
        if in_file.isfile() and in_file.name.endswith('.TIF'):
            coords_x=(int(central_pixel_x-pixels/2), int(central_pixel_x+pixels/2))
            coords_y=(int(central_pixel_y-pixels/2), int(central_pixel_y+pixels/2))
#            print(coords_x,coords_y)

            c = tar.extractfile(in_file)#.read()
            img=tiffile.imread(c)
            # print("img shape")
            # print(img.shape)
            out_data[in_file.name.replace(basename,'').strip('_').replace('.TIF','')] =img[coords_y[0]:coords_y[1],coords_x[0]:coords_x[1]]


    return out_data

