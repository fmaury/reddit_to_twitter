if Path('reddit_token.json').is_file():
    with open('reddit_token.json', 'r') as reddit_token:
        data = json.load(reddit_token)
        client_id = data["client_id"]
        client_secret = data["client_secret"]
        username = data["username"]
        password = data["password"]
try:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="twitter",
    )
except praw.prawcore.OAuthException as error:
    print(error)

subreddit = reddit.subreddit("Aww")
for submission in subreddit.top('hour'):
    if submission.url:
        print(submission.title)
        print(submission.url)
