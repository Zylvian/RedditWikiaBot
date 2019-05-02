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

    def create_response_string(self, pages):

        response_string = ""

        for page in pages:
            curr_title = page["title"]
            curr_url = page["url"]
            curr_id = page["id"]
            curr_image_url = self.fetcher.fetch_image_url(curr_id)
            curr_summary = self.fetcher.fetch_summary(curr_id)
            response_string += ("#[{title}]({image_url})\n\n###*{summary}*\n\n{url}".format(title=curr_title, url=curr_url,
                                                                                         image_url=curr_image_url,
                                                                                         summary=curr_summary))
        return response_string

    def _comment_responder(self):
        reddit = praw.Reddit('bot1')
        # answeredDB = commentDB.DB()

        subreddit = reddit.subreddit("onepiece+memepiece")

        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                if os.path.isfile(self.LOCK_FILE):
                    text = comment.body
                    # Finds all text within brackets.
                    names = NameParser().parse_text(text)
                    if names:
                        pages = self.fetcher.get_wiki_pages(names)

                        response_string = self.create_response_string(pages) + "\n"

                        try:
                            comment.reply(response_string)
                            # log.info("replying to {user}: {response}".format(
                            #    user=comment.author.name, response=response_string))
                        except praw.exceptions.APIException as e:
                            log.info(str(e))

                else:
                    return
            except Exception as e:
                log.info(str(e))
                if text:
                    log.info('Comment: "' + text + '"')
                else:
                    log.info("Couldn't parse comment.")

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
