import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

def create_pdf_from_images(dir_c, output_pdf):
    # Get list of images in directory C
    images = sorted([f for f in os.listdir(dir_c) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))], key=lambda x: os.path.getmtime(os.path.join(dir_c, x)))

    # Set up PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    
    # Calculate image size and positions with 0.25 inch margins
    image_width = (width - 1*inch) / 2  # 1 inch for margins and spacing
    image_height = (height - 1*inch) / 2  # 1.25 inch for margins and spacing
    positions = [
        (0.25*inch, height - 0.25*inch - image_height),
        (0.25*inch + image_width + 0.5*inch, height - 0.25*inch - image_height),
        (0.25*inch, height - 0.25*inch - 2*image_height - 0.5*inch),
        (0.25*inch + image_width + 0.5*inch, height - 0.25*inch - 2*image_height - 0.5*inch)
    ]
    
    for i, img_name in enumerate(images):
        if i % 4 == 0 and i != 0:
            c.showPage()  # Start a new page
        
        img = Image.open(os.path.join(dir_c, img_name))
        
        # Add white background if the image has an alpha channel
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background.convert('RGB')
        
        img_width, img_height = img.size
        aspect = img_width / img_height
        
        # Calculate dimensions to fit within the allocated space while preserving aspect ratio
        if aspect > image_width / image_height:  # Image is wider
            draw_width = image_width
            draw_height = draw_width / aspect
        else:  # Image is taller
            draw_height = image_height
            draw_width = draw_height * aspect
        
        # Calculate position to center the image in its allocated space
        x, y = positions[i % 4]
        x += (image_width - draw_width) / 2
        y += (image_height - draw_height) / 2
        
        # Save the image with white background temporarily
        temp_path = os.path.join(dir_c, f"temp_{img_name}")
        img.save(temp_path)
        
        # Draw the image
        c.drawImage(temp_path, x, y, width=draw_width, height=draw_height)
        
        # Remove temporary file
        os.remove(temp_path)
    
    c.save()
    print(f"PDF created: {output_pdf}")

# Usage
dir_c = "./finaldecs"
output_pdf = "final-decs2.pdf"

create_pdf_from_images(dir_c, output_pdf)