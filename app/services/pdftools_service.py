from pikepdf import Pdf, Page, Rectangle
import os

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