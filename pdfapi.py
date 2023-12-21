from pikepdf import Pdf, Page, Rectangle
from pdf_functions import merge_pdfs,add_string_before_extension_os,delete_file_os
from pdf_overlay import overlay_pdf_with_start_page
from pdf_compress import gs_compress,compress_pdf

def overlay_with_start(template,overlay,start_page):
    # merge path
    merge_output = add_string_before_extension_os(template,"merge")
    # merge pdfs
    merge_pdfs(overlay,merge_output)
    # over lay path
    overlay_path = add_string_before_extension_os(template,"overlay")
    # over lay pdf
    overlay_pdf_with_start_page(template,merge_output,overlay_path,start_page)
    #delete merge file 
    delete_file_os(merge_output)
    #output path
    output_file = add_string_before_extension_os(template,"output")
    #compress the file
    gs_compress(overlay_path,output_file)
    print("compression over")
    #delete the overlay file
    #delete_file_os(overlay_path)
    #return output
    return output_file

#compress_pdf("data/1.pdf","data/2.pdf")
