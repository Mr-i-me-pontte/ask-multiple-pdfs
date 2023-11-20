import os

from pdf2image import convert_from_path

from helpers import analyze_local_response, find_page_blocks, process_text_analysis
from utils import extract_tables, validate_saved_tables


def pdf_to_jpeg_and_extract_tables(pdf_path, output_dir, json_file, min_table_width=1000, min_table_height=100):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path)
    analysis_results = []

    for i, page in enumerate(pages):
        image_path = os.path.join(output_dir, f'page_{i + 1}.jpeg')

        # Save the JPEG image
        page.save(image_path, 'JPEG')

        local_response = analyze_local_response(json_file)
        page_blocks = find_page_blocks(local_response['Blocks'], i + 1)

        if page_blocks:
            block_count = process_text_analysis(image_path, page_blocks)

            # Find tables in the image
            table_image_path = image_path.replace('.jpeg', '_table.jpeg')
            annotated_image_path = image_path.replace('.jpeg', '_annotated.jpeg')

            extract_tables(annotated_image_path, output_path=table_image_path, min_table_width=min_table_width,
                           min_table_height=min_table_height)

            # Validate the saved table image
            validate_saved_tables(image_path, table_image_path)
            analysis_results.append(block_count)
        else:
            print(f"No blocks found for page {i + 1}.")
            analysis_results.append(0)

    return analysis_results


if __name__ == '__main__':
    pdf_path = '/pdfapp/table_detection/woth_aws/data/input.pdf'
    output_dir = 'temp'
    json_file = 'data/analyzeDocResponse.json'  # Example JSON file

    try:
        results = pdf_to_jpeg_and_extract_tables(pdf_path, output_dir, json_file)
        print(results)
    except ImportError:
        print("Please make sure the required libraries are installed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

