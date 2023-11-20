import cv2
import numpy as np


def extract_tables(image_path, output_path, min_table_width=1000, min_table_height=100):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to segment the image
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours based on minimum width and height
    tables = [cv2.boundingRect(contour) for contour in contours if
              cv2.boundingRect(contour)[2] > min_table_width and
              cv2.boundingRect(contour)[3] > min_table_height]

    # Create a blank image with the same dimensions as the input image
    output = np.ones_like(image) * 255

    # Copy the tables from the original image to the output image
    for table in tables:
        x, y, w, h = table
        output[y:y + h, x:x + w] = image[y:y + h, x:x + w]

    # Save the output image with only the tables
    cv2.imwrite(output_path, output)

    print(f"Extracted {len(tables)} table(s) and saved to {output_path}")
def validate_saved_tables(original_table_image_path, saved_table_image_path):
    original_table_image = cv2.imread(original_table_image_path, cv2.IMREAD_GRAYSCALE)
    saved_table_image = cv2.imread(saved_table_image_path, cv2.IMREAD_GRAYSCALE)

    if original_table_image.shape == saved_table_image.shape:
        print("Table images have the same shape.")
    else:
        print("Table images have different shapes.")
