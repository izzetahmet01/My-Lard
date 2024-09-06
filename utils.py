import json
import numpy as np
import os
from pathlib import Path
import pandas as pd 
import cv2 
import matplotlib.pyplot as plt
from src.scenario.write_scenario import write_scenario
from src.scenario.scenario_config import ScenarioConfig
from src.ges.ges_dataset import add_or_update_runways
from src.labeling.earth_studio_export import export_labels
from src.dataset.lard_dataset import LardDataset
import requests
import time 
from natsort import natsorted
import shutil
import csv

def get_elevation(latitude,longitude):
    # Define the URL without API key, since it's included in the payload now
    url = 'https://content-earthengine.googleapis.com/v1/projects/ee-izzetahmet216/value:compute?key=AIzaSyCIdO53SBE0yrw3mmxBnfF3HeIIj316gA0'

    # Define the headers
    headers = {
        'Authorization': 'Bearer ya29.a0AcM612xm0uMDvjMNWmkLVAPRRVqUVrdCOYN5MRIyrnrYSgKWBkn3UOfR6-kRx8_hgtcIJC8AczMtz26iGw_K7Lj7u5XaWudDI9g-jroGPReV3UQdxdoAPE6dyOA61PUu8pRhFf1AsZNAmtnJmgRxVkvbyefGJRM0E0W-n9CNNLpzCgaCgYKARwSARESFQHGX2MiAZagQxYs_3nlYnaVGrqbVA0181',
        'Content-Type': 'application/json',
        'Origin': 'https://code.earthengine.google.com',
        'Referer': 'https://code.earthengine.google.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'X-Client-Data': 'CJW2yQEIpbbJAQipncoBCOmIywEIkqHLAQic/swBCIWgzQEI3PzNAQjkr84BCMS2zgEI2rfOAQi8uc4BGPbJzQEYua7OARidsc4B',
        'X-Goog-Api-Client': 'ee-js/latest',
        'X-Goog-User-Project': 'ee-izzetahmet216',
        'Priority': 'u=1, i'
    }

    # Define the payload (body) of the request, including API key
    payload = {
        "expression": {
            "result": "0",
            "values": {
                "0": {
                    "functionInvocationValue": {
                        "arguments": {
                            "dictionary": {
                                "functionInvocationValue": {
                                    "arguments": {
                                        "image": {
                                            "functionInvocationValue": {
                                                "arguments": {
                                                    "id": {
                                                        "constantValue": "USGS/SRTMGL1_003"
                                                    }
                                                },
                                                "functionName": "Image.load"
                                            }
                                        },
                                        "reducer": {
                                            "functionInvocationValue": {
                                                "arguments": {},
                                                "functionName": "Reducer.first"
                                            }
                                        },
                                        "geometry": {
                                            "functionInvocationValue": {
                                                "arguments": {
                                                    "coordinates": {
                                                        "constantValue": [latitude,longitude]
                                                    }
                                                },
                                                "functionName": "GeometryConstructors.Point"
                                            }
                                        },
                                        "scale": {
                                            "constantValue": 30
                                        },
                                        "maxPixels": {
                                            "constantValue": 1000000000
                                        }
                                    },
                                    "functionName": "Image.reduceRegion"
                                }
                            },
                            "key": {
                                "constantValue": "elevation"
                            },
                            
                        },
                        "functionName": "Dictionary.get"
                    }
                }
            }
        }
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Print the response
    #print(response.status_code)
    #print(response.json())
    return response.json()



def gather_files(scenario_path :str ):
    """
    Gather all same named esp and yaml files in same folder 
    """
    # List all files in the directory
    files = os.listdir(scenario_path)

    # Process each file
    for file in files:
        # Get the file's base name without the extension
        if file.endswith(('.esp', '.yaml')):
            base_name = os.path.splitext(file)[0]
            
            # Create a new directory with the base name if it doesn't exist
            folder_path = os.path.join(scenario_path, base_name)
            os.makedirs(folder_path, exist_ok=True)
            
            # Move the file into the corresponding folder
            shutil.move(os.path.join(scenario_path, file), os.path.join(folder_path, file))

    print("Files have been organized into their respective folders.")

def gerenate_scenario_from_params(DATABASE_PATH :str ,airport_ICAO_code :str, alpha_deg :int,file_name : str ):
    """
    Generates scenarios from default parameters
    """
    with open(DATABASE_PATH, 'r') as f:
        runways_database = json.load(f)

    output_directory = Path("scenarios/") # Creation of the scenario output if needed directory

    for runway in runways_database[airport_ICAO_code]: 
        conf = ScenarioConfig(airport_ICAO_code, [runway], scenario_dir= output_directory, file_name = file_name)
        conf.sample_number = 500
        
        conf.month_max = 7
        conf.month_min = 7
        conf.day_max = 1
        conf.day_min = 1
        conf.hour_max = 20
        conf.hour_min = 20
        conf.minute_max = 0
        conf.minute_min = 0    

        conf.alpha_h_deg = alpha_deg
        conf.alpha_v_deg = -3
        conf.dist_ap_m = 300.0
        conf.pitch_deg = -4
        conf.roll_deg = 10
        conf.yaw_deg = alpha_deg

        conf.std_alpha_h_deg = 0
        conf.std_alpha_v_deg = 0
        conf.std_pitch_deg = 0
        conf.std_roll_deg = 0
        conf.std_yaw_deg = 0

        conf.width = 1920
        conf.height = 1080
        conf.watermark_height = None
        
        # Distance to runway parameters
        conf.max_distance_m  = 10000 # Default value corresponding to 3 Nautical Mile
        conf.min_distance_m  = 300

        # Distribution used for the distances from the runway (details in generate_dist in src/ges/ges_dataset)
        conf.distrib_param   = 1
        conf.distribution    = "uniform"   
        
        # Scenario generation
        write_scenario(conf)


def crete_labels(yaml_file_path = str):
    """
    This creates csv file from yaml file that created while scenario generation
    """
    export_labels(Path(yaml_file_path))

def draw_boundary_boxes(csv_file: str, output_dir: str, images_dir: str):
    """
    Draw boundary boxes from given csv file to images in images_dir.
    Each point is drawn with a different color.
    """   

    df = pd.read_csv(csv_file, delimiter=";")
    os.makedirs(output_dir, exist_ok=True)

    # Define colors for the points
    colors = [(0, 0, 255),   # Red
              (0, 255, 0),   # Green
              (255, 0, 0),   # Blue
              (0, 255, 255)] # Yellow

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Load the image
        image_path = os.path.join(images_dir, row['image'].split("\\")[-1])  # Assuming the CSV has an 'image' column with image paths
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_path}")
            continue

        # Extract the coordinates
        points = [(row['x_A'], row['y_A']),
                  (row['x_B'], row['y_B']),
                  (row['x_C'], row['y_C']),
                  (row['x_D'], row['y_D'])]

        # Draw points on the image with different colors
        for i, point in enumerate(points):
            cv2.circle(image, point, radius=5, color=colors[i % len(colors)], thickness=3)

        # Save the modified image
        output_path = os.path.join(output_dir, f"{index}.jpg")
        cv2.imwrite(output_path, image)

        print(f"Saved: {output_path}")

# Crates DB from json file
def read_and_create_scenario(DATABASE_PATH :str , ICAO_PATH_JSON : str, alpha_deg, file_name ):
    """
    This function takes database path and ICAO json files as input and creates database from ICAO json file 
    It also generates scenarios from default paramters placed in gerenate_scenario_from_params function 
    

    !!! Using "1" as a default runway. You can change runway id and coordinates and create different landing simulations
    """
    # Read the JSON file
    with open(ICAO_PATH_JSON, 'r') as file:
        icao_database = json.load(file)

    for airport_ICAO_code in icao_database.keys():
        add_or_update_runways(DATABASE_PATH, airport_ICAO_code,  ["1"], np.array(icao_database[airport_ICAO_code]))
        print(airport_ICAO_code , " : " , icao_database[airport_ICAO_code] )
        print("Added To Database!!!\n")
        gerenate_scenario_from_params(DATABASE_PATH,airport_ICAO_code, alpha_deg, file_name )
        print(f"{airport_ICAO_code} Scenario Created!!!\n")

    
    gather_files("scenarios") 

def create_video_from_images(image_folder, video_name, fps=30):
    # Get list of all image files in the directory with .jpeg extension
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpeg") or img.endswith(".jpg")]
    
    # Sort the images in natural order
    images = natsorted(images)
    
    # Read the first image to get dimensions
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'XVID', 'DIVX', etc.
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Iterate over all images and write them to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release the VideoWriter object
    video.release()
    print(f"Video saved as {video_name}")




def csv_to_coco(csv_file_path,output_coco_json_path ):
    # Initialize the COCO dictionary structure
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Since your CSV does not have category information, assume a single category for now
    category_id = 1
    coco_format["categories"].append({
        "id": category_id,
        "name": "object",  # change this according to your label
        "supercategory": "none"
    })

    annotation_id = 1

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file,delimiter = ";" )
        for i, row in enumerate(csv_reader):
            image_id = i + 1
            image_path = row['image']
            height = int(row['height'])
            width = int(row['width'])

            # Add image info
            coco_format["images"].append({
                "id": image_id,
                "file_name": os.path.basename(image_path),
                "height": height,
                "width": width
            })

            # Calculate bounding box [x, y, width, height] from the points
            x_coords = [float(row['x_A']), float(row['x_B']), float(row['x_C']), float(row['x_D'])]
            y_coords = [float(row['y_A']), float(row['y_B']), float(row['y_C']), float(row['y_D'])]
            category_id = row["airport"]
            x_min = min(x_coords)
            y_min = min(y_coords)
            bbox_width = max(x_coords) - x_min
            bbox_height = max(y_coords) - y_min

            bbox = [x_min, y_min, bbox_width, bbox_height]

            # Add annotation info
            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": bbox,
                "area": bbox_width * bbox_height,
                "iscrowd": 0
            })
            
            annotation_id += 1

    # Save the COCO JSON
    with open(output_coco_json_path, 'w') as json_file:
        json.dump(coco_format, json_file, indent=4)

    print(f"COCO format JSON saved at {output_coco_json_path}")
