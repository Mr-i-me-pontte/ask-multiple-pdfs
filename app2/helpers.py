import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from pdf2image import convert_from_path

def show_bounding_box(draw, box, width, height, box_color):
    left = width * box['Left']
    top = height * box['Top']
    right = left + (width * box['Width'])
    bottom = top + (height * box['Height'])
    draw.rectangle([left, top, right, bottom], outline=box_color)

def display_block_information(block):
    print(f'Id: {block["Id"]}')
    if 'Text' in block:
        print(f'    Detected: {block["Text"]}')
    print(f'    Type: {block["BlockType"]}')

    if 'Confidence' in block:
        print(f'    Confidence: {block["Confidence"]:.2f}%')

    if block['BlockType'] == 'CELL':
        print(f"    Cell information")
        print(f"        Column: {block['ColumnIndex']}")
        print(f"        Row: {block['RowIndex']}")
        print(f"        Column Span: {block['ColumnSpan']}")
        print(f"        Row Span: {block['RowSpan']}")

    if 'Relationships' in block:
        print(f'    Relationships: {block["Relationships"]}')
    print('    Geometry: ')
    print(f'        Bounding Box: {block["Geometry"]["BoundingBox"]}')
    print(f'        Polygon: {block["Geometry"]["Polygon"]}')

    if block['BlockType'] == "KEY_VALUE_SET":
        print(f'    Entity Type: {block["EntityTypes"][0]}')

    if block['BlockType'] == 'SELECTION_ELEMENT':
        print('    Selection element detected: ', end='')
        print('Selected' if block['SelectionStatus'] == 'SELECTED' else 'Not selected')

    if 'Page' in block:
        print(f'Page: {block["Page"]}')
    print()

def process_text_analysis(image_path, blocks):
    print('Detected Document Text')

    image = Image.open(image_path)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    for block in blocks:
        display_block_information(block)

        box_color = None
        if block['BlockType'] == "KEY_VALUE_SET":
            box_color = 'pink' if block['EntityTypes'][0] == "KEY" else 'green'
        elif block['BlockType'] == 'TABLE':
            box_color = 'brown'
        elif block['BlockType'] == 'CELL':
            box_color = 'red'
        elif block['BlockType'] == 'SELECTION_ELEMENT':
            box_color = 'blue' if block['SelectionStatus'] == 'SELECTED' else None

        if box_color is not None:
            show_bounding_box(draw, block['Geometry']['BoundingBox'], width, height, box_color)

    # Save the annotated image
    annotated_image_path = image_path.replace('.jpeg', '_annotated.jpeg')
    image.save(annotated_image_path, 'JPEG')
    # image.show()

    return len(blocks)

def find_page_blocks(blocks, page):
    return [block for block in blocks if 'Page' in block and block['Page'] == page]

def analyze_local_response(json_file):
    with open(json_file, 'r') as file:
        response = json.load(file)
    return response
