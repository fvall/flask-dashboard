import numpy as np
import pandas as pd
import datetime
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


if __name__ == "__main__":
    print(fake_data())
