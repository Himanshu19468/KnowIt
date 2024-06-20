from datetime import datetime, timedelta
import pandas as pd


def break_dates(start_date_str, end_date_str, n):
    """
    Breaks the interval between start_date and end_date into smaller intervals of n days each.

    Parameters:
    - start_date_str: A string representing the start date/time in "YYYY-MM-DD HH:MM" format.
    - end_date_str: A string representing the end date/time in "YYYY-MM-DD HH:MM" format.
    - n: Number of days for each interval.

    Returns:
    - A list of tuples, each containing start and end dates of the intervals.
    """

    # Convert string dates to datetime objects
    # "%Y-%m-%d-%H-%M"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")

    # Initialize the current_date to start_date
    current_date = start_date

    # List to hold the result intervals
    intervals = []

    # Generate intervals
    while current_date < end_date:
        next_date = current_date + timedelta(days=n)

        # Make sure the end date of the interval does not exceed the overall end date
        if next_date > end_date:
            next_date = end_date

        # Append the interval (start and end dates) to the list
        intervals.append((current_date.strftime("%Y-%m-%d %H:%M"), next_date.strftime("%Y-%m-%d %H:%M")))

        # Move to the next interval
        current_date = next_date

    return intervals


# Example usage

def convert_datetime_format(df, datetime_column):
    """
    Convert datetime strings in a DataFrame column to the "YYYY-MM-DD HH:MM:SS" format.

    Parameters:
    - df: DataFrame
        The DataFrame containing the datetime column.
    - datetime_column: str
        The name of the datetime column in the DataFrame.

    Returns:
    - DataFrame: A copy of the input DataFrame with the datetime column converted to the desired format.
    """
    # Make a copy of the DataFrame to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Convert datetime column to datetime type
    df_copy[datetime_column] = pd.to_datetime(df_copy[datetime_column])

    # Format datetime column to "YYYY-MM-DD HH:MM:SS" format
    df_copy[datetime_column] = df_copy[datetime_column].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df_copy


def convert_datetime_format_2(df, datetime_column):
    """
    Convert datetime strings in a DataFrame column to the "YYYY-MM-DD" format.

    Parameters:
    - df: DataFrame
        The DataFrame containing the datetime column.
    - datetime_column: str
        The name of the datetime column in the DataFrame.

    Returns:
    - DataFrame: A copy of the input DataFrame with the datetime column converted to the desired format.
    """
    # Make a copy of the DataFrame to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Convert datetime column to datetime type
    df_copy[datetime_column] = pd.to_datetime(df_copy[datetime_column])

    # Format datetime column to "YYYY-MM-DD" format
    df_copy[datetime_column] = df_copy[datetime_column].dt.strftime("%Y-%m-%d")

    return df_copy


def getInstruments():
    df = pd.read_csv('instruments.csv')
    return df



# test
activeTest = False
if activeTest:
    start_date = "2021-02-08 09:00"
    end_date = "2022-02-08 09:00"
    n = 30  # Interval of 30 days
    intervals = break_dates(start_date, end_date, n)
    print(intervals)
    df = getInstruments()
    print(df['name'])
