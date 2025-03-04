import json
import sys
import os
import re
import pandas as pd

def split_json(input_json, max_size_kb=10):
    """Splits JSON data into chunks if the size exceeds the max limit."""
    max_size_bytes = max_size_kb * 1024
    result = {}

    for key, items in input_json.items():
        chunk = []
        part = 1

        for item in items:
            test_chunk = chunk + [item]
            test_json = json.dumps({key: test_chunk})

            if sys.getsizeof(test_json.encode('utf-8')) > max_size_bytes:
                new_key = key if part == 1 else f"{key}{part}"
                result[new_key] = chunk
                chunk = [item]
                part += 1
            else:
                chunk = test_chunk

        if chunk:
            new_key = key if part == 1 else f"{key}{part}"
            result[new_key] = chunk

    return result

def fix_pseudo_json(pseudo_json, debug=False):
    """Converts pseudo-JSON into valid JSON format and prints transformations for debugging."""
    pseudo_json = pseudo_json.strip()
    
    if debug:
        print("\n--- Debugging Pseudo-JSON Conversion ---")

    # Step 1: Replace `o(` with `{` and `)` with `}`
    before = pseudo_json
    pseudo_json = pseudo_json.replace("o(", "{").replace(")", "}")
    if debug:
        print(f"Step 1: Replace `o(` & `)`: \nBefore: {before}\nAfter:  {pseudo_json}\n")

    # Step 2: Convert inner `{}` blocks into `[]`
    before = pseudo_json
    pseudo_json = re.sub(r'\{([^{}]+)\}', r'[\1]', pseudo_json)
    if debug:
        print(f"Step 2: Convert inner `{{}}` to `[]`: \nBefore: {before}\nAfter:  {pseudo_json}\n")

    # Step 3: Ensure keys are quoted and followed by colons
    before = pseudo_json
    pseudo_json = re.sub(r'"([^"]+)"\s*,\s*(\[|\{)', r'"\1": \2', pseudo_json)
    if debug:
        print(f"Step 3: Ensure keys are quoted & followed by colons: \nBefore: {before}\nAfter:  {pseudo_json}\n")

    # Step 4: Add commas between key-value pairs
    before = pseudo_json
    pseudo_json = re.sub(r'\]\s*"', r'], "', pseudo_json)
    if debug:
        print(f"Step 4: Add commas between key-value pairs: \nBefore: {before}\nAfter:  {pseudo_json}\n")

    # Step 5: Remove trailing commas inside lists
    before = pseudo_json
    pseudo_json = re.sub(r',\s*([\]}])', r'\1', pseudo_json)
    if debug:
        print(f"Step 5: Remove trailing commas: \nBefore: {before}\nAfter:  {pseudo_json}\n")

    # Validate the JSON
    try:
        json.loads(pseudo_json)
        if debug:
            print("Validation: The output is valid JSON.")
    except json.JSONDecodeError as e:
        print(f"Validation Error: The output is not valid JSON. Error: {e}")

    if debug:
        print("--- End of Debugging ---\n")

    return pseudo_json


def read_text_file_as_json(input_file):
    """Reads a text file and converts it into proper JSON."""
    try:
        with open(input_file, 'r') as f:
            text_content = f.read()

        # Convert pseudo-JSON to valid JSON
        fixed_json_string = fix_pseudo_json(text_content)
        return json.loads(fixed_json_string)  # Ensure it's valid JSON
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse input file as JSON. Issue: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error processing text file: {e}")
        sys.exit(1)

def excel_to_json(input_excel):
    """Converts an Excel file to a JSON dictionary."""
    df = pd.read_excel(input_excel)
    json_data = {}

    for column in df.columns:
        items = df[column].dropna().tolist()
        json_data[column] = items

    return json_data

def apply_text_replacements(json_string):
    replacements = [
        ('{', 'o('),
        ('}', ')'),
        ('[', '{'),
        (']', '}'),
        (':', ',')
    ]
    for old, new in replacements:
        json_string = json_string.replace(old, new)
    return json_string

def save_json_to_file(data, output_file):
    """Saves JSON data to a file."""
    json_string = json.dumps(data, indent=2)
    transformed_string = apply_text_replacements(json_string)
    with open(output_file, 'w') as f:
        f.write(transformed_string)
    print(f"Processed JSON has been saved to {output_file}")

def main(input_file, debug=False):
    """Determines the file type and processes it accordingly."""
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext in ('.xls', '.xlsx'):
        input_json = excel_to_json(input_file)
    else:
        input_json = read_text_file_as_json(input_file)

    if not isinstance(input_json, dict):  # Ensure valid JSON structure
        print("Error: Could not parse input into valid JSON.")
        sys.exit(1)

    split_result = split_json(input_json)
    output_file = os.path.splitext(input_file)[0] + '_split_output.txt'
    save_json_to_file(split_result, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> [--debug]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    debug = "--debug" in sys.argv
    main(input_file, debug)
