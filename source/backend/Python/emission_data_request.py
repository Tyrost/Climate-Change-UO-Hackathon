import requests
from pprint import pprint
from sys import argv
from json import dumps

def get_api_data(country_name:str):

    name = country_name.lower()

    api_url = f'https://restcountries.com/v3.1/name/{name}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        return data
    
    else:
        raise BufferError(f"There was an error obtaining the data. Error code {response.status_code}")
    
def fetch_data(country_name) -> dict:

    data:dict = get_api_data(country_name)[0]

    name = data.get('name', {}).get('common', 'N/A')
    capital = data.get('capital', ['N/A'])[0]
    population = data.get('population', 'N/A')
    region = data.get('region', 'N/A')
    currency_data = data.get('currencies', {})
    currency_name, currency_symbol = 'N/A', 'N/A'

    if currency_data:
        currency:dict = list(currency_data.values())[0]
        currency_name = currency.get('name', 'N/A')
        currency_symbol = currency.get('symbol', 'N/A')



    result = {
        "Country": name,
        "Capital": capital,
        "Population": population,
        "Region": region,
        "Currency": f"{currency_name} ({currency_symbol})"
    }
    
    return result

if __name__ == '__main__':

    country_name = argv[1]

    try:

        data = fetch_data(country_name)
        print(dumps(data, default=str))

    except Exception as e:
        print(f"Error occurred: {e}")