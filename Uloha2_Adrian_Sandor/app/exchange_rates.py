import requests
from config import EXCHANGE_RATE_API_KEY

def get_exchange_rate(from_currency, to_currency):
    from_currency_upper = from_currency.upper()
    to_currency_upper = to_currency.upper()
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
    response = requests.get(url, params={
        "from": from_currency_upper,
        "to": to_currency_upper,
        "amount": 1
    })
    data = response.json()

    if "error" in data:
        print(f"Error: {data['error']}")
        return

    try:
        exchange_rate = data["conversion_rates"][to_currency_upper]
        return round(exchange_rate, 2)
    except KeyError:
        print(
            f"Error: Invalid currency pair ({from_currency_upper} to {to_currency_upper})")
        return
