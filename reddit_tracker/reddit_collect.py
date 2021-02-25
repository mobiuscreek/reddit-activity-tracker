import datetime
from influxdb_client import InfluxDBClient, Point
import praw

reddit = praw.Reddit("tracker_bot") # provided by praw.ini


def to_datetime(timestamp):
    ''' Convert from timestamp to datetime '''
    return datetime.datetime.fromtimestamp(timestamp)

def collect_data(comment_id, time_thres):
    ''' Collect posts from subreddits after specified time threshold '''
    comment = reddit.comment(id=f'{comment_id}')
    redditor_dob = filter_created_utc(time_thres, comment)
    if redditor_dob is not None:
        return {"measurement": "redditor_dob",
                "tags": {"subreddit": str(comment.subreddit)},
                "fields": {"created_utc_float": comment.author.created_utc, "comment_id": str(comment_id)},
                "time": datetime.datetime.now()}

def extract_comments(sub_url):
    sub = reddit.submission(url=sub_url)
    sub.comments.replace_more(limit=None)
    for comment_id in sub.comments.list():
        return comment_id


def collect_historical_subs(sub_name, query_str, start_time, end_time):
    ''' Return subs that match query in text
        of top submissions based on dates '''
    historical_subs = []
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    for submission in reddit.subreddit(sub_name).top(limit=500):
        sub_time = to_datetime(submission.created_utc)
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

def filter_created_utc(time_thres, comment):
    ''' Extract DOB of new accounts
        based on threshold datetime
    '''
    date_time = datetime.datetime.strptime(time_thres, '%Y-%m-%d')
    try:
        redditor_dob = to_datetime(comment.author.created_utc)
    except Exception: ## Needs better handling
        return None

    if date_time <= redditor_dob:
        return redditor_dob
    else:
        return None
