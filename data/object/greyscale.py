'''
Loop through all avalible colored images and write grayscaled image in grey folder
'''

import os
src_directory = './color/'
dst_directory = './grey/'
from PIL import Image
 
# iterate over all colored images 
for filename in os.listdir(src_directory):
    f = os.path.join(src_directory, filename)
    try:
        # checking if it is a file
        if os.path.isfile(f) and (not filename.startswith("._")):
            img = Image.open(f).convert('L')
            img.save(dst_directory+filename)

    except:
        print(f"{filename} failed.")