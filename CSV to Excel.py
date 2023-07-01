import pandas as pd

def read_csv(csv_file):
    try:
        data_frame = pd.read_csv(csv_file)
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

def sort_csv_to_excel(csv_file, excel_file, sort_column):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        if sort_column not in data_frame.columns:
            print(f"Error: Column '{sort_column}' does not exist in the CSV file.")
        else:
            sorted_data = data_frame.sort_values(by=sort_column)
            save_to_excel(sorted_data, excel_file)

def filter_csv_to_excel(csv_file, excel_file, filter_column, filter_value):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        if filter_column not in data_frame.columns:
            print(f"Error: Column '{filter_column}' does not exist in the CSV file.")
        else:
            filtered_data = data_frame[data_frame[filter_column] == filter_value]
            save_to_excel(filtered_data, excel_file)

def aggregate_csv_to_excel(csv_file, excel_file, group_by_columns, aggregation_column, aggregation_function):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        columns_exist = all(column in data_frame.columns for column in group_by_columns + [aggregation_column])
        if not columns_exist:
            print("Error: One or more columns do not exist in the CSV file.")
        else:
            aggregated_data = data_frame.groupby(group_by_columns)[aggregation_column].agg(aggregation_function).reset_index()
            save_to_excel(aggregated_data, excel_file)

def merge_csv_to_excel(csv_files, excel_file):
    data_frames = [read_csv(csv_file) for csv_file in csv_files]
    data_frames = [df for df in data_frames if df is not None]  # Remove any None values
    if data_frames:
        merged_data = pd.concat(data_frames)
        save_to_excel(merged_data, excel_file)

def rename_columns(csv_file, excel_file, column_names):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame.rename(columns=column_names, inplace=True)
        save_to_excel(data_frame, excel_file)

def remove_duplicates(csv_file, excel_file):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame.drop_duplicates(inplace=True)
        save_to_excel(data_frame, excel_file)

def apply_function_to_columns(csv_file, excel_file, columns, function):
    data_frame = read_csv(csv_file)
    if data_frame is not None:
        data_frame[columns] = data_frame[columns].apply(function)
        save_to_excel(data_frame, excel_file)

if __name__ == '__main__':
    # Provide the paths to the CSV and Excel files
    csv_file_path = "path/to/input.csv"
    excel_file_path = "path/to/output.xlsx"

    # Specify the column to sort by
    sort_column_name = "column_name_to_sort"

    # Specify the column and value to filter by
    filter_column_name = "column_name_to_filter"
    filter_value = "value_to_filter"

    # Specify the columns to group by, column to aggregate, and aggregation function
    group_by_columns = ["column1", "column2"]
    aggregation_column = "column_to_aggregate"
    aggregation_function = "sum"

    # Specify the list of CSV files to merge
    csv_files_to_merge = ["path/to/file1.csv", "path/to/file2.csv", "path/to/file3.csv"]

    # Call the function to rename the columns and save the modified data to Excel
    column_names_to_rename = {"current_column_name1": "new_column_name1", "current_column_name2": "new_column_name2"}
    rename_columns(csv_file_path, excel_file_path, column_names_to_rename)

    # Call the function to remove duplicates and save the modified data to Excel
    remove_duplicates(csv_file_path, excel_file_path)

    # Call the function to apply a function to columns and save the modified data to Excel
    columns_to_apply_function = ["column1", "column2"]
    function_to_apply = lambda x: x.upper()  # Example function, you can replace it with your desired function
    apply_function_to_columns(csv_file_path, excel_file_path, columns_to_apply_function, function_to_apply)

    # Call the function to sort the data and save it to Excel
    sort_csv_to_excel(csv_file_path, excel_file_path, sort_column_name)

    # Call the function to filter the data and save it to Excel
    filter_csv_to_excel(csv_file_path, excel_file_path, filter_column_name, filter_value)

    # Call the function to aggregate the data and save it to Excel
    aggregate_csv_to_excel(csv_file_path, excel_file_path, group_by_columns, aggregation_column, aggregation_function)

    # Call the function to merge the CSV files and save the merged data to Excel
    merge_csv_to_excel(csv_files_to_merge, excel_file_path)