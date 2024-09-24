from PIL import Image
import os
import json
import piexif

def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img.info.get('exif')
            if exif_data:
                exif_dict = piexif.load(exif_data)
                image_location = exif_dict.get('GPS', {})
                camera_info = exif_dict.get('0th', {})
            else:
                print(f"No EXIF data found for {image_path}")
                image_location = {}
                camera_info = {}

            # Attempt to get image location using Pillow
            img_location = img.info.get('gps_info', {})
            if img_location:
                image_location.update(img_location)

            metadata = {
                "image_name": os.path.basename(image_path),
                "size": img.size,
                "mode": img.mode,
                "image_location": image_location,
                "camera_info": camera_info,
                # Add more metadata fields as needed
            }
            return metadata
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def process_images(directory_path):
    image_data = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(directory_path, filename)
            metadata = get_image_metadata(image_path)
            if metadata:
                image_data.append(metadata)

    return image_data

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    # Set your image directory path
    image_directory = "Resized"

    # Process images and get metadata
    images_metadata = process_images(image_directory)

    # Save metadata to JSON file
    save_to_json(images_metadata, "images.json")

    print("Image metadata saved to images.json")
