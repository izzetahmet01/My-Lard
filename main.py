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


degree = 10
ICAO_CODE = "UBBB"

# for alpha in range(0,degree + 1,10):
#     print(alpha)
#     gerenate_scenario_from_params(DATABASE_PATH,ICAO_CODE,alpha,f"{ICAO_CODE}{alpha}")

# for alpha in range(180 - degree,180,10):
#     print(alpha)
#     gerenate_scenario_from_params(DATABASE_PATH,ICAO_CODE,alpha,f"{ICAO_CODE}{alpha}")

# for alpha in range(180 ,180+ degree + 1,10):
#     print(alpha)
#     gerenate_scenario_from_params(DATABASE_PATH,ICAO_CODE,alpha,f"{ICAO_CODE}{alpha}")
gerenate_scenario_from_params(DATABASE_PATH,ICAO_CODE,0,f"{ICAO_CODE}{10}")

gather_files(r"C:\Users\STAJYER\Desktop\Codes\RunWay\LARD\scenarios")