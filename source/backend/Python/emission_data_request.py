from requests import request

def get_api_data(api_url, API_KEY = ''):

    #https://search.worldbank.org/api/v3/wds?format=json

    api = f'{api_url}?'

    return