import pandas as pd

# load all csv
anime = pd.read_csv("./all_images_anime.csv")
fantasy = pd.read_csv("./all_images_fantasy.csv")
imagenet = pd.read_csv("./all_images_imagenet.csv")
landscape = pd.read_csv("./all_images_landscape.csv")
nga = pd.read_csv("./all_images_nga.csv")

df = pd.concat([anime, fantasy, imagenet, landscape, nga])

def relative_path(row, color):
    if row['type'] == 'anime':
        return f"./anime/{color}/"

    elif row['type'] == 'fantasy':
        return f"./fantasy/{color}/"

    elif row['type'] == 'imagenet':
        return f"./imagenet/{color}/"

    elif row['type'] == 'landscape':
        return f"./landscape/{color}/"

    elif row['type'] == 'paintings':
        return f"./arts/nga/{color}/"

    else:
        print("something is wrong....")

df['color_path'] = df.apply (lambda row: relative_path(row, "color"), axis=1)
df['grey_path'] = df.apply (lambda row: relative_path(row, "grey"), axis=1)

df.to_csv("./all_images.csv", index=False)