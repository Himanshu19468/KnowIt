import requests
import pandas as pd


# URL for the JSON file


def getall():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

    # Fetch data from the URL
    response = requests.get(url)
    data = response.json()

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Display the first few rows of the DataFrame
    print(df.shape)

    df.to_csv('instruments.csv', index=False)


def filter():
    import csv

    input_file_path = 'instruments.csv'
    output_file_path = 'equity.csv'

    with open(input_file_path, mode='r', newline='') as infile, open(output_file_path, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()  # Write headers to output file

        for row in reader:
            if '-EQ' in row['symbol']:
                writer.writerow(row)  # Write rows that meet the condition




getAll = False
if getAll:
    getall()


filter_ = True
if filter_:
    filter()










