
from polygon import RESTClient
from datetime import date
from os import environ
from dotenv import load_dotenv

class ApiAccess:
    def __init__(self):
        load_dotenv()
        key = environ.get('POLY_API')
        self.client = RESTClient(api_key =key)
    def get_5mn_data(self,indice,m):
        t = indice
        aggs = []
        for a in self.client.list_aggs(ticker= t, multiplier=m, timespan="minute", from_="2010-01-01", to=date.today(), limit=50000):
            aggs.append(a)
        return aggs
        