import pandas as pd

def sort_csv_to_excel(csv_file, excel_file, sort_column):
    # Read the CSV file into a pandas DataFrame
    data_frame = pd.read_csv(csv_file)

    # Check if the sort column exists in the DataFrame
    if sort_column not in data_frame.columns:
        print(f"Error: Column '{sort_column}' does not exist in the CSV file.")
        return

    # Sort the DataFrame based on the specified column
    sorted_data = data_frame.sort_values(by=sort_column)

    # Write the sorted data to an Excel file
    sorted_data.to_excel(excel_file, index=False)

    print("Data sorted and saved to Excel successfully.")

def filter_csv_to_excel(csv_file, excel_file, filter_column, filter_value):
    # Read the CSV file into a pandas DataFrame
    data_frame = pd.read_csv(csv_file)

    # Check if the filter column exists in the DataFrame
    if filter_column not in data_frame.columns:
        print(f"Error: Column '{filter_column}' does not exist in the CSV file.")
        return

    # Filter the DataFrame based on the specified column and value
    filtered_data = data_frame[data_frame[filter_column] == filter_value]

    # Write the filtered data to an Excel file
    filtered_data.to_excel(excel_file, index=False)

    print("Data filtered and saved to Excel successfully.")

def aggregate_csv_to_excel(csv_file, excel_file, group_by_columns, aggregation_column, aggregation_function):
    # Read the CSV file into a pandas DataFrame
    data_frame = pd.read_csv(csv_file)

    # Check if the group by columns and aggregation column exist in the DataFrame
    columns_exist = all(column in data_frame.columns for column in group_by_columns + [aggregation_column])
    if not columns_exist:
        print("Error: One or more columns do not exist in the CSV file.")
        return

    # Perform the aggregation
    aggregated_data = data_frame.groupby(group_by_columns)[aggregation_column].agg(aggregation_function).reset_index()

    # Write the aggregated data to an Excel file
    aggregated_data.to_excel(excel_file, index=False)

    print("Data aggregated and saved to Excel successfully.")

def merge_csv_to_excel(csv_files, excel_file):
    # Read the CSV files into a list of pandas DataFrames
    data_frames = [pd.read_csv(csv_file) for csv_file in csv_files]

    # Merge the DataFrames
    merged_data = pd.concat(data_frames)

    # Write the merged data to an Excel file
    merged_data.to_excel(excel_file, index=False)

    print("Data merged and saved to Excel successfully.")

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

# Call the function to sort the data and save it to Excel
sort_csv_to_excel(csv_file_path, excel_file_path, sort_column_name)

# Call the function to filter the data and save it to Excel
filter_csv_to_excel(csv_file_path, excel_file_path, filter_column_name, filter_value)

# Call the function to aggregate the data and save it to Excel
aggregate_csv_to_excel(csv_file_path, excel_file_path, group_by_columns, aggregation_column, aggregation_function)

# Call the function to merge the CSV files and save the merged data to Excel
merge_csv_to_excel(csv_files_to_merge, excel_file_path)
