import datetime
import sys

import pandas as pd
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pytrading212 import *  # just for simplicity, not recommended, import only what you use
from pytrading212.trading212 import Period

if __name__ == "__main__":
    # email and password passed as program arguments,
    # change this with your credentials
    email = sys.argv[1]
    password = sys.argv[2]

    # Use your preferred web driver with your custom options
    # options = Options()
    # headless (optional)
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # or Firefox
    # driver = webdriver.Firefox()

    trading212 = Trading212(email, password, driver, mode=Mode.DEMO)

    market_order = trading212.execute_order(
        MarketOrder(instrument_code="AMZN_US_EQ", quantity=2)
    )

    limit_order = trading212.execute_order(
        LimitOrder(
            instrument_code="AMZN_US_EQ",
            quantity=2,
            limit_price=3000,
            time_validity=TimeValidity.DAY,
        )
    )

    stop_order = trading212.execute_order(
        StopOrder(
            instrument_code="AMZN_US_EQ",
            quantity=2,
            stop_price=4000,
            time_validity=TimeValidity.GOOD_TILL_CANCEL,
        )
    )

    stop_limit = trading212.execute_order(
        StopLimitOrder(
            instrument_code="AMZN_US_EQ",
            quantity=2,
            limit_price=3000,
            stop_price=4000,
            time_validity=TimeValidity.GOOD_TILL_CANCEL,
        )
    )

    quantity_order = trading212.execute_order(
        EquityOrder(
            "AMZN_US_EQ",
            quantity=2,
            limit_price=3000,
            stop_price=4000,
            time_validity=TimeValidity.GOOD_TILL_CANCEL,
        )
    )

    value_order = trading212.execute_value_order(ValueOrder("AMZN_US_EQ", value=100))

    # sell an equity that you own

    value_sell_order = trading212.execute_value_order(
        ValueOrder("AMZN_US_EQ", value=-100)
    )

    sell_limit = trading212.execute_order(
        LimitOrder(
            instrument_code="AMZN_US_EQ",
            quantity=-2,
            limit_price=4000,
            time_validity=TimeValidity.GOOD_TILL_CANCEL,
        )
    )

    print(quantity_order)
    print(value_order)

    funds = trading212.get_funds()
    print(funds)

    # Timezone is MANDATORY, please specify it, otherwise it won't work!
    older_than = datetime.datetime.now(tz=pytz.timezone("Europe/Rome"))
    newer_than = datetime.datetime(year=2022, month=5, day=9, tzinfo=pytz.timezone("Europe/Rome"))

    orders = trading212.get_orders(older_than=older_than, newer_than=newer_than)
    print('Orders', orders)
    for o in orders['data']:
        order_details = trading212.get_order_details(o['detailsPath'])

        # FX fee
        fx_fee = order_details['sections'][3]['rows'][0]['value']['context']['amount']

        # Total
        total = order_details['sections'][3]['rows'][1]['value']['context']['amount']

        # Exchange Rate
        exchange_rate = order_details['sections'][2]['rows'][4]['value']['context']['quantity']
        print(order_details)

        # changeRate
    # Orders with more details

    transactions = trading212.get_transactions(older_than=older_than, newer_than=newer_than)
    print('Transactions', transactions)

    dividends = trading212.get_dividends(older_than=older_than, newer_than=newer_than)
    print('Dividends', dividends)

    portfolio = trading212.get_portfolio_composition()
    performance = trading212.get_portfolio_performance(Period.LAST_DAY)

    print(portfolio)
    print(performance)

    # Pandas integration examples
    funds_df = pd.DataFrame(funds)
    print(funds_df)

    orders_df = pd.DataFrame(orders)
    print(orders_df)

    portfolio_df = pd.DataFrame(portfolio)
    performance_df = pd.DataFrame(performance)
