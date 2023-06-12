from termcolor import colored
from datetime import datetime
import os
from database import initialize_database
from exchange_rates import get_exchange_rate

previous_exchange_rates = {}
exchange_history = []

# Initialize the database
conn = initialize_database()

def store_exchange_rate(timestamp, from_currency, to_currency, exchange_rate):
    is_higher = None
    previous_rate = previous_exchange_rates.get((from_currency, to_currency))
    if previous_rate is not None:
        is_higher = exchange_rate > previous_rate

    insert_query = '''
        INSERT INTO exchange_history (timestamp, from_currency, to_currency, exchange_rate, is_higher)
        VALUES (%s, %s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(insert_query, (timestamp, from_currency,
                       to_currency, exchange_rate, is_higher))
    conn.commit()

def print_exchange_rate(from_currency, to_currency, exchange_rate):
    previous_rate = previous_exchange_rates.get((from_currency, to_currency))
    if previous_rate is None:
        print(
            f"The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {exchange_rate}")
    elif exchange_rate > previous_rate:
        print(colored(
            f"The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {exchange_rate}", 'green'))
    elif exchange_rate < previous_rate:
        print(colored(
            f"The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {exchange_rate}", 'red'))
    else:
        print(
            f"The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {exchange_rate}")

while True:
    command = input(
        "Enter a currency pair ('history' to view exchange history, 'quit' to exit): ")

    if command == "quit":
        break

    if command == "history":
        print("Exchange history:")
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT timestamp, from_currency, to_currency, exchange_rate, is_higher FROM exchange_history")
            rows = cursor.fetchall()
            for row in rows:
                timestamp, from_currency, to_currency, exchange_rate, is_higher = row
                formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                formatted_rate = colored(str(exchange_rate), 'green') if is_higher else colored(
                    str(exchange_rate), 'red')
                print(
                    f"{formatted_timestamp} {from_currency.upper()} {to_currency.upper()} {formatted_rate}")
        continue

    currencies = command.split()
    if len(currencies) != 2:
        print("Invalid input. Please enter two currencies separated by a space.")
        continue

    from_currency, to_currency = currencies

    exchange_rate = get_exchange_rate(from_currency, to_currency)
    if exchange_rate is not None:
        exchange_history.append((from_currency, to_currency))
        timestamp = datetime.now()
        store_exchange_rate(timestamp, from_currency,
                            to_currency, exchange_rate)
        print_exchange_rate(from_currency, to_currency, exchange_rate)
        previous_exchange_rates[(from_currency, to_currency)] = exchange_rate

conn.close()
