import os
import time
from bs4 import BeautifulSoup
import requests
from scraper import *  # Ensure this module is correctly implemented
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Manually set the environment variables
os.environ['DB_CONN_STRING'] = os.getenv('DB_CONN_STRING')
os.environ['AZURE_BLOB_CONN_STRING'] = os.getenv('AZURE_BLOB_CONN_STRING')

# Define the scraping functions
def league_table():
    url = "http://example.com/league_table"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table_data = []
    table = soup.find('table')
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        table_data.append([col.text for col in cols])
    df = pd.DataFrame(table_data)
    return df

functions = [league_table]  

# Verify the connection strings
db_conn_string = os.getenv('DB_CONN_STRING')
blob_conn_string = os.getenv('AZURE_BLOB_CONN_STRING')

print(f"Database connection string: '{db_conn_string}'")
print(f"Blob connection string: '{blob_conn_string}'")

# retry database connection
def connect_to_db(retries=5, delay=5):
    for i in range(retries):
        try:
            db = create_engine(db_conn_string)
            conn = db.connect()
            print("Database connection established")
            return conn
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e

# Create database engine with retry
try:
    conn = connect_to_db()
    for fun in functions:
        function_name = fun.__name__
        result_df = fun()
        result_df.to_sql(function_name, con=conn, if_exists='replace', index=False)
        print(f'Data pushed for {function_name}')
    # Close db connection
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")

# Create BlobServiceClient
try:
    blob_service_client = BlobServiceClient.from_connection_string(blob_conn_string)
    print("Blob service client created successfully.")
except Exception as e:
    print(f"Error creating BlobServiceClient: {e}")

# Example function to upload a file to Azure Blob Storage
def upload_file_to_blob(container_name, file_path, blob_name):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f'Uploaded {file_path} to container {container_name} as blob {blob_name}')
    except Exception as e:
        print(f"Error uploading file to blob: {e}")
# Example usage
# upload_file_to_blob('testtech', 'path_to_your_file', 'file_name_in_blob')

