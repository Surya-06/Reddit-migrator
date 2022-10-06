import praw
import os

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
OLD_USERNAME = os.getenv('REDDIT_USERNAME')
OLD_PASSWORD = os.getenv('REDDIT_PW')
OLD_CLIENT_ID = os.getenv('CLIENT_ID')
OLD_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
NEW_USERNAME = os.getenv('REDDIT_NEW_USERNAME')
NEW_PASSWORD = os.getenv('REDDIT_NEW_PW')
NEW_CLIENT_ID = os.getenv('NEW_CLIENT_ID')
NEW_CLIENT_SECRET = os.getenv('NEW_CLIENT_SECRET')

def get_user(old_account: bool):
    if old_account:
        return praw.Reddit(
            client_id = OLD_CLIENT_ID,
            client_secret = OLD_CLIENT_SECRET,
            username = OLD_USERNAME,
            password = OLD_PASSWORD,
            user_agent = USER_AGENT
        )
    else:
        return praw.Reddit(
            client_id = NEW_CLIENT_ID,
            client_secret = NEW_CLIENT_SECRET,
            username = NEW_USERNAME,
            password = NEW_PASSWORD,
            user_agent = USER_AGENT
        )

def migrate_subscriptions():

    old_account = get_user(old_account = True)

    print ( 'Logged in as the user : {}' , old_account.user.me() )
    print ( 'scopes : ' , old_account.auth.scopes() )

    subscribed_subreddits = old_account.user.subreddits(limit=None)

    new_reddit = get_user(old_account = False)

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


def migrate_preferences():
    old_user = get_user(old_account = True)
    new_user = get_user(old_account = False)

    old_preferences = old_user.user.preferences()
    new_preferences = new_user.user.preferences()


def show_preferences(old: bool):
    user = get_user(old_account = old)
    preferences = user.user.preferences()
    for pref in preferences:
        print(pref)


def show_subreddits(old: bool):
    user = get_user(old_account = old)
    subreddits = user.user.subreddits(limit = None)
    print("showing subreddits")
    for subreddit in subreddits:
        print(str(subreddit))


if __name__ == '__main__':
    print ( HELP_MESSAGE )
    print (
        '''
            Select an option:
            1. Migrate subreddits
            2. Migrate preferences
            3. Show old account subreddits
            4. Show new account subreddits
            5. Show old account preferences
            6. Show new account preferences
        '''
    )
    selection = input('Enter selection : ')
    selection = int(selection)

    if selection == 1:
        migrate_subscriptions()
    elif selection == 2:
        migrate_preferences()
    elif selection == 3:
        show_subreddits(old = True)
    elif selection == 4:
        show_subreddits(old = False)
    elif selection == 5:
        show_preferences(old = True)
    elif selection == 6:
        show_preferences(old = False)

