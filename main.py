import praw
import os
import argparse


HELP_MESSAGE = '''
    Quick tool to migrate your reddit subscriptions & preferences.

    NOTE:
    This requires a client ID & client secret to be generated in the source & destination accounts.

    Once they are handy, please set them in the environment using the following variable names:

    For the source account:
    REDDIT_USERNAME
    REDDIT_PW
    CLIENT_ID
    CLIENT_SECRET

    For the target account:
    REDDIT_NEW_USERNAME
    REDDIT_NEW_PASSWORD
    NEW_CLIENT_ID
    NEW_CLIENT_SECRET
'''

USER_AGENT = 'reddit migrator user agent'

def get_user(username, pw, client_id, client_secret):
    return praw.Reddit(
        client_id = client_id, 
        client_secret = client_secret, 
        username = username,
         password = pw,
         user_agent = USER_AGENT)

def migrate_subscriptions():
    reddit_username = os.getenv('REDDIT_USERNAME')
    reddit_pw = os.getenv('REDDIT_PW')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    old_account = get_user(
        reddit_username, 
        reddit_pw, 
        client_id, 
        client_secret)

    print ( 'Logged in as the user : {}' , old_account.user.me() )
    print ( 'scopes : ' , old_account.auth.scopes() )

    subscribed_subreddits = old_account.user.subreddits(limit=None)

    reddit_new_username = os.getenv('REDDIT_NEW_USERNAME')
    reddit_new_pw = os.getenv('REDDIT_NEW_PW')
    new_client_id = os.getenv('NEW_CLIENT_ID')
    new_client_secret = os.getenv('NEW_CLIENT_SECRET')

    new_reddit = get_user(
        reddit_new_username, 
        reddit_new_pw, 
        new_client_id, 
        new_client_secret)

    print ( 'New reddit account : ' , new_reddit.user.me() )
    print ( 'scopes : ' , new_reddit.auth.scopes() )

    new_account_subreddits = new_reddit.user.subreddits(limit=None)

    failed_subscriptions = []

    for subreddit in subscribed_subreddits:
        if subreddit not in new_account_subreddits:
            print ('attempting to subscribe to : ' , str(subreddit))
            try:
                new_reddit.subreddit(str(subreddit)).subscribe()
                print ( 'Successfully subscribed!' )
            except Exception as e:
                print ( 'Failed to subscribe to : ' , str(subreddit) )
                print ( 'Error : ' , e )

    print ( 'Subscriptions failed for : ' , len(failed_subscriptions) )
    for sub in failed_subscriptions:
        print ( 'Failed to subscribe to : ' , str(sub) )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Quick tool to migrate your reddit preferences & subscriptions')
    parser.add_argument('--subscribe', dest='migrate_subscriptions', help='Migrate subscriptions from old account to new account')
    args = parser.parse_args()

    



