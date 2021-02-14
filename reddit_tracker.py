import datetime
import logging
import praw

reddit = praw.Reddit("tracker_bot")


def conv_time(posix_time):
    ''' Convert time from POSIX to string '''
    time = datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d')
    return time

def collect_subs(sub_name):
    ''' Collect posts from subreddits '''
    sub_list = []

    for submission in reddit.subreddit(sub_name).hot(limit=1):
        logging.info(submission.title)
        submission.comments.replace_more()
        sub_list = submission.comments.list()
    return sub_list

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
    start_time = '2021-01-01'
    sub_data = collect_subs('wallstreetbets')
    count = sum_new_accounts(start_time, sub_data)
    logging.info(count)
