import pandas as pd

# Constants
CSV_FILE_PATH = "path/to/input.csv"
EXCEL_FILE_PATH = "path/to/output.xlsx"
SORT_COLUMN_NAME = "column_name_to_sort"
FILTER_COLUMN_NAME = "column_name_to_filter"
FILTER_VALUE = "value_to_filter"
GROUP_BY_COLUMNS = ["column1", "column2"]
AGGREGATION_COLUMN = "column_to_aggregate"
AGGREGATION_FUNCTION = "sum"
CSV_FILES_TO_MERGE = ["path/to/file1.csv", "path/to/file2.csv", "path/to/file3.csv"]
COLUMN_NAMES_TO_RENAME = {
    "current_column_name1": "new_column_name1",
    "current_column_name2": "new_column_name2",
}
COLUMNS_TO_APPLY_FUNCTION = ["column1", "column2"]

# Utility functions
def read_csv(csv_file):
    try:
        data_frame = pd.read_csv(csv_file, header=None, skip_blank_lines=True)
        return data_frame
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: Unable to read '{csv_file}': {e}")
        return None

def save_to_excel(data_frame, excel_file):
    try:
        data_frame.to_excel(excel_file, index=False)
        print(f"Data saved to '{excel_file}' successfully.")
    except Exception as e:
        print(f"Error: Unable to save data to '{excel_file}': {e}")

# Data processing functions
def remove_duplicates_and_save(csv_file, excel_file):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame.drop_duplicates(inplace=True)
        save_to_excel(data_frame, excel_file)

def sort_and_save(csv_file, excel_file, sort_column):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        if sort_column not in data_frame.columns:
            print(f"Error: Column '{sort_column}' does not exist in the CSV file.")
        else:
            sorted_data = data_frame.sort_values(by=sort_column)
            save_to_excel(sorted_data, excel_file)

def filter_and_save(csv_file, excel_file, filter_column, filter_value):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        if filter_column not in data_frame.columns:
            print(f"Error: Column '{filter_column}' does not exist in the CSV file.")
        else:
            filtered_data = data_frame[data_frame[filter_column] == filter_value]
            save_to_excel(filtered_data, excel_file)

def aggregate_and_save(csv_file, excel_file, group_by_columns, aggregation_column, aggregation_function):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        columns_exist = all(column in data_frame.columns for column in group_by_columns + [aggregation_column])
        if not columns_exist:
            print("Error: One or more columns do not exist in the CSV file.")
        else:
            aggregated_data = data_frame.groupby(group_by_columns)[aggregation_column].agg(aggregation_function).reset_index()
            save_to_excel(aggregated_data, excel_file)

def merge_and_save(csv_files, excel_file):
    data_frames = [read_csv(csv_file) for csv_file in csv_files]
    data_frames = [df for df in data_frames if df is not None]  # Remove any None values
    if data_frames:
        merged_data = pd.concat(data_frames)
        save_to_excel(merged_data, excel_file)

def rename_columns_and_save(csv_file, excel_file, column_names):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame.rename(columns=column_names, inplace=True)
        save_to_excel(data_frame, excel_file)

def apply_function_and_save(csv_file, excel_file, columns, function):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame[columns] = data_frame[columns].apply(function)
        save_to_excel(data_frame, excel_file)

if __name__ == '__main__':
    # Call the function to rename the columns and save the modified data to Excel
    rename_columns_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH, COLUMN_NAMES_TO_RENAME)

    # Call the function to remove duplicates and save the modified data to Excel
    remove_duplicates_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH)

    # Call the function to apply a function to columns and save the modified data to Excel
    apply_function_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH, COLUMNS_TO_APPLY_FUNCTION, lambda x: x.upper())

    # Call the function to sort the data and save it to Excel
    sort_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH, SORT_COLUMN_NAME)

    # Call the function to filter the data and save it to Excel
    filter_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH, FILTER_COLUMN_NAME, FILTER_VALUE)

    # Call the function to aggregate the data and save it to Excel
    aggregate_and_save(CSV_FILE_PATH, EXCEL_FILE_PATH, GROUP_BY_COLUMNS, AGGREGATION_COLUMN, AGGREGATION_FUNCTION)

    # Call the function to merge the CSV files and save the merged data to Excel
    merge_and_save(CSV_FILES_TO_MERGE, EXCEL_FILE_PATH)
