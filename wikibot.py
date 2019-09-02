import os
import sys
import time

import praw
from prawcore import PrawcoreException

from constants import Constants
from parse_helper import NameParser
from fetching import Fetcher
import logging as log


class RedditBot:

    def __init__(self):
        self.LOCK_FILE = 'lockfile.lock'

        self._subs_to_check = "onepiece+memepiece+rickandmorty"

        self.fetcher = Fetcher()

        self._subs_to_check = self.fetcher.get_subs_to_check()

        """self.constants = Constants()

        self.fetcher_dict = self.constants.fetchers"""

        # self._subs_to_check = "+".join(self.fetcher_dict.keys())

        log.basicConfig(filename='bot_logging.log', level=log.INFO
                        )

    def create_response_string(self, info_dict):

        response_string = ""

        all_titles = list()
        for page in info_dict:
            curr_title = page["title"]
            curr_url = page["url"]
            curr_image_url = page["image_url"]
            curr_summary = page["summary"]

            all_titles.append(curr_title)

            response_string += ("#[{title}]({image_url})\n\n"
                                "#####*{summary}*\n\n"
                                "{url}\n\n".
                                format(title=curr_title, url=curr_url,
                                       image_url=curr_image_url,
                                       summary=curr_summary))

        log.info("Commenting about:" + (",".join(all_titles)))

        if response_string == "":
            response_string = "##*Didn't find any results.*\n\n"

        response_string += "---\n\n^(*For any feedback on this bot,*) [^(*send a DM to u/Zylvian.*)](https://www.reddit.com/message/compose?to=Zylvian&subject=Wikia Bot feedback&message=ay suck my dick)"

        return response_string

    def _comment_responder(self):
        reddit = praw.Reddit('bot1')
        # answeredDB = commentDB.DB()

        subreddit = reddit.subreddit(self._subs_to_check)
        print(self._subs_to_check)
        parser = NameParser()

        for comment in subreddit.stream.comments(skip_existing=True):

            if os.path.isfile(self.LOCK_FILE):

                # Parse the comment
                text = comment.body
                # Finds all text within brackets.
                names = parser.parse_text(text)

                if names:


                    curr_sub = comment.subreddit.display_name
                    info_dict = self.fetcher.get_wiki_info(curr_sub, names)
                    response_string = self.create_response_string(info_dict) + "\n"

                    try:
                        comment.reply(response_string)
                        # log.info("replying to {user}: {response}".format(
                        #    user=comment.author.name, response=response_string))
                    except praw.exceptions.APIException as e:
                        log.info(str(e))


            else:
                return

        # for comment in subreddit.stream.comments():
        #    if not answeredDB.exists(comment.parent_id, cards):

    def run(self):
        with open(self.LOCK_FILE, 'w'): pass
        print("Lock file made (presumably)")
        log.info("STARTED")
        # remove to kill

        self.run_cont()

    def run_cont(self):

        try:
            self._comment_responder()
        except PrawcoreException as e:
            log.info(e)
            log.info("Sleeping for 1 minute...")
            time.sleep(60)
            self.run_cont()
        except KeyboardInterrupt:
            raise
        except:
            log.info("Something random happened, sleeping for 10 sec.")
            time.sleep(60)
            self.run_cont()

if __name__ == '__main__':
    RedditBot().run()
