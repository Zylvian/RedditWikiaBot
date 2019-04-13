import json


class Constants():
    """wraps all constant data"""
    CARD_LIMIT = 7

    def __init__(self, constantJSON='data/constants.json'):
        with open(constantJSON, 'r', encoding='utf8') as file:
            constants = json.load(file)


        # alternative names
        self.__translations = {}
        for alt_names, actual_name in constants['alternative_names'].items():

            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    self.__translations[alt_name] = actual_name
            else:
                self.__translations[alt_names] = actual_name

        self.alternativeNames = self.__translations.keys()

    def translateAlt(self, card):
        """translate alternative card name or return card"""
        return self.__translations.get(card, card)