# static-data
Working with LARGE data sets and $static


README for JSON Processing Script
This script is designed to process Excel files containing IQ Object data, convert it into valid JSON, split the JSON into smaller chunks based on size constraints, and save the output in a transformed format. Below is a high-level overview of the script's functionality and usage.

Features
Excel to JSON Conversion:

Reads an Excel file and converts each column into a JSON array.

Handles invalid JSON strings by cleaning and fixing common formatting issues.

JSON Splitting:

Splits large JSON arrays into smaller chunks to ensure each chunk does not exceed a specified size limit (default: 10 KB).

Text Replacements:

Applies transformations to the JSON structure (e.g., replacing { with o() for compatibility with specific systems.

Reverses these transformations when saving the output.

Debugging Support:

Includes optional debugging messages to track the transformation process.

Output Saving:

Saves the processed JSON to a file with a _split_output.json suffix.

Usage
Prerequisites
Python 3.x

Required Python libraries:

pandas (for Excel file handling)

json (for JSON processing)

re (for regex-based text replacements)

Install the required libraries using pip:

bash
Copy
pip install pandas
Running the Script
Basic Usage
To process an Excel file, run the script with the input file as an argument:

bash
Copy
python script.py <input_excel_file>
Example:

bash
Copy
python script.py data.xlsx
Debugging Mode
To enable debugging messages, use the --debug flag:

bash
Copy
python script.py <input_excel_file> --debug
Input File Format
The input file should be an Excel file (.xls or .xlsx).

Each column in the Excel file should contain IQ Object data or valid JSON strings.

Example of a valid column in Excel:

Copy
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
Output
The script generates a JSON file with the same name as the input file, appended with _split_output.json.

The output file contains:

Transformed JSON structure (e.g., { replaced with o().

Split JSON arrays to ensure each chunk is within the specified size limit.

Example output:

json
Copy
o(
"Other1", [
"54440",
"54440",
"56229"
],
"Other2", [
"12305",
"61047"
])
Customization
Max Chunk Size: Modify the max_size_kb parameter in the split_json function to change the maximum size of each JSON chunk (default: 10 KB).

Text Replacements: Update the replacements list in the apply_text_replacements and reverse_text_replacements functions to customize the transformations.

Error Handling
The script skips invalid JSON strings in the input file and logs a warning message.

If the input file cannot be parsed into valid JSON, the script exits with an error message.

Example Workflow
Input File: data.xlsx

Copy
Column1
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
Run Script:

bash
Copy
python script.py data.xlsx
Output File: data_split_output.json

json
Copy
o(
"Column1", [
{"name": "Alice", "age": 30},
{"name": "Bob", "age": 25}
])
Limitations
The script assumes that the input Excel file contains IQ Object or valid JSON strings in each column.

It does not handle deeply nested JSON structures or complex data types beyond strings and numbers.

