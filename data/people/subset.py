
# import OS module
import os
from tqdm import tqdm
import shutil
 
# Get the list of all files and directories
path = "/Volumes/T7/Master 3rd Semester/Big Data Analytics/Final Project/Dataset/people/c/"
src = "/Volumes/T7/Master 3rd Semester/Big Data Analytics/Final Project/Dataset/people/c/"
dst = "/Volumes/T7/Master 3rd Semester/Big Data Analytics/Final Project/Dataset/people/color/"
dir_list = os.listdir(path)
print(dir_list[:30])

counter = 0 
for i in tqdm(range(len(dir_list))):
    if (counter % 3 == 0):
        file_name = dir_list[i]
        if (not file_name.startswith('._')):
            shutil.copyfile(src+file_name, dst+file_name)
    counter += 1
