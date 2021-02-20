import datetime
from influxdb_client import InfluxDBClient, Point
import praw

reddit = praw.Reddit("tracker_bot")


def to_datetime(timestamp):
    ''' Convert from timestamp to datetime '''
    return datetime.datetime.fromtimestamp(timestamp)

def collect_data(sub_list, time_thres):
    ''' Collect posts from subreddits after specified time threshold '''
    data = []

    for sub_url in sub_list:
        sub = reddit.submission(url=sub_url)
        sub.comments.replace_more(limit=None)
        for comment_id in sub.comments.list():
            try:
                filtered_data = filter_created_utc(time_thres, comment_id)
            except Exception:
                continue
            if filtered_data is not None:
                data.append(filtered_data)

    return data

def collect_historical_subs(sub_name, query_str, start_time, end_time):
    ''' Return subs that match query in text
        of top submissions based on dates '''
    historical_subs = []

    for submission in reddit.subreddit(sub_name).top(limit=100):
        sub_time = conv_time(submission.created_utc)
        if query_str in submission.selftext and start_time <= sub_time <= end_time:
            historical_subs.append(submission.url)
        else:
            continue

    return historical_subs

def search(sub_name, query_str):
    ''' Return subs that match query string '''
    subs = []

    for submission in reddit.subreddit(sub_name).search(query_str):
        subs.append(submission)

    return subs

def collect_hot_subs(sub_name, query_str):
    ''' Return subs that match query in text of hot submissions '''
    hot_subs = []

    for submission in reddit.subreddit(sub_name).new(limit=10):
        sub_time = to_datetime(submission.created_utc)
        if query_str in submission.selftext:
            hot_subs.append(submission.url)
        else:
            continue

    return hot_subs

def filter_created_utc(time_thres, comment_id):
    ''' Traverse through replies from sub
        and extract DOB of new accounts
        based on threshold time
    '''
    date_time = datetime.datetime.strptime(time_thres, '%Y-%m-%d')
    comment = reddit.comment(id=f'{comment_id}')
    redditor_dob = to_datetime(comment.author.created_utc)

    if date_time <= redditor_dob:
        return {"measurement": "redditor_dob",
                "tags": {"subreddit": str(comment.subreddit)},
                "fields": {"created_utc_float": comment.author.created_utc, "comment_id": str(comment_id)},
                "time": redditor_dob}

