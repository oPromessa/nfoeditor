"""
    by oPromessa, 2024
    Published on https://github.com/oPromessa/nfoeditor
"""

import xml.etree.ElementTree as ET
import sys
import re
import pandas as pd
import os

def edit_xml(xml_file, row, fields_to_edit):
    # Check if XML file exists
    if not os.path.exists(xml_file):
        print(f"Error: XML file '{xml_file}' not found.")
        return False
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Function to validate date format
    def validate_date(date_str):
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        return bool(re.match(date_pattern, date_str))

    # Function to recursively edit fields
    def edit_fields(element):
        for child in element:
            if child.tag in fields_to_edit.get(element.tag, {}):
                field_type = fields_to_edit[element.tag][child.tag]
                if field_type == "date":
                    current_value = child.text.strip()  # Get current value
                    new_value = row.loc[element.tag+'/'+child.tag+':'+field_type]
                    # new_value = input(f"Enter new date value for {element.tag}/{child.tag} (YYYY-MM-DD) [{current_value}]: ")
                    if not new_value:  # If input is empty, keep previous value
                        new_value = current_value
                    else:
                        if not validate_date(new_value):
                            print("Invalid date format (expected YYYY-MM-DD). Keep current format.")
                            new_value = current_value
                            # new_value = input(f"Enter new date value for {element.tag}/{child.tag} (YYYY-MM-DD) [{current_value}]: ")
                else:
                    current_value = child.text.strip()  # Get current value
                    new_value = row.loc[element.tag+'/'+child.tag+':'+field_type]
                    # new_value = input(f"Enter new value for {element.tag}/{child.tag} ({field_type}) [{current_value}]: ")
                    if not new_value:  # If input is empty, keep previous value
                        new_value = current_value

                # Convert input to the specified type
                if field_type == "integer":
                    new_value = int(new_value)
                elif field_type == "float":
                    new_value = float(new_value)
                child.text = str(new_value)
                print(f"\tDefined {element.tag+'/'+child.tag+':'} [{new_value}].")
            else:
                edit_fields(child)

    # Edit fields
    edit_fields(root)

    # Write back to the same file while preserving comments
    tree.write(xml_file, encoding='utf-8', xml_declaration=True, method="xml")

    return True

def process_xls(xls_file):
    # Read the Excel file
    df = pd.read_excel(xls_file)
    total_rows = 0
    edited_rows = 0

    for index, row in df.iterrows():
        xml_file = row['xml filename']
        print(f"Editing file [{xml_file}]...")
        fields_to_edit = {}
        for column in df.columns[1:]:  # Exclude the first column (xml filename)
            field, field_type = column.split(':')
            parent, child = field.split('/')
            if parent not in fields_to_edit:
                fields_to_edit[parent] = {}
            fields_to_edit[parent][child] = field_type

        if edit_xml(xml_file, row, fields_to_edit):
            edited_rows += 1
        total_rows += 1

    print(f"Total rows processed:[{total_rows}] Out of which edited:[{edited_rows}]")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python program_name.py <xls_file>")
        sys.exit(1)

    xls_file = sys.argv[1]
    process_xls(xls_file)
