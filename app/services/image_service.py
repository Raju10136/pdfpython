from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def convert_pdf_page_to_image(pdf_path, page_number):
    # Convert the specified page to an image
    images = convert_from_path(pdf_path, first_page=page_number+1, last_page=page_number+1)
    return images[0]  # There's only one image in the list

def crop_image(image, crop_box):
    # Crop the image based on the provided box
    cropped_image = image.crop(crop_box)
    return cropped_image

def save_image(image, output_path):
    # Save the image to the specified path
    image.save(output_path)
    print(f'Cropped image saved as: {output_path}')
    
# crop box calulation
def crop_box_calculation(page_width,page_height,image,obj):
     image_width, image_height = image.size
     x_scale = image_width / page_width
     y_scale = image_height / page_height
     left =int(float(obj['left']))
     height = int(float(obj['height']))
     width = int(float(obj['width']))
     top = int(float(obj['top']))
     actual_left = left * x_scale
     actual_top = top * y_scale
     actual_width = width * x_scale
     actual_height = height * y_scale
     actual_right = actual_left + actual_width
     actual_lower = actual_top + actual_height
     crop_box = (actual_left, actual_top, actual_right, actual_lower)
     return crop_box
#extract the text from image
def extract_text_from_image(img):
    text = pytesseract.image_to_string(img)
    return text.strip()

