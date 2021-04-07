import re
import numpy as np
import pandas as pd
import datetime
import yfinance as yf

from .util import css_variables


def fake_data():

    """
    Generate fake data for testing
    """

    symbols = ["ABC", "DEF", "GHI", "JKL", "MNO"]
    prices = pd.DataFrame(
        np.random.rand(10, len(symbols)) * 100,
        columns = symbols
    )

    today = datetime.date.today()
    prices.index = pd.DatetimeIndex(
        pd.date_range(today, periods = prices.shape[0], freq = "1D")
    )

    return prices


def get_price_data(symbols, start_date = None, end_date = None):

    if end_date is None:
        end_date = datetime.date.today()
    
    if start_date is None:
        start_date = end_date

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    start_date += datetime.timedelta(days = 1) # YFinance API auto subtracts 1 day
    end_date += datetime.timedelta(days = 1)   # we want end_date to be inclusive

    data = yf.download(
        symbols,
        start = start_date,
        end = end_date,
        actions = True,
        group_by = 'ticker'
    )

    # - Format data

    data = (
        data
        .melt(var_name = ['symbol', 'field'], ignore_index = False)
        .reset_index()
        .pivot(['Date', 'symbol'], 'field', 'value')
        .reset_index()
        .pipe(
            lambda df: df.rename(
                columns = {col : col.lower().replace(" ", "_") for col in df.columns}
            )
        )
        .sort_values('date', ascending = False)
    )

    return data


def calc_return(price_data, index = 1):
    
    if index < 1:
        raise ValueError("index must be greater than zero")

    def ret(pr, index):

        last  = pr['date'].iloc[0]
        first = pr['date'].iloc[min(index, len(pr))]
        df = pr.loc[pr['date'].isin([last, first])]
        
        return (
            df.loc[:, ['date', 'symbol', 'adj_close']]
            .pivot('symbol', 'date', 'adj_close')
            .assign(
                ret  = lambda df: df[last] / df[first] - 1,
                date = last
            )
        )

    df = pd.concat(
        [ret(tbl, index) for _, tbl in price_data.groupby('symbol')],
        sort = False
    )

    return df[['date', 'ret']]


def format_data_frame(df):

    css = css_variables()

    def hover(hover_color = "#ffff99", text_color = "black"):
        return [
            dict(
                selector = "tr:hover",
                props = [
                    ("background-color", "%s" % hover_color),
                    ("color", text_color)
                ]
            ),
            dict(
                selector = "tr:hover > td",
                props = [
                    ("background-color", "%s" % hover_color),
                    ("color", text_color)
                ]
            ),
            dict(
                selector = "tr:hover > th",
                props = [
                    ("background-color", "%s" % hover_color),
                    ("color", text_color)
                ]
            ),
        ]

    styles = [
        dict(
            selector = "th",
            props = [
                ("padding", "2px 5px"),
                ("text-align", "center"),
                ("border-top", "solid 1px"),
                ("border-bottom", "solid 1px"),
                ("color", "white"),
            ]
        ),
        dict(
            selector = "td",
            props = [
                ("padding", "2px 5px"),
                ("text-align", "center"),
                ("font-size", "0.8rem"),
            ]
        ),
        dict(
            selector = "tr:nth-child(even)",
            props = [
                ("background-color", css['color_3'])
            ]
        ),
        *hover(css["color_2"], css['color_1'])
    ]

    return (
        df
        .style
        .set_table_styles(styles)
        .hide_index()
    )


def parse_date(date):

    if isinstance(date, datetime.datetime):
        return date.date()

    if isinstance(date, datetime.date):
        return date

    if isinstance(date, str):
        date = re.sub(r'[-_/]', '', date)
        date = datetime.datetime.strptime(date, "%Y%m%d")
        return date.date()

    raise TypeError(f"Cannot parse_date for type {type(date).__name__}")


if __name__ == "__main__":
    print(fake_data())
