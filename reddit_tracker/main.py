import argparse
import praw
from db import  check_exists, db_connect, db_write
from reddit_collect import extract_comments, collect_hot_subs, collect_historical_subs, collect_data


def reddit_monitor(bucket, org, subreddit,
                   keyword, time_thres,
                   date_from, date_to):
    client=db_connect()

    subs = collect_historical_subs(subreddit, keyword, date_from, date_to)
    for sub_url in subs:
        comment_id = extract_comments(sub_url)
        sub_attrs = collect_data(comment_id, time_thres)
        if sub_attrs is not None:
            subs = sub_attrs['time'].isoformat()[:-7]+'Z'
            exists = check_exists(client, bucket, subs)
            if not exists:
                db_write(client, bucket, org, sub_attrs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(--bucket, help="bucket's name (influxdb)")
    parser.add_argument(--org, help="organization's name (influxdb)")
    parser.add_argument(--subreddit, help="subreddit's name")
    parser.add_argument(--keyword, help="keyword to search for in submission's body")
    parser.add_argument(--time_thres, help="redditor's account creation date to extract")
    parser.add_argument(--date_from, help="lower date limit of submission to extract")
    parser.add_argument(--date_to, help="upper date limit of submission to extract")

   reddit_monitor(bucket, org, subreddit,
                  keyword, time_thres,
                  date_from, date_to)
