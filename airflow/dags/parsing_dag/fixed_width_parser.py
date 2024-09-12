import json
import csv
import argparse

# Load the spec file
def load_spec(file_path):
    with open(file_path, 'r') as f:
        spec = json.load(f)
    column_names = spec['ColumnNames']
    offsets = list(map(int, spec['Offsets']))
    fixed_width_encoding = spec['FixedWidthEncoding']
    include_header = spec['IncludeHeader'].lower() == 'true'
    delimited_encoding = spec['DelimitedEncoding']
    
    print(f"Loaded spec: {spec}")  # Debugging
    return column_names, offsets, fixed_width_encoding, include_header, delimited_encoding


# Parse fixed-width file to CSV
def parse_fixed_width_file(input_file, output_file, column_names, offsets, fixed_width_encoding, include_header, delimited_encoding):
    print(f"Reading input file: {input_file}")  # Debugging
    print(f"Writing to output file: {output_file}")  # Debugging
    
    with open(input_file, 'r', encoding=fixed_width_encoding) as infile, open(output_file, 'w', newline='', encoding=delimited_encoding) as outfile:
        writer = csv.writer(outfile)
        
        if include_header:
            writer.writerow(column_names)
        
        for line in infile:
            start = 0
            row = []
            for length in offsets:
                row.append(line[start:start + length].strip())
                start += length
            writer.writerow(row)
            print(f"Processed row: {row}")  # Debugging

    print(f"CSV file created: {output_file}")  # Debugging


# Main function to parameterize using command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Parse fixed-width files to CSV using a spec file.")
    
    # Arguments for file paths
    parser.add_argument('--spec', required=True, help="Path to the spec.json file.")
    parser.add_argument('--input_file', required=True, help="Path to the input fixed-width file.")
    parser.add_argument('--output_file', required=True, help="Path to the output CSV file.")
    
    args = parser.parse_args()
    
    # Load the spec file
    column_names, offsets, fixed_width_encoding, include_header, delimited_encoding = load_spec(args.spec)
    
    # Parse the fixed-width file and generate the CSV
    parse_fixed_width_file(args.input_file, args.output_file, column_names, offsets, fixed_width_encoding, include_header, delimited_encoding)


if __name__ == "__main__":
    main()
