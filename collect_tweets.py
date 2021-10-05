# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 00:36:09 2021

@author: taruibrunopc
"""

# For sending requests for the API
import requests

# For dealing with json responses we receive from the API
import json

# For connect to the SQL database
import pyodbc

#For managing and parsing date time formats
import datetime

#Bearer token from your twitter API project:
bearer_token = "<add_your_bearer_token>"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules():
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "COVID lang:pt", "tag": "Covid rule"},
        {"value": "Saúde lang:pt", "tag": "Health rule"},
        {"value": "Vacina lang:pt", "tag": "Vaccine rule"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream():
    #Filtered stream request including the extra field "Created_at"
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    #print request error, if there is any
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        #Make sure you post a valid response line
        if response_line:
            json_response = json.loads(response_line)
            tweet_id = json_response["data"]["id"]
            created = datetime.datetime.strptime(json_response["data"]["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
            #If a tweet is caught by two or more rules, there will be one entry in the database for each rule
            if len(json_response["matching_rules"]) > 1:
                for tag in json_response["matching_rules"]:
                    rule = tag["tag"]
                    post_sql(connect_sql(), tweet_id, rule, created)
            else:
                rule = json_response["matching_rules"][0]["tag"]
                post_sql(connect_sql(), tweet_id, rule, created)
         

def connect_sql():
    server = '<your_server_name>'
    db = '<your_DB_Name>'
    
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=' + server + ';'
                      'Database=' + db + ';'
                      'Trusted_Connection=yes;')
    return connection

def post_sql(conn,tweet_id,rule,created):
    cursor = conn.cursor()

    cursor.execute("""
                INSERT INTO twitter_stream (ID, Tag, CreatedOn)
                VALUES             
                (?,?,?)
                """, tweet_id, rule, created)
    conn.commit()

def main():
    
    #Delete the current rules applied to the filtered stream
    delete_all_rules(get_rules())
    
    #Set rules for the filtered stream
    set_rules()
    
    #Get the tweets and post them in the Database
    get_stream()
    
if __name__ == "__main__":
    main()
