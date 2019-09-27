import re
import logging as log


class NameParser:

    def parse_text(self, text):
        return self.__get_name(text)

    def __get_name(self, text):
        """look for [[cardname]]s in text and collect them"""
        names = []

        # regex for escaped (new reddit and some apps) and unescaped brackets
        #for name in re.finditer(r'\\?\[\\?\[([^\]\\]{1,30})\\?\]\\?\]', text):
        for name in re.finditer(r'\\?\:\\?\:([^\:\\]{1,30})\\?\:\\?\:', text):
            name = name.group(1)
            if name not in names:
                names.append(name)
            else:
                log.info("duplicate name: %s", name)

        return names
