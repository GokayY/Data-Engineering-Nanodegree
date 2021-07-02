import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ 
    The function ais to load, process and load data within the song files.
    
    =======
    
    Params:
    
    cur : cursor object for db connection 
    filepath: string object for filepath
    
    Return:
    none
    
    """
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ 
    The function ais to load, process and load data within the log files.
    
    =======
    
    Params:
    
    cur : cursor object for db connection 
    filepath: string object for filepath
    
    returns:
    none
    
    """
    # open log file
    df =  pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.DataFrame(pd.to_datetime(df.loc[:,'ts'] , unit='ms'))
    df['timestamp'] = pd.to_datetime(df.loc[:,'ts'] , unit='ms')
    
    # insert time data records
    time_data = [t.ts.dt.values.tolist(),\
                 t.ts.dt.hour.values.tolist(),\
                 t.ts.dt.day.values.tolist(),\
                 t.ts.dt.weekofyear.values.tolist(),\
                 t.ts.dt.month.values.tolist(),\
                 t.ts.dt.year.values.tolist(),\
                 t.ts.dt.weekday.values.tolist()]
    column_labels = ['timestamp', 'hour', 'day', 'weekOfYear', 'month', 'year', 'weekday']
    
    time_dict = {}
    
    for key,value in zip(column_labels, time_data):
        time_dict[key] = value
        
    time_df = pd.DataFrame().from_dict(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'userAgent']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
            
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.timestamp, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Pipeline-like function for ETL process
    
    =======
    Params:
    
    cur: cursor object for db connection
    conn: connector to database
    filepath: string object for filepath
    func: Function for ETL process
    
    returns:
    none
    
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()