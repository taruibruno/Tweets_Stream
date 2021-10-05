# Tweets_Stream
Script to get tweets in real time respecting the given rules and save them in a SQL database.

## Introduction
This project aims to collect real time tweets about COVID, Health and Vaccine subjects in Brazil and store them in a SQL database for further analysis. In this project were collected approximately 100,000 tweets along the day using the free API v2 from Twitter.

## Requirements
1. In order to access the Twitter API to collect the tweets stream, you need a twitter developer account. You can request one in this [link](https://developer.twitter.com/en/portal/dashboard)
2. Create a project in Twitter's developer page and get a valid bearer token.
3. You need access to a SQL database. 
    - For this project I used a local SQL server Express 2019, the instructions to install and set up the server can be found in this [video](https://www.youtube.com/watch?v=3o2xvWoNBIA&ab_channel=DENRICDENISE-INFO).
    - The table I used was created with the below SQL-T commands:
      ```
      CREATE TABLE twitter_stream (
        ID varchar(255) NOT NULL,
        Tag varchar(255),
        CreatedOn datetime
        );
      ```
    - **Note:** You can also use a database that already exists in a dedicated server or cloud service. You just need to make sure that you have the access to post data into the database. The table you use can also be different, as long as it has at least the following columns: ID, Tag and CreatedOn.
4. Python 3.0 or later.

## Analyzing the data
Once the data has been posted in your database, you can run queries to analyze the results. The examples of queries below are considering the table proposed on Step 3 in the **Requirements** section.
* Count the total number of tweets for each rule applied:
```
SELECT COUNT(ts.ID) as 'Tweets', ts.Tag
FROM twitter_stream as ts
Group by ts.tag
``` 

* Count the total number of tweets posted in each hour of the day:
```
SELECT COUNT(ts.ID) as 'Tweets', DATEPART(HOUR, ts.CreatedOn) as CreatedHourUTC
FROM twitter_stream as ts
GROUP BY DATEPART(HOUR, ts.CreatedOn)
ORDER BY DATEPART(HOUR, ts.CreatedOn) 
``` 

## References
If you want further information about the API and the code used here, please check below:
* [Creating rules for filtered stream API](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule)
* [Twitter filtered stream API quick start](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/quick-start)
* [Getting Started with Pyodbc](https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-ver15)
* [Guide to collect tweets using the API (Not using the stream filter)](https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a)

