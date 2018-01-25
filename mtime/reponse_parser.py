import re
import json


class ResponseParser:
    def url_parser(self, response):
        """
        Get all hot showing movies' basic information.
        response: str -> list of dicts.
        Ex:
            [
                {"Id":227232,"Url":"http://movie.mtime.com/227232/","Title":"勇敢者游戏：决战丛林"},
                {"Id":249736,"Url":"http://movie.mtime.com/249736/","Title":"神秘巨星"},
            ]
        """
        pattern = re.compile(r'hotplaySvList = (.*?);')
        hot_showing = pattern.findall(response)[0]
        return eval(hot_showing)

    def json_parser(self, response):
        """
        Get the json information of the movie.
        response: str -> dict
        """
        pattern = re.compile(r'= (.*?);')
        content = pattern.findall(response)[0]
        return json.loads(content)

    def released_parser(self):
        pass

    def not_released_parser(self):
        pass

