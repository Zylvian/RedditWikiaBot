import os

import praw
from parse_helper import NameParser
from fetching import Fetcher
import logging as log


class RedditBot:

    def __init__(self):
        self.LOCK_FILE = 'lockfile.lock'

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
                    nl_tuple_list = Fetcher().get_wiki_links(names)
                    response_string = ""
                    for name, link in nl_tuple_list:
                        response_string += (name + ": " + link + " \n\n")

                    try:
                        comment.reply(response_string)
                        log.info("replying to {user}: {response}".format(
                            user=comment.author.name, response=response_string))
                    except praw.exceptions.APIException:
                        log.info("Hit rate limit, skipping message...")

            else:
                return
        # for comment in subreddit.stream.comments():
        #    if not answeredDB.exists(comment.parent_id, cards):

    def run(self):
        # remove to kill
        with open(self.LOCK_FILE, 'w'): pass
        print("Lock file made (presumably)")

        self._comment_responder()


if __name__ == '__main__':
    RedditBot().run()
