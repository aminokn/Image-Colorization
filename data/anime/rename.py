import os
import pandas as pd
import numpy as np

def rename(folder):
    all_image_name = []
   
    for _, filename in enumerate(os.listdir(folder)):
        filenum, extension = os.path.splitext(filename)

        if (not filename.startswith("._")) and (not filename.startswith("people_")):
            # target_name = filenum.replace("people_", "")
            dst = f"{filenum}{extension}"
            src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
            dst =f"{folder}/{dst}"

            all_image_name.append(dst)

            # rename() function will rename all the files
            try:
                os.rename(src, dst)
            except:
                import pdb; pdb.set_trace()
                print()

    return all_image_name

result = rename("./color")
result = [x.replace("./color/", "") for x in result]

# make a csv of the selected sample: image_name, category
new_df = pd.DataFrame(np.array(result), columns=['image_name'])
new_df['type'] = "anime"
new_df.to_csv("./all_images.csv", index=False)