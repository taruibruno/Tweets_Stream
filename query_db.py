# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 02:35:47 2021

@author: taruibrunopc
"""
# To connect to the SQL database
import pyodbc

# Pandas used to run the SQL query
import pandas as pd

def connect_sql():
    server = 'DESKTOP-C6B6BST\SQLEXPRESS2019'
    db = 'Hilab_test'
    
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=' + server + ';'
                      'Database=' + db + ';'
                      'Trusted_Connection=yes;')
    return connection

def query_sql(conn,query):
    
    #Run the query using Pandas
    df = pd.read_sql_query(query, conn)
    
    #Print the results
    print(df)
    
def main():
    q1 = """
            SELECT COUNT(ts.ID) as 'Tweets', ts.Tag 
            FROM twitter_stream as ts 
            Group by ts.tag
        """
    
    q2 = """
        SELECT COUNT(ts.ID) as 'Tweets', DATEPART(HOUR, ts.CreatedOn) as CreatedHourUTC
        FROM twitter_stream as ts
        GROUP BY DATEPART(HOUR, ts.CreatedOn)
        ORDER BY DATEPART(HOUR, ts.CreatedOn)
    """
    
    query_sql(connect_sql(), q1)
    print('\n')
    query_sql(connect_sql(), q2)
    
if __name__ == "__main__":
    main()