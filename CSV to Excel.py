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
        data_frame = pd.read_csv(csv_file, skip_blank_lines=True)
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
def process_and_save_csv(csv_file, excel_file, functions):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        for function in functions:
            data_frame = function(data_frame)
        save_to_excel(data_frame, excel_file)

def remove_duplicates(data_frame):
    data_frame.drop_duplicates(inplace=True)
    return data_frame

def sort_data(data_frame):
    if SORT_COLUMN_NAME in data_frame.columns:
        return data_frame.sort_values(by=SORT_COLUMN_NAME)
    else:
        print(f"Error: Column '{SORT_COLUMN_NAME}' does not exist in the CSV file.")
        return data_frame

def filter_data(data_frame):
    if FILTER_COLUMN_NAME in data_frame.columns:
        return data_frame[data_frame[FILTER_COLUMN_NAME] == FILTER_VALUE]
    else:
        print(f"Error: Column '{FILTER_COLUMN_NAME}' does not exist in the CSV file.")
        return data_frame

def aggregate_data(data_frame):
    if all(column in data_frame.columns for column in GROUP_BY_COLUMNS + [AGGREGATION_COLUMN]):
        return data_frame.groupby(GROUP_BY_COLUMNS)[AGGREGATION_COLUMN].agg(AGGREGATION_FUNCTION).reset_index()
    else:
        print("Error: One or more columns do not exist in the CSV file.")
        return data_frame

def merge_csv_files(csv_files):
    data_frames = [read_csv(csv_file) for csv_file in csv_files]
    data_frames = [df for df in data_frames if df is not None]
    if data_frames:
        return pd.concat(data_frames)
    else:
        return None

def rename_columns(data_frame):
    data_frame.rename(columns=COLUMN_NAMES_TO_RENAME, inplace=True)
    return data_frame

def apply_function(data_frame):
    data_frame[COLUMNS_TO_APPLY_FUNCTION] = data_frame[COLUMNS_TO_APPLY_FUNCTION].apply(lambda x: x.upper())
    return data_frame

if __name__ == '__main__':
    functions_to_apply = [
        rename_columns,
        remove_duplicates,
        apply_function,
        sort_data,
        filter_data,
        aggregate_data
    ]

    merged_data_frame = merge_csv_files(CSV_FILES_TO_MERGE)

    if merged_data_frame is not None:
        functions_to_apply.append(lambda df: merged_data_frame)

    process_and_save_csv(CSV_FILE_PATH, EXCEL_FILE_PATH, functions_to_apply)