import requests
from mtime.head import Head
from mtime.mtime_exception import RequestFailed


class Downloader:
    def __init__(self, request_headers):
        self.headers = Head.format(request_headers)

    def html_download(self, url):
        """
        Download the html corresponded to the url.
        """
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            raise RequestFailed

    def json_download(self, movie_id):
        """
        Download the json corresponded to the movie.
        """
        url = ('http://service.library.mtime.com/Movie.api?'
               'Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&'
               'Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&'
               'Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F{}%2F&'
               'Ajax_CallBackArgument0={}').format(movie_id, movie_id)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            raise RequestFailed
