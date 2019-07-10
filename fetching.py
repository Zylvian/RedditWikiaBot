import itertools
import string

import requests
import logging as log
from constants import Constants

""" 
S = requests.Session()

PARAMS = {
    "action": "query",
    "format": "json",
    "generator": "allpages",
    "gtitles":"Luffy",
    "list": "allimages"
}

url = 'https://onepiece.fandom.com/api.php'

print(requests.get(url=url, params=PARAMS).content)
"""


class Fetcher:

    def __init__(self):

        self.constants = Constants()

        self._querystartlink = None
        self._queryendlink = None

        self._imagestartlink = None
        self._summarystartlink = None


    def get_wiki_info(self, sub, names):

        # Always run this
        self.__change_wiki(sub)

        pages = []
        for name in names:
            try:
                checkedname = self.constants.translateAlt(name)

                pages.append(self.__fetch_page(checkedname))
            except KeyError:
                pass

        return_dict = self.__pages_to_list(pages)

        log.info("Input names: " + ",".join(names))

        return return_dict



    def __get_correct_page(self, checked_name, all_pages):
        # Gets first page
        first_page = None
        log_string = ""

        # clean_name = self.cleanName(checked_name)
        clean_name = checked_name.replace(" ", "+")

        # Checks for any direct hits.
        # difflib.get_close_matches[0]
        for nr, page in enumerate(all_pages.values()):
            title = page['title']
            title_clean = self.cleanName(title)
            log_string += title + ","
            if title_clean == clean_name:
                log.info("Found direct match, page nr {}: {}".format(nr + 1, clean_name))
                first_page = page
                break

        # Gets first entry
        if not first_page:
            first_page = next(iter(all_pages.values()))

        log.info(
            "Input name: {} \n Parsed titles were: {}.\n Result title was: {}".format(checked_name, log_string[:-1],
                                                                                      first_page["title"]))

        return first_page

    def __fetch_page(self, name):

        # Returns translated name or the same name
        # clean_name = self.cleanName(name)
        checked_name = self.constants.translateAlt(name.lower())

        # All pages with "name" in there, and their URLs.
        fetch_json = requests.get(self._querystartlink + checked_name.title()
                                  ).json()  # 'Use "gapfilterredir=nonredirects" option instead of "redirects" when using allpages as a generator' #gaplimit=1

        first_page = fetch_json["items"][0]

        return first_page

    def __fetch_image_url(self, page_id):

        image_json = requests.get(self._imagestartlink + str(page_id)).json()

        try:
            image_url_dirty = image_json["image"]["imageserving"]
            image_url = (image_url_dirty.split("/revision/"))[0]

            return image_url
        except KeyError:
            log.info("Couldn't parse image url")
            return ""

    def __fetch_summary(self, page_id):

        fetch_json = requests.get(self._summarystartlink + str(page_id)).json()

        try:
            return fetch_json["sections"][0]["content"][0]["text"]
        except: #If there is no summary.
            return ""

    def __change_wiki(self, sub):

        wiki_name = self.constants.sub_to_wiki(sub.lower())
        wiki_site = 'https://{wiki_name}.fandom.com'.format(wiki_name=wiki_name)

        self._querystartlink = wiki_site + '/api/v1/Search/List?query='
        self._queryendlink = '&limit=1&minArticleQuality=10&batch=1&namespaces=0%2C14'

        self._imagestartlink = wiki_site + '/api.php?format=json&action=imageserving&wisId='
        self._summarystartlink = wiki_site + "/api/v1/Articles/AsSimpleJson?id="

    def __pages_to_list(self, pages):

        return_list = []

        for page in pages:
            info_dict = {}
            info_dict["title"] = page["title"]
            # all_titles.append(curr_title)
            info_dict["url"] = page["url"]

            curr_id = page["id"]
            info_dict["summary"] = self.__fetch_summary(curr_id)
            info_dict["image_url"] = self.__fetch_image_url(curr_id)

            return_list.append(info_dict)

        return return_list

    def get_subs_to_check(self):
        return self.constants.get_subs_to_check()


class SpellChecker():
    """Find and fix simple spelling errors.
    based on Peter Norvig
    http://norvig.com/spell-correct.html
    """

    def __init__(self, names):
        self.model = set(names)

    def __known(self, words):
        for w in words:
            if w in self.model:
                return w
        return None

    def __edits(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = (a + b[1:] for a, b in splits if b)
        transposes = (a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1)
        replaces = (a + c + b[1:] for a, b in splits for c in string.ascii_lowercase if b)
        inserts = (a + c + b for a, b in splits for c in string.ascii_lowercase)
        return itertools.chain(deletes, transposes, replaces, inserts)

    def correct(self, word):
        """returns input word or fixed version if found"""
        return self.__known([word]) or self.__known(self.__edits(word)) or word

    """
    # distance 2
    def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    """

# Test
# print(requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=info').content) #prop=info&inprop=url


# image_json = requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=images').json()
# print(image_json)
# test_output = image_json['query-continue']['']

# All images from the Monkey D. Luffy page
# print(requests.get('https://onepiece.fandom.com/api.php?format=json&action=query&generator=images&titles=Monkey_D._Luffy&prop=imageinfo').content)
