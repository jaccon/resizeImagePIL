from PIL import Image, ExifTags
from tqdm import tqdm
import os
import json

def resizeImages(sourceDir, destDir, targetWidth, targetHeight, compressionQuality):
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    files = os.listdir(sourceDir)
    progressBar = tqdm(files, desc="Resizing Images", unit="image")

    for file in progressBar:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            sourcePath = os.path.join(sourceDir, file)
            destPath = os.path.join(destDir, file)

            image = Image.open(sourcePath)

            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                pass

            aspectRatio = image.width / image.height
            newWidth = targetWidth
            newHeight = int(newWidth / aspectRatio)
            resizedImage = image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)

            resizedImage.save(destPath, quality=compressionQuality)

    progressBar.close()

if __name__ == "__main__":
    with open('setup.json', 'r') as configFile:
        config = json.load(configFile)

    sourceDirectory = config["source_directory"]
    destinationDirectory = config["destination_directory"]
    targetWidth = config["width"]
    targetHeight = config["height"]
    compressionQuality = config["compression_quality"]

    resizeImages(sourceDirectory, destinationDirectory, targetWidth, targetHeight, compressionQuality)

    print("Image resizing completed.")
