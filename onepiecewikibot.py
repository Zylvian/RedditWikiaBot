import os
import sys

import praw
from parse_helper import NameParser
from fetching import Fetcher
import logging as log


class RedditBot:

    def __init__(self):
        self.LOCK_FILE = 'lockfile.lock'
        self.fetcher = Fetcher()


        log.basicConfig(filename='bot_logging.log', level=log.INFO
                        )

    def _comment_responder(self):
        reddit = praw.Reddit('bot1')
        # answeredDB = commentDB.DB()

        subreddit = reddit.subreddit("onepiece")

        for comment in subreddit.stream.comments(skip_existing=True):
            if os.path.isfile(self.LOCK_FILE):
                text = comment.body
                names = NameParser().parse_text(text)
                if names:
                    pages = self.fetcher.get_wiki_pages(names)

                    response_string = ""

                    for page in pages:
                        curr_title = page["title"]
                        curr_url = page["fullurl"]
                        curr_image_url = self.fetcher.fetch_image_url()
                        response_string += ("##"+curr_title + "\n\n" + curr_url + " \n\n" + curr_image_url)

                    try:
                        comment.reply(response_string)
                        #log.info("replying to {user}: {response}".format(
                        #    user=comment.author.name, response=response_string))
                    except praw.exceptions.APIException as e:
                        log.info(str(e))

            else:
                return
        # for comment in subreddit.stream.comments():
        #    if not answeredDB.exists(comment.parent_id, cards):

    def run(self):
        # remove to kill
        with open(self.LOCK_FILE, 'w'): pass
        print("Lock file made (presumably)")
        log.info("STARTED")
        self._comment_responder()


if __name__ == '__main__':
    RedditBot().run()
