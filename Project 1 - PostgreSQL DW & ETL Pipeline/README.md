Udacity Data Engineering NanoDegree PostgreSQL Data Modelling and ETL process submission

Dataset can be found in data folder in different json files. 
ETL Process includes:
- Extracting the data from json files with Python sripts
- Transforming the data with Python scripts 
- Creating Database, data tables and necessary scripts to use in python scripts
- Loading the data into Fact and Dimension tables

This data warehouse acts as single source of truth for the company and all the necessary analysis can be done through this data warehouse. Thus, it is really important to maintain and improve the data warehouse. 

There are 5 tables in the database and these tables are fact and dimension tables in a star schema. While songplays table is the fact table, the rest of the tables act as dimension tables for read performance for any reporting and analysis purposes. These tables, attributes and their data types are as follows:

1) songplays 
- songplay_id int 
- start_time varchar
- user_id int
- level varchar
- song_id varchar
- artist_id varchar
- session_id int
- location varchar
- user_agent varchar

2) users 
- user_id int
- first_name varchar
- last_name varchar
- gender char
- user_agent varchar

3) songs 
- song_id varchar
- title varchar
- artist_id varchar
- year int
- duration float

4) artists 
- artist_id varchar
- artist_name varchar
- artist_location varchar
- artist_latitude float
- artist_longitude float

5) time 
- timestamp varchar
- hour int
- day int
- weekOfYear int
- month int
- year int
- weekday int

ETL Pipeline is created according to the needs and running "create_tables.py" and "etl.py" files will populate the tables in PostgreSQL database.