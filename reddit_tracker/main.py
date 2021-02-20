from db import  db_read, db_connect, db_write
from reddit_tracker import collect_hot_subs, collect_data

if __name__ == '__main__':

    client = db_connect()
    subs = collect_hot_subs('wallstreetbets', 'a')
    data = collect_data(subs, '2019-01-01')
    db_write(client, 'reddit_tracker', data)
    db_read(client, 'reddit_tracker')

