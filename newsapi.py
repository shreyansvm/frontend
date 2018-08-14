import requests

API_KEY = "XXXXXXXXXXX"

class newsApi(object):

    def __init__(self,
                 news_type = "top-headlines",
                 keyword = None,
                 domains = None,
                 **kwargs):
        print('------ Hello from NewsApi ------\n')
        self.api_key = API_KEY
        self.base_url = "https://newsapi.org/v2/"

        self.language = "en"
        self.country = "us"
        self.api = "apiKey=" + self.api_key

        self.news_sources_url = self.base_url + "sources?" + self.api
        self.available_sources = self.available_news_source()
        self.news_source = None
        self.source = ""
        if self.news_source is not None:
            self.source = "sources=" + self.news_source + "&"

        self.domains = domains

        # dict of {'news_source': 'category'}
        # Example : {'abc-news': 'general', 'bbc-sport': 'sports'}
        self.available_news_categories = self.available_news_categories()

        # news_type can be : top-headlines or everything
        self.news_type = news_type
        self.keyword = keyword
        self.query_type = ""
        if self.news_type is "everything":
            if self.keyword is not None:
                self.query_type = "q=" + self.keyword + "&"
                if domains is not None:
                    self.full_url = self.base_url + \
                                    self.news_type + "?" + \
                                    self.query_type + \
                                    "domain=" + self.domains + "&" + \
                                    self.api
                else:
                    self.full_url = self.base_url + \
                                    self.news_type + "?" + \
                                    self.query_type + \
                                    "language=" + self.language + "&" + \
                                    self.api
        else:
            # assuming self.news_type = "top-headlines"
            self.full_url = self.base_url + \
                            "top-headlines?" + \
                            self.source + \
                            "country=" + self.country + "&" + \
                            self.api

        self.__dict__.update(kwargs)

    def documentation(self):
        print('----- Refer -----')
        print('https://newsapi.org/docs/get-started')
        print('https://newsapi.org/docs')
        print('\n')

    def available_news_source(self):
        # refer : https://newsapi.org/docs/endpoints/sources
        available_types = []
        response = requests.get(self.news_sources_url)
        sources = response.json()
        if sources["status"] == "ok":
            for each_source in sources["sources"]:
                available_types.append(each_source["id"])
        return available_types

    def print_available_news_source(self):
        print('self.available_sources : ', self.available_sources)

    def available_news_categories(self):
        available_categories = {}
        response = requests.get(self.news_sources_url)
        sources = response.json()
        if sources["status"] == "ok":
            for each_source in sources["sources"]:
                available_categories[each_source["id"]] = each_source["category"]
        return available_categories

    def print_available_news_categories(self):
        print('available_news_categories : ', self.available_news_categories)

    def set_base_url(self, url):
        self.base_url = url

    def set_news_type(self, news_type):
        self.news_type = news_type

    def set_country(self, country):
        self.country = country

    def set_news_type(self, news_type):
        # TODO
        pass

    def set_news_source(self, news_source):
        # TODO
        pass

    def reconstruct_full_url(self):
        self.full_url = self.base_url + \
                        self.news_type + "?" + \
                        "country=" + self.country + "&" + \
                        self.api
        print('re-constructed newsApi full_url : ', self.full_url)

    def get_response(self):
        print('newsApi full_url : ', self.full_url)
        response = requests.get(self.full_url)
        json_resp = response.json()
        if json_resp["status"] == "ok":
            print('newsAPI query successful')
            return json_resp
        else:
            print('newsAPI query NOT SUCCESSFUL')

    def print_user_text(self, value):
        print('You selected : ', value)

