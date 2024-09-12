import csv
import argparse
from faker import Faker

# Initialize Faker
fake = Faker()

def generate_csv(file_name, num_rows):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['first_name', 'last_name', 'address', 'date_of_birth']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _ in range(num_rows):
            writer.writerow({
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'address': fake.address().replace("\n", ", "),  # Clean up address format
                'date_of_birth': fake.date_of_birth()
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a CSV file with fake data.')
    parser.add_argument('--file', required=True, help='Path to the output CSV file.')
    parser.add_argument('--rows', type=int, default=1000, help='Number of rows to generate.')

    args = parser.parse_args()
    generate_csv(args.file, args.rows)
