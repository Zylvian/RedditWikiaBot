import itertools

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
        self._startlink = 'https://onepiece.fandom.com/api.php?format=json&action=query&'
        self.constants = Constants()

    def get_wiki_links(self, names):
        nls = []
        for name in names:
            nls.append(self.__fetch_link(name))

        return nls


    def __fetch_link(self, name):

        # Returns translated name or the same name
        checked_name = self.constants.translateAlt(name.lower())

        # All pages with "name" in there, and their URLs.
        fetch_json = requests.get(self._startlink + 'generator=allpages&gapfrom=' + checked_name +
                                  '&prop=info&inprop=url').json() #'Use "gapfilterredir=nonredirects" option instead of "redirects" when using allpages as a generator' #gaplimit=1

        # Gets the first page
        all_pages = fetch_json['query']['pages']
        # Gets first page
        first_page = None
        log_string = ""


        # Checks for any direct hits.
        for nr, page in enumerate(all_pages.values()):
            title = page['title']
            title_low = title.lower()
            log_string += title + ","
            if title_low == checked_name.lower():
                log.info("Found direct match, page nr {}: {}".format(nr + 1, checked_name))
                first_page = page
                break

        # Gets first entry
        if not first_page:
            first_page = next(iter(all_pages.values()))

        log.info("Input name: {} \n Parsed titles were: {}.\n Result title was: {}".format(checked_name, log_string[:-1],
                                                                                           first_page["title"]))
        # Gets first url
        first_title = first_page["title"]
        first_url = first_page["fullurl"]

        # THIS IS THE URL WE NEED AT LEAST

        return (first_title, first_url)

        # ASSUME THAT THE FIRST LINK IS CORRECT - MIGHT BE REDIRECTION LINK!



        def check_title(self):
            pass



# Test
#print(requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=info').content) #prop=info&inprop=url


#image_json = requests.get(startlink+'generator=allpages&gapfrom=Luffy&prop=images').json()
#print(image_json)
#test_output = image_json['query-continue']['']

#All images from the Monkey D. Luffy page
#print(requests.get('https://onepiece.fandom.com/api.php?format=json&action=query&generator=images&titles=Monkey_D._Luffy&prop=imageinfo').content)