import os
from jinja2 import Template
import datetime

def get_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(root, file))
    return image_files

def generate_html(image_dir):
    # Get the list of image files in the specified directory and its subdirectories
    image_files = get_image_files(image_dir)

    # Order the images based on creation time
    image_files.sort(key=lambda x: os.path.getctime(x))

    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Display loader while processing images
    print("Generating HTML document. Please wait...")

    # Read the HTML template
    template_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }

            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-start; /* Align elements to the left */
                margin: 20px;
            }

            .gallery div {
                width: 200px;
                height: 200px;
                overflow: hidden;
                margin: 10px;
                position: relative;
            }

            .gallery img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                cursor: pointer;
                transition: transform 0.3s;
            }

            .gallery img:hover {
                transform: scale(1.1);
            }

            .loader {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                display: none;
            }

            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.9);
                justify-content: center;
                align-items: center;
            }

            .modal img {
                width: 80%;
                height: auto;
                max-width: 800px;
                cursor: pointer;
                transition: transform 0.3s;
            }

            .modal img:hover {
                transform: scale(1.1);
            }

            .close {
                position: absolute;
                top: 15px;
                right: 15px;
                color: #fff;
                font-size: 30px;
                cursor: pointer;
            }

            .prev, .next {
                position: absolute;
                top: 50%;
                font-size: 20px;
                color: #fff;
                cursor: pointer;
                transform: translateY(-50%);
            }

            .prev {
                left: 15px;
            }

            .next {
                right: 15px;
            }
        </style>
    </head>
    <body>

    <div class="gallery" id="imageGallery">
        {% for image in images %}
        <div onclick="openModal('{{ image }}')">
            <img src="{{ image }}" alt="Image {{ loop.index }}">
        </div>
        {% endfor %}
    </div>

    <div class="loader" id="loader">Loading...</div>

    <div id="myModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <span class="prev" onclick="changeImage(-1)">&#10094;</span>
        <span class="next" onclick="changeImage(1)">&#10095;</span>
        <img id="modalImage" class="modal-content">
    </div>

    <script>
        let currentImageIndex = 0;
        const images = [
            {% for image in images %}
            '{{ image }}',
            {% endfor %}
        ];

        function openModal(imageSrc) {
            currentImageIndex = images.indexOf(imageSrc);
            document.getElementById('modalImage').src = imageSrc;
            document.querySelector('.modal').style.display = 'flex';
        }

        function closeModal() {
            document.querySelector('.modal').style.display = 'none';
        }

        function changeImage(direction) {
            currentImageIndex += direction;
            if (currentImageIndex < 0) {
                currentImageIndex = images.length - 1;
            } else if (currentImageIndex >= images.length) {
                currentImageIndex = 0;
            }
            document.getElementById('modalImage').src = images[currentImageIndex];
        }

        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            if (document.querySelector('.modal').style.display === 'flex') {
                if (event.key === 'ArrowLeft') {
                    changeImage(-1);
                } else if (event.key === 'ArrowRight') {
                    changeImage(1);
                } else if (event.key === 'Escape') {
                    closeModal();
                }
            }
        });

        // Hide the loader once the images are loaded
        window.onload = function() {
            document.getElementById('loader').style.display = 'none';
        };
    </script>

    </body>
    </html>
    """

    # Render the template with the image files and current date/time
    rendered_template = Template(template_content).render(images=image_files)

    # Write the generated HTML to a new file
    output_filename = f"gallery-{current_datetime}.html"
    with open(output_filename, 'w') as output_file:
        output_file.write(rendered_template)

    print(f"HTML document '{output_filename}' generated successfully.")

# Specify the directory containing the images
image_dir = "Resized"

generate_html(image_dir)
