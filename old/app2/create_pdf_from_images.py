import os
from fpdf import FPDF

def create_pdf_from_images(image_dir, output_pdf_path):
    pdf = FPDF()

    # List all files in the image directory
    image_files = [f for f in os.listdir(image_dir) if f.endswith('_table.jpeg')]

    # Sort image files based on their names
    image_files.sort()

    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        pdf.add_page()
        pdf.image(image_path, x=10, y=8, w=190)  # Adjust x, y, w as needed

    pdf.output(output_pdf_path, "F")

if __name__ == '__main__':
    image_dir = 'temp'  # Directory containing the JPEG images with "_table"
    output_pdf_path = 'output_tables.pdf'

    try:
        create_pdf_from_images(image_dir, output_pdf_path)
        print(f"Created PDF with tables at: {output_pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
