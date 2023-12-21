import subprocess
import pikepdf

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

def compress_pdf(input_path, output_path):
    #pikepdf._qpdf.set_flate_compression_level(9)
    pikepdf.settings.set_flate_compression_level(9)
    with pikepdf.Pdf.open(input_path) as pdf:
        # Set the compression options for the PDF
        #pdf.compress()

        # Save the compressed PDF to the output file
        pdf.save(output_path, recompress_flate=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)