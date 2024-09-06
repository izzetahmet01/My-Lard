from utils import * 
import os

DATABASE_PATH = r'C:\Users\STAJYER\Desktop\Codes\RunWay\LARD\data\runways_database.json'
ICAO_PATH = r"C:\Users\STAJYER\Desktop\Codes\RunWay\LARD\ICAO_and_coordinatesV2.json"
SCENARIO_PATH = r"C:\Users\STAJYER\Desktop\Codes\RunWay\LARD\scenarios"
VIDEO_PATH = rf"C:\Users\STAJYER\Desktop\Codes\RunWay\LARD\Videos"


# # read_and_create_scenario(DATABASE_PATH,  ICAO_PATH,alpha_deg= 0 , file_name= "")

# for dataset_name in os.listdir(SCENARIO_PATH):
#     print("Processing : ",dataset_name)
#     csv_file = os.path.join(SCENARIO_PATH,dataset_name,dataset_name,"exported_labels.csv")
#     exported_file = os.path.join(SCENARIO_PATH,dataset_name,dataset_name,"exported_images")
#     bbox_folder =  os.path.join(SCENARIO_PATH,dataset_name,dataset_name,"bbox_images")  


#     print("Moves yaml to correct directory")
    
#     shutil.move(os.path.join(SCENARIO_PATH,dataset_name,str(dataset_name + ".yaml")),os.path.join(SCENARIO_PATH,dataset_name,dataset_name))
    
#     print("Converts labels")
#     crete_labels(os.path.join(SCENARIO_PATH,dataset_name,dataset_name,str(dataset_name + ".yaml")))

#     print("Draws boundary points to images")
#     draw_boundary_boxes(csv_file,bbox_folder,exported_file)
#     create_video_from_images(bbox_folder,VIDEO_PATH, fps = 3) 


