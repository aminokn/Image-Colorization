import re
import requests
from tqdm import tqdm
import os
from urllib.parse import urlparse


def run_batch(filepath, storepath, start_counter=0, all_images={}):
    """
    extract link from a html page (in text format) and 
    store all discovered images 
    Arguments:
        filepath: path to html page in text
        storepath: path to store the discovered images
        start_counter: start number of image name, default 0
        all_images: images want to exclude, default empty set
    Returns:
        all_images: a set of all extracted and stored images name
        counter: current counter status
    """
    with open(filepath, 'r') as text_file:
        content = text_file.read()

        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)

        links = re.findall(link_regex, content)
        links = [x[0] for x in links if ('.jpg' in x[0] or 'jpeg' in x[0] or 'png' in x[0])][1:]
        new_links = links[::-1]

        def parse_link(link):
            symbols = link.replace('&quot', '').replace(';', '').replace(')', '').replace('(', '')
            return symbols

        def extract_image_name(link):
            '''extract image name from link'''
            a = urlparse(link)
            return os.path.basename(a.path)

        all_images = set()
        counter = start_counter

        for i in tqdm(range(len(new_links))):
            parsed_link = parse_link(new_links[i])
            filename = extract_image_name(parsed_link)[:-4]

            # check whether we had saved images
            if (filename not in all_images):

                all_images.add(filename)

                img_data = requests.get(parsed_link).content
                image_name = storepath + str(counter) + parsed_link[-4:]

                # check the size of the image, if too small, might be user avatar
                if (len(img_data) > 11000):
                    with open(image_name, 'wb') as handler:
                        handler.write(img_data)
                    
                    counter += 1

    return all_images, counter


image_set, counter = run_batch("pictures.txt", "./fantasy_worlds/", 0, {})
image_set, counter = run_batch("pictures2.txt", "./fantasy_worlds/", counter+1, image_set)
image_set, _ = run_batch("pictures3.txt", "./fantasy_worlds/", counter+1, image_set)

with open('all_images.txt','w') as f:
   f.write(str(image_set))