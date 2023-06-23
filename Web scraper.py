import csv
import argparse
import logging
import requests
from bs4 import BeautifulSoup


def scrape_data(url, output_filename):
    # Start scraping
    logging.info('Scraping data from %s...', url)

    # Get page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        logging.error('Failed to retrieve page: %s', e)
        exit(1)

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find table
    table = soup.find('table')

    if not table:
        logging.error('Table not found')
        exit(1)

    # Find rows
    rows = table.find_all('tr')

    if not rows:
        logging.warning('No rows found in table')
        exit(1)

    # Write data to CSV file
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)

        for row in rows:
            cells = row.find_all(['td', 'th'])

            if not cells:
                logging.warning('No cells found in row: %s', row)
                continue

            csv_row = [cell.get_text().strip() for cell in cells]
            writer.writerow(csv_row)

    logging.info('Data saved to %s', output_filename)


def print_data(csv_filename, filter_column=None, filter_value=None):
    # Read data from CSV file and print it
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if filter_column is None or filter_value is None or \
                    (filter_column < len(row) and row[filter_column] == filter_value):
                print(row)


def count_rows(csv_filename):
    # Count the number of rows in the CSV file
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        row_count = sum(1 for _ in reader)
        return row_count


def extract_column(csv_filename, column_index):
    # Extract a specific column from the CSV file
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        column_data = [row[column_index] for row in reader if column_index < len(row)]
        return column_data


def search_value(csv_filename, search_column, search_value, return_column):
    # Search for a specific value in a column and return the corresponding value from another column
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if search_column < len(row) and return_column < len(row) and row[search_column] == search_value:
                return row[return_column]
        return None


if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser(description='Web scraper')
    parser.add_argument('url', type=str, help='URL of the page to scrape')
    parser.add_argument('-o', '--output', type=str, default='data.csv', help='Output filename')
    parser.add_argument('-p', '--print', action='store_true', help='Print the data after scraping')
    parser.add_argument('-c', '--count', action='store_true', help='Count the number of rows')
    parser.add_argument('-fc', '--filter-column', type=int, help='Filter data by column index')
    parser.add_argument('-fv', '--filter-value', type=str, help='Filter data by column value')
    parser.add_argument('-ec', '--extract-column', type=int, help='Extract a specific column')
    parser.add_argument('-sc', '--search-column', type=int, help='Column index for search operation')
    parser.add_argument('-sv', '--search-value', type=str, help='Value to search for')
    parser.add_argument('-rc', '--return-column', type=int, help='Column index to return in search operation')
    args = parser.parse_args()

    # Logging configuration
    logging.basicConfig(level=logging.INFO)

    # URL and output filename
    url = args.url
    output_filename = args.output

    # Scrape data
    scrape_data(url, output_filename)

    # Print data if specified
    if args.print:
        print_data(output_filename, args.filter_column, args.filter_value)

    # Count rows if specified
    if args.count:
        row_count = count_rows(output_filename)
        print(f"Number of rows: {row_count}")

    # Extract column if specified
    if args.extract_column is not None:
        column_index = args.extract_column
        column_data = extract_column(output_filename, column_index)
        print(f"Column {column_index}: {column_data}")

    # Search for a value in a column and return another column's value if specified
    if args.search_column is not None and args.search_value is not None and args.return_column is not None:
        search_column_index = args.search_column
        search_value = args.search_value
        return_column_index = args.return_column
        result = search_value(output_filename, search_column_index, search_value, return_column_index)
        if result is not None:
            print(f"Found: {result}")
        else:
            print("Value not found.")