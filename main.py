import argparse

from reddit_to_twitter import RedditToTwitter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddit", help="Select the subreddit. Default: Aww", action='store', default='Aww')
    parser.add_argument("-t", "--top", help="Choose the top day / hour / all. Default: hour", action='store',
                        default='hour')
    parser.add_argument("-w", "--hashtag", help="Add a random word from hashtags.txt as hashtags", action='store_true')
    args = parser.parse_args()
    reddit_to_twitter = RedditToTwitter(args=args)
    reddit_to_twitter.run()
