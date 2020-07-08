import praw
import json
import requests
import time
import re
from datetime import datetime, timedelta

file = open('textFiles/secrets.txt', 'r')
login_info = file.read().split('\n')

reddit = praw.Reddit(client_id=     login_info[0],
                    client_secret=  login_info[1],
                    username=       login_info[2],
                    password=       login_info[3],
                    user_agent=     login_info[4]
                    )
print("Logged in as u/" + str(reddit.user.me()))


def main():
    while True:
        for new_comment in reddit.inbox.unread(limit=100):
            parent1_id=new_comment_id=parent2_body=parent2_comment=parent2_id=submission_body=submission_title=parent1_comment=submission= ''
            new_comment_id = new_comment.fullname

            if new_comment_id.startswith('t1_') and 'u/undeleteparent' in new_comment.body.lower():
                parent1_id = get_parent_id(new_comment)

                if parent1_id.startswith('t1_'):
                    parent1_comment = reddit.comment(parent1_id[3:])
                    parent2_id = get_parent_id(parent1_comment)
                    
                    if parent2_id.startswith('t1_'):
                        parent2_comment = reddit.comment(parent2_id[3:])
                        parent2_body = get_comment_data(parent2_id)

                        if parent2_comment.body != '[removed]':
                            print("UNDELETE COMMENT")
                            try:
                                reply_comment(new_comment, parent2_body)
                            except:
                                print("I AM BANNED IN r/" + str(new_comment.subreddit))
                                print("SEND PM")
                                try:
                                    pm_comment(new_comment, parent2_body)
                                except:
                                    print("User has disallowed PMs from strangers")
                        else:
                            print("MOD-DELETED COMMENT. SEND PM.")
                            try:
                                pm_comment(new_comment, parent2_body)
                            except:
                                print("User has disallowed PMs from strangers")
                        new_comment.mark_read()

                    else:
                        print("Replied to wrong comment? Ignore?")

                elif parent1_id.startswith('t3_'):
                    submission = reddit.submission(parent1_id[3:])
                    submission_title, submission_body = get_submission_data(submission.id)
                    
                    if submission.selftext != '[removed]':
                        print("UNDELETE SUBMISSION")
                        try:
                            reply_submission(new_comment, submission_title, submission_body)
                        except:
                            print("I AM BANNED IN r/" + str(new_comment.subreddit))
                            print("SEND PM")
                            try:
                                pm_submission(new_comment, submission_title, submission_body)
                            except:
                                print("User has disallowed PMs from strangers")
                    else:
                        print("MOD-DELETED SUBMISSION. SEND PM.")
                        try:
                            pm_submission(new_comment, submission_title, submission_body)
                        except:
                            print("User has disallowed PMs from strangers")
                    new_comment.mark_read()
            
            else:
                # Not a comment. If t4_ it is a ban notification. Otherwise idk wtf it is so just mark it as read.
                new_comment.mark_read()
                



def get_parent_id(comment):
    return comment.parent_id

def get_submission_data(id):
    url = 'https://api.pushshift.io/reddit/search/submission/?ids=' + str(id)
    response = requests.get(url)
    submission_json = response.json()
    try:
        submission_title = submission_json['data'][0]['title']
    except:
        submission_title = ''
    try:
        submission_body = submission_json['data'][0]['selftext']
    except:
        submission_body = ''
    return submission_title, submission_body

def get_comment_data(id):
    url = 'https://api.pushshift.io/reddit/search/comment/?ids=' + str(id)
    response = requests.get(url)
    comment_json = response.json()
    comment_body = comment_json['data'][0]['body']
    return comment_body

def pm_comment(new_comment, parent2_body):
    source = 'https://www.reddit.com' + reddit.comment(new_comment).permalink
    reddit.redditor(str(new_comment.author)).message('Undeleted comment from r/'+str(new_comment.subreddit), 'I am banned in r/' + str(new_comment.subreddit) + ' and/or this comment was removed by the moderators of said subreddit. \n\nUNDELETED comment: \n\n>' + parent2_body + '\n\n' + source + '\n\nI am a bot\n\n^please ^pm ^me ^if ^I ^mess ^up\n\n---\n\nconsider [supporting me?](https://paypal.me/undeleteparent)')

def reply_comment(new_comment, parent2_body):
    new_comment.reply("UNDELETED comment: \n\n>" + parent2_body + "\n\nI am a bot\n\n^please ^pm ^me ^if ^I ^mess ^up\n\n---\n\nconsider [supporting me?](https://paypal.me/undeleteparent)")

def pm_submission(new_comment, submission_title, submission_body):
    source = 'https://www.reddit.com' + reddit.comment(new_comment).permalink
    reddit.redditor(str(new_comment.author)).message('Undeleted submission from r/'+str(new_comment.subreddit), 'I am banned in r/' + str(new_comment.subreddit) + ' and/or this submission was removed by the moderators of said subreddit. \n\nUNDELETED submission: \n\nTitle:\n\n>' + submission_title + '\n\nBody:\n\n>' + submission_body + '\n\n' + source + '\n\nI am a bot\n\n^please ^pm ^me ^if ^I ^mess ^up\n\n---\n\nconsider [supporting me?](https://paypal.me/undeleteparent)')

def reply_submission(new_comment, submission_title, submission_body):
    new_comment.reply('UNDELETED submission: \n\nTitle:\n\n>' + submission_title + '\n\nBody:\n\n>' + submission_body + '\n\nI am a bot\n\n^please ^pm ^me ^if ^I ^mess ^up\n\n---\n\nconsider [supporting me?](https://paypal.me/undeleteparent)')

if __name__ == "__main__":
    main()