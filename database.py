from scraper import * 
import pandas as pd 
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv
import os 
 
load_dotenv()

functions = [league_table,top_scorers,detail_top,player_table,all_time_winner_club,top_scorers_seasons,goals_per_season]

conn_string = os.getenv('DB_CONN_STRING')

db = create_engine(conn_string)
conn = db.connect()
for fun in functions:
    function_name = fun.__name__
    result_df = fun()
    result_df.to_sql(function_name, con=conn,if_exists='replace', index=False)
    print(f'data pushed for {function_name}')

#close db connection
conn.close()