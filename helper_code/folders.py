import os 
from datetime import datetime 

# All these scripts depened on the main program changing the current working directory

def create_month_day_folder(): 
	today = datetime.today() 
	folder = "./" + str(today.month) + "_" + str(today.day)		
	if os.path.exists(folder) and os.path.isdir(folder):
		print("Folder exists")
	else: 
		os.mkdir(folder) 

	return folder

#looks like the above funcion but if i did them in the same function then you would have an extra os function call and more confusing code	
#create_electrode_folder gets claled every time you do a test. create_month_day_folder gets called when the program starts

def create_electrode_folder(electrode_name): 
	today = datetime.today()	
	month_day_folder = str(today.month) + "_" + str(today.day)
	folder =  "./" + electrode_name	 
	if os.path.exists(folder) and os.path.isdir(folder):
		print("electrode file exits")
	else: 
		os.mkdir(folder) 
	
	return folder

def create_new_test_set_folder(test_type): 
	number_of_folders =  sum(os.path.isdir(item) for item in os.listdir("."))
	folder = "./Test_Set_" + str(number_of_folders) "_" + test_type

	if os.path.exists(folder) and os.path.isdir(folder):
		print("Test set folder already exists")
	else:
		os.mkdir(folder) 

	return folder

