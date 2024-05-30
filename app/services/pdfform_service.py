from pikepdf import Pdf, Page, Rectangle
import os
import subprocess
import pdfkit
# this is to generate water mark pdf with single page
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import white
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from app.services.image_service import convert_pdf_page_to_image,crop_image,save_image,crop_box_calculation,extract_text_from_image,image_to_base64
import io


def read_pdf_form_fields_old(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
           reader = PdfReader(pdf_path)
           fields = reader.get_form_text_fields()
           print("pdf fileds " , fields)
    except Exception as e:
        print(f"Error: {str(e)}") # PyMuPDF

def read_pdf_form_fields(pdf_path):
    form_field_info = []
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)            
            for page_num in range(len(pdf_reader.pages)):
                #page_info = {'page_number': page_num + 1, 'fields': []}
                page_fileds =[]
                page = pdf_reader.pages[page_num]
                annotations = page.get('/Annots')                
                if annotations:
                    for annotation in annotations:
                        field_dict = annotation.get_object()
                        field_name = field_dict.get('/T')
                        field_value = field_dict.get('/V')
                        field_rect = field_dict.get('/Rect')
                        field_type = field_dict.get('/FT', 'Unknown Type')
                        field_left = field_rect[0]
                        field_top =  field_rect[1]
                        field_right = field_rect[2]
                        field_bottom =  field_rect[3]
                        width =  field_right -  field_left
                        height = field_bottom - field_top
                        if field_name:
                            field_info = {
                                'stype' : field_dict.get('/Subtype'),
                                'name': field_name,
                                'value': field_value,
                                'rect': field_rect,
                                'type':field_type,
                                'left':field_left,
                                'top':841-field_bottom,
                                'width':width,
                                'height':height
                            }
                            page_fileds.append(field_info)
                            #print(f"Page {page_num + 1}:")
                            #print(f"  Field Name: {field_name}")
                            #print(f"  Field Value: {field_value}")
                            #print(f"  Position: {field_rect}")
                            #print()
                form_field_info.append(page_fileds)

    except Exception as e:
        print(f"Error: {str(e)}")
    # return the form fields
    return form_field_info

def fill_form_fields(src_loc,page_fields,dest_loc):
    reader = PdfReader(src_loc)
    writer = PdfWriter()
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        writer.add_page(page)
        if 0 <= page_num < len(page_fields):
            fields = page_fields[page_num]
            for obj in fields:    
                name = obj['name']
                value= obj['value']   
                writer.update_page_form_field_values(
                     writer.pages[page_num], {name: value}
                )
    # write "output" to PyPDF2-output.pdf
    with open(dest_loc, "wb") as output_stream:
        writer.write(output_stream)


def generate_template_pdf(src_loc,page_fields,dest_loc):
    try:
         reader = PdfReader(src_loc)
         writer = PdfWriter()
         #print("page writer name as target ")
         for page_num in range(len(reader.pages)):
             page = reader.pages[page_num]
             packet = io.BytesIO()
             c = canvas.Canvas(packet, pagesize=letter)
             c.drawString(0, 0, "")
             #pdf_writer = PdfWriter()
             #pdf_writer.add_page(page)
             #print("enteerd in page number " , page_num)       
             if 0 <= page_num < len(page_fields):
                fields = page_fields[page_num]
                for obj in fields:    
                    value = obj['value']
                    name = obj['name']
                    if value=="newsoft":
                       media_box = page.mediabox
                       page_height = media_box.upper_right[1] - media_box.lower_left[1]
                       #print("entering in page class of objects ")
                       left = int(float(obj['left']))
                       height = int(float(obj['height']))
                       top = page_height - height - int(float(obj['top']))
                       width = int(float(obj['width']))
                       type = obj['type']
                       #print("top specified is " , top)
                       # Create a canvas for drawing on the first page
                       #llx = 100
                       #lly = 350
                       #urx = 200
                       #ury = 500                    
                       # Create a text field
                       if type=="checkbox":
                            c.acroForm.checkbox(name=name,x=left,y=top)
                       else :
                           c.acroForm.textfield(name=name, x=left, y=top, width=width, 
                                            height=height,borderWidth=0, fontSize=10,
                                            fillColor=white) 
                #value= obj['value']
             #print("Fields Loop out")   
             c.save()
             packet.seek(0)
             #print("asigning the canvas to new pdf")
             new_pdf = PdfReader(packet)
             #print("merging the canvas first page to page length = " , len(new_pdf.pages))
             page.merge_page(new_pdf.pages[0])
             #print("adding to writer that page")
             writer.add_page(page)                   
    # write "output" to PyPDF2-output.pdf
         with open(dest_loc, "wb") as output_stream:
            writer.write(output_stream)
    except Exception as e:
        print(f"Error: {str(e)}")


def extract_data_pdf(src_loc,page_fields,dest_loc):
    try:
         reader = PdfReader(src_loc)
         page_fileds =[]
         #writer = PdfWriter()
         #print("page writer name as target ")
         for page_num in range(len(reader.pages)):
             page = reader.pages[page_num]
             media_box = page.mediabox
             page_height = float(media_box[3])
             page_width = float(media_box[2])
             if 0 <= page_num < len(page_fields):
                fields = page_fields[page_num]
                for obj in fields:  
                    image = convert_pdf_page_to_image(src_loc, page_num)
                    crop_box = crop_box_calculation(page_width,page_height,image,obj)            
                    cropped_image = crop_image(image, crop_box)
                    output_image_path = dest_loc + '/cropped_image_'+str(page_num) + str(obj["left"]) +'.png'
                    save_image(cropped_image, output_image_path)
                    if obj["type"]!='image': 
                        extacted_text = extract_text_from_image(cropped_image)
                    else :
                        extacted_text = image_to_base64(cropped_image)
                    field={
                        'name':obj["name"],
                        'text':extacted_text,
                        'type':obj["type"]
                    }
                    page_fileds.append(field)
                    print("extracted image path " , extacted_text)
         return page_fileds 
            #  obj = {}
            #  obj["left"] = 363
            #  obj["width"] = 144
            #  obj["top"] = 142
            #  obj["height"] = 28
            
             #output_image_path = dest_loc + '/cropped_image_'+str(page_num)+'.png'
             #save_image(cropped_image, output_image_path)  
    except Exception as e:
        print(f"Error: {str(e)}")

