from pikepdf import Pdf, Page, Rectangle

def overlay_pdf_with_start_page(input,overlay,output,start_page):
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

