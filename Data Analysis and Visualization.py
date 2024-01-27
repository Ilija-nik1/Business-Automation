import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_data(filename):
    """Reads data from a CSV file."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        raise FileNotFoundError("Error: File not found.")

def validate_columns(data, *column_names):
    """Validates if columns exist in the data."""
    missing_columns = [col for col in column_names if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Error: Columns not found in the data: {', '.join(missing_columns)}")

def calculate_statistics(data, column_name):
    """Calculates mean, median, and generates a summary for a column."""
    validate_columns(data, column_name)
    mean_value = data[column_name].mean()
    median_value = data[column_name].median()
    summary = data[column_name].describe()
    return mean_value, median_value, summary

def plot_histogram(data, column_name):
    """Plots a histogram for a column."""
    validate_columns(data, column_name)
    sns.histplot(data[column_name], kde=True)
    plt.title(f'Distribution of {column_name}')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def plot_boxplot(data, column_name):
    """Plots a boxplot for a column."""
    validate_columns(data, column_name)
    sns.boxplot(data[column_name])
    plt.title(f'Boxplot of {column_name}')
    plt.xlabel('Values')
    plt.grid(True)
    plt.show()

def plot_scatter(data, x_column, y_column):
    """Plots a scatter plot for two columns."""
    validate_columns(data, x_column, y_column)
    sns.scatterplot(data=data, x=x_column, y=y_column)
    plt.title(f'Scatter plot: {x_column} vs {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)
    plt.show()

def calculate_correlation(data, column1, column2):
    """Calculates the correlation between two columns."""
    validate_columns(data, column1, column2)
    correlation = data[column1].corr(data[column2])
    return correlation

def plot_heatmap(data):
    """Plots a correlation heatmap for the data."""
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.grid(True)
    plt.show()

def main():
    # Read the data from a CSV file
    filename = 'data.csv'
    data = read_data(filename)

    if data is not None:
        # Select the columns to analyze
        column_name = 'column_name'
        x_column = 'x_column'
        y_column = 'y_column'

        # Calculate statistics and generate a summary for a column
        mean_value, median_value, summary_stats = calculate_statistics(data, column_name)
        print(f"Mean: {mean_value}")
        print(f"Median: {median_value}")
        print(summary_stats)

        # Plot a histogram
        plot_histogram(data, column_name)

        # Plot a boxplot
        plot_boxplot(data, column_name)

        # Plot a scatter plot
        plot_scatter(data, x_column, y_column)

        # Calculate correlation
        correlation = calculate_correlation(data, x_column, y_column)
        print(f"Correlation between {x_column} and {y_column}: {correlation}")

        # Plot a correlation heatmap
        plot_heatmap(data)

if __name__ == "__main__":
    main()