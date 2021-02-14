import datetime
import logging
import praw

reddit = praw.Reddit("tracker_bot")


def conv_time(posix_time):
    ''' Convert time from POSIX to string '''
    time = datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d')
    return time

def collect_comments(sub_list):
    ''' Collect posts from subreddits '''
    comments = []

    for sub_url in sub_list:
        sub = reddit.submission(url=sub_url)
        sub.comments.replace_more(limit=None)
        for comment_id in sub.comments.list():
            comments.append(comment_id)

    return comments

def collect_historical_subs(sub_name, query_str, start_time, end_time):
    ''' Return subs that match query in text of top submissions based on dates'''
    historical_subs = []

    for submission in reddit.subreddit(sub_name).top(limit=100):
        sub_time = conv_time(submission.created_utc)
        if query_str in submission.selftext and start_time <= sub_time <= end_time:
            historical_subs.append(submission.url)
        else:
            continue

    return historical_subs


def collect_hot_subs(sub_name, query_str):
    ''' Return subs that match query in text of hot submissions '''
    historical_subs = []
    for submission in reddit.subreddit(sub_name).search(query):
        if conv_time(submission.created_utc) == '2021-01-27':
            historical_subs.append(submission.title)
        else:
            continue
    print(historical_subs)


def sum_new_accounts(start_time, sub_list):
    ''' Traverse through replies from sub
        and extract DOB of new accounts
        based on start_time
    '''
    count = 0
    for comment_id in sub_list:
        comment = reddit.comment(id=f'{comment_id}')

        try:
            creation_time = conv_time(comment.author.created_utc)
        except AttributeError:
            continue
        if start_time >= creation_time:
            count += 1
    return count

if __name__ == '__main__':
  #  start_time = '2021-01-01'
  #   sub_data = collect_subs('wallstreetbets')
  #  count = sum_new_accounts(start_time, sub_data)
  #  logging.info(count)
  collect_historical_subs('wallstreetbets', 'GME')
