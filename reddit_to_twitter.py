import json
import praw
import random
import re
import requests
import shutil
import tweepy

from pathlib import Path


class RedditToTwitter:
    def __init__(self,
                 args):
        self._top_since = args.top
        self._subreddit = args.subreddit
        self._hashtag = args.hashtag

        self._reddit = None
        self._tweeter = None
        self._posts = {}

    def _connect_reddit(self):
        if Path(f'{Path(__file__).parents[0]}/reddit_token.json').is_file():
            with open(f'{Path(__file__).parents[0]}/reddit_token.json', 'r') as reddit_token:
                data = json.load(reddit_token)
                client_id = data["client_id"]
                client_secret = data["client_secret"]
                username = data["username"]
                password = data["password"]
        try:
            self._reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent="twitter",
            )
        except praw.prawcore.OAuthException as error:
            print(error)

    def _connect_twitter(self):
        if Path(f'{Path(__file__).parents[0]}/twitter_token.json').is_file():
            with open(f'{Path(__file__).parents[0]}/twitter_token.json', 'r') as reddit_token:
                data = json.load(reddit_token)
                access_token = data["access_token"]
                access_secret = data["access_secret"]
                api_key = data["api_key"]
                api_secret = data["api_secret"]
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(auth)
        else:
            print('Twitter token file is missing')

    def _build_text(self, text):
        text = re.sub('[\(\[].*?[\)\]]', "", text)
        if self._hashtag and Path(f'{Path(__file__).parents[0]}/hashtag.txt').is_file():
            with open(f'{Path(__file__).parents[0]}/hashtag.txt', 'r') as hashtag_file:
                hashtag_list = hashtag_file.read().split('\n')
                text += f' #{random.choice(hashtag_list)}'
        text = re.sub('\\s+', ' ', text)
        return text.strip()

    def _get_reddit_post(self):
        subreddit = self._reddit.subreddit(self._subreddit)
        for i, submission in enumerate(subreddit.top(self._top_since)):
            if submission.url and submission.url.endswith('.jpg'):
                url_split = submission.url.split('/')
                file = f'/tmp/{url_split[len(url_split) - 1]}'
                if not Path(file).is_file():
                    response = requests.get(submission.url, stream=True)
                    with open(file, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    text = self._build_text(submission.title)
                    self._posts[i] = {'text': text, 'url': submission.url,
                                      'file': file}
                    print(self._posts[i])
                else:
                    print('The file already exist.')

    def _post_tweeter(self):
        for post in self._posts:
            print(f'Uploading file {self._posts[post]["file"]} with text {self._posts[post]["text"]}')
            self.api.update_status_with_media(filename=self._posts[post]["file"], status=self._posts[post]["text"])

    def run(self):
        self._connect_reddit()
        self._connect_twitter()
        self._get_reddit_post()
        self._post_tweeter()
