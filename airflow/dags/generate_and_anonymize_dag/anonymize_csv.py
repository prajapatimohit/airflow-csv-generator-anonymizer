import csv
import hashlib
import argparse


def anonymize_data(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def process_csv(input_file, output_file, fields_to_anonymize, chunk_size=10000):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)  # Use DictReader to handle columns by name
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Process each chunk of data
        for i, row in enumerate(reader):
            for field in fields_to_anonymize:
                if field in row and row[field]:
                    row[field] = anonymize_data(row[field])
            
            writer.writerow(row)
            if i % chunk_size == 0:
                print(f"Processed {i} rows")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Anonymize specific fields in a CSV file.')
    parser.add_argument('--input', required=True, help='Path to the input CSV file.')
    parser.add_argument('--output', required=True, help='Path to the output anonymized CSV file.')
    parser.add_argument('--fields', nargs='+', required=True, help='List of fields (column names) to anonymize.')
    parser.add_argument('--chunk_size', type=int, default=1000, help='Number of rows to process at a time.')


    args = parser.parse_args()
    # Call the process_csv function with the input, output file paths, and fields to anonymize
    process_csv(args.input, args.output, args.fields, args.chunk_size)


