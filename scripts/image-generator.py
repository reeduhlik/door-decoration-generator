import os
import random
from PIL import Image

def combine_images(dir_a, dir_b, dir_c):
    # Ensure output directory exists
    os.makedirs(dir_c, exist_ok=True)

    # Get list of images in both directories
    images_a = sorted([f for f in os.listdir(dir_a) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))], key=lambda x: os.path.getmtime(os.path.join(dir_a, x)))
    images_b = [f for f in os.listdir(dir_b) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    for img_a_name in images_a:
        # Randomly select an image from directory B
        img_b_name = random.choice(images_b)

        # Open images
        img_a = Image.open(os.path.join(dir_a, img_a_name))
        img_b = Image.open(os.path.join(dir_b, img_b_name))

        # Resize image A
        new_height = 72
        aspect_ratio = img_a.width / img_a.height
        new_width = int(new_height * aspect_ratio)
        img_a_resized = img_a.resize((new_width, new_height), Image.LANCZOS)

        # Create a new image with the size of image B
        result = Image.new('RGBA', img_b.size, (0, 0, 0, 0))

        # Paste image B
        result.paste(img_b, (0, 0))

        # Calculate position for image A (40 pixels from the bottom)
        position = ((img_b.width - new_width) // 2, img_b.height - new_height - 4)

        # Paste resized image A
        result.paste(img_a_resized, position, img_a_resized)

        # Save the result
        output_path = os.path.join(dir_c, f"combined_{img_a_name}")
        result.save(output_path)

        print(f"Saved combined image: {output_path}")

# Usage
dir_a = "./door-decs"
dir_b = "./name-fonts"
dir_c = "./finaldecs"

combine_images(dir_b, dir_a, dir_c)