from pikepdf import Pdf, Page, Rectangle
import os
import subprocess
import pdfkit
# this is to generate water mark pdf with single page
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter


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
                page_info = {'page_number': page_num + 1, 'fields': []}
                page = pdf_reader.pages[page_num]
                annotations = page.get('/Annots')                
                if annotations:
                    for annotation in annotations:
                        field_dict = annotation.get_object()
                        field_name = field_dict.get('/T')
                        field_value = field_dict.get('/V')
                        field_rect = field_dict.get('/Rect')
                        field_type = field_dict.get('/FT', 'Unknown Type')
                        
                        if field_name:
                            field_info = {
                                'filed_stype' : field_dict.get('/Subtype'),
                                'field_name': field_name,
                                'field_value': field_value,
                                'field_rect': field_rect,
                                'filed_type':field_type
                            }
                            page_info['fields'].append(field_info)
                            #print(f"Page {page_num + 1}:")
                            #print(f"  Field Name: {field_name}")
                            #print(f"  Field Value: {field_value}")
                            #print(f"  Position: {field_rect}")
                            #print()
                form_field_info.append(page_info)

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

