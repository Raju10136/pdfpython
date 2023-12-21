from pikepdf import Pdf, Page, Rectangle
from pdf_functions import merge_pdfs
from pdf_overlay import overlay_pdf_with_start_page
from pdf_compress import gs_compress,compress_pdf
#from pikepdf import Pdf
input_pdf_path = "template.pdf"
overlay_pdf_path = "overlay/1.pdf"
output_pdf_path = "output.pdf"
#copy_pdf(input_pdf_path, output_pdf_path)
#overlay_pdf(input_pdf_path,overlay_pdf_path,output_pdf_path)
input_files=["overlay/1.pdf","overlay/2.pdf","overlay/3.pdf","overlay/4.pdf","overlay/5.pdf"]
output_file = "overlay/combine.pdf"
#merge_pdfs(input_files,output_file)
#overlaying process start
final_pdf="overlay.pdf"
#overlay_pdf_with_start_page(input_pdf_path,output_file,final_pdf,42)
#compression of pdf
compressed_pdf="compressed.pdf"
#gs_compress(final_pdf,compressed_pdf)
compress_pdf(final_pdf,compressed_pdf)