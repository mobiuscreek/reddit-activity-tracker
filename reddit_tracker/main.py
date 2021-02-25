import praw
from db import  check_exists, db_connect, db_write
from reddit_collect import extract_comments, collect_hot_subs, collect_historical_subs, collect_data

reddit = praw.Reddit("tracker_bot")

if __name__ == '__main__':
    client = db_connect()
    subs = collect_historical_subs('wallstreetbets', 'GME')
    for sub_url in subs:
        comment_id = extract_comments(sub_url)
        sub_attrs = collect_data(comment_id, '2020-01-01')
        if sub_attrs is not None:
            subs = sub_attrs['time'].isoformat()[:-7]+'Z'
            exists = check_exists(client, 'reddit_tracker', subs)
            if not exists:
                db_write(client, 'reddit_tracker', 'home', sub_attrs)
