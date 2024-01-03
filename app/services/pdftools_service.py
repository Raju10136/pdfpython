from pikepdf import Pdf, Page, Rectangle
import os
import subprocess

def generate_watermark_pdf(watermark_text, output_pdf):  
    c = canvas.Canvas(output_pdf)
    c.setFontSize(40)   
    c.setFillColorRGB(0.7, 0.7, 0.7)
    c.rotate(45)
    c.drawString(180, 50, watermark_text)
    c.save()

def merge_pdfs(input_files,output_file):
    pdf = Pdf.new()
    for fileName in input_files:
        src = Pdf.open(fileName)
        pdf.pages.extend(src.pages)
    pdf.save(output_file)

def add_string_before_extension_os(file_path, new_string):
    # Split the path into directory and filename parts
    directory, filename = os.path.split(file_path)

    # Split the filename into name and extension parts
    name, extension = os.path.splitext(filename)

    # Add the new string before the extension
    new_filename = f"{name}_{new_string}{extension}"

    # Join the directory and the new filename back together
    new_file_path = os.path.join(directory, new_filename)

    return new_file_path

def delete_file_os(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")

def gs_compress(input_pdf,output_pdf):
    ghostscript_command = [
    'gs',
    '-sDEVICE=pdfwrite',
    '-dCompatibilityLevel=1.4',
    '-dPDFSETTINGS=/screen',
    '-dNOPAUSE',
    '-dQUIET',
    '-dBATCH',
    f'-sOutputFile={output_pdf}',
    input_pdf
    ]
    # Execute the Ghostscript command
    try:
        subprocess.run(ghostscript_command, check=True)
        print("Ghostscript command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Ghostscript command: {e}")
# a service function to over the pdf
def overlay_pdf_with_start_page(input,overlay,output,start_page):
    try:
        input_pdf = Pdf.open(input)
        input_pdf_length=len(input_pdf.pages)
        print("input pdf length " , input_pdf_length)
        overlay_pdf = Pdf.open(overlay)
        overlay_pdf_length=len(overlay_pdf.pages)
        page_difference = input_pdf_length - (start_page + overlay_pdf_length)
        print("overlay_length " , overlay_pdf_length, "  spage " , start_page , " diff = ", page_difference)
        # Iterate through the pages of the input PDF
        for page_num, input_page in enumerate(input_pdf.pages, start=1):
            # Skip pages before the start_page
            if page_num < start_page:
                continue
            # If overlay has pages left, overlay the current page
            if page_num - start_page < len(overlay_pdf.pages):
                input_final_page=Page(input_pdf.pages[page_num])
                overlay_page =  Page(overlay_pdf.pages[page_num - start_page])
                input_final_page.add_overlay(overlay_page, Rectangle(20, 130, 580, 750))
        input_pdf.save(output)
    except  Exception as e:
        print(f"Error executing overlay command: {e}")

# adding water mark
def add_watermark(input_pdf, output_pdf, watermark_pdf):
    # Open the original PDF
    with Pdf.open(input_pdf) as pdf:
        wpdf = Pdf.open(watermark_pdf)
        # Loop through each page
        for page_num in range(len(pdf.pages)):
            destination_page = Page(pdf.pages[page_num])
            thumbnail = Page(wpdf.pages[0])
            destination_page.add_underlay(thumbnail, Rectangle(0, 0, 590, 800))
        # Save the watermarked PDF to a new file
        pdf.save(output_pdf)