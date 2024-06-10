from scraper import *
import pandas as pd 
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

functions = [league_table,top_scorers,detail_top,player_table,all_time_winner_club,top_scorers_seasons,goals_per_season]

def to_blob(func):
    '''
    This function converts the output of a given function to Parquet format and uploads it to the Azure Blob Storage
    Args:
        func (function): The function that retrieves data to process and upload
    Returns:
        None
    
    This function takes a provided function and will call it to get data, convert the data,
    and create an arrow table. The arrow table is serialized into Parquet format and uploaded to an 
    Azure Blob Storage container which is specified. The functions name is used as the blob name

    Example: 
        Take a function called "scorers", to_blob(scorers) will process
        the output of scorers and convert it to Parquet format which is then uploaded to the Azure Blob Storage
    '''

    file_name = func.__name__
    func = func()

    #convert df to arrow table
    table = pa.Table.from_pandas(func)

    parquet_buffer = BytesIO()
    pq.write_table(table,parquet_buffer)

    connection_string = os.getenv('BLOB_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "wsoccerblob"
    blob_name = f"{file_name}".parquet
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(parquet_buffer.getvalue(),overwrite=True)
    print(f"{blob_name} updated successfully")

for items in functions:
    to_blob(items)
