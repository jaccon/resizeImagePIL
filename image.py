import os
import json
from PIL import Image

# read configurations
with open('config.json', 'r') as file:
    data = json.load(file)

config = data[0]  

def resize_images_with_original_rotation(input_dir, output_dir, new_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            original_rotation = 0
            if hasattr(image, '_getexif') and image._getexif() is not None:
                exif_data = image._getexif()
                if 274 in exif_data:
                    orientation = exif_data[274]
                    if orientation == 3:
                        original_rotation = 180
                    elif orientation == 6:
                        original_rotation = 270
                    elif orientation == 8:
                        original_rotation = 90

            image.thumbnail(new_size, Image.ANTIALIAS)
            image = image.rotate(original_rotation, expand=True)
            output_path = os.path.join(output_dir, filename)
            image.save(output_path)
            print("Resized image with original rotation saved to:", output_path)

# execute
source =  config['sourceDirectory']
destination =  config['destinationDirectory']
width = int(config['resizeWidth'])
height = int(config['resizeHeight'])
new_size = (width, height)

resize_images_with_original_rotation(source, destination, new_size)
