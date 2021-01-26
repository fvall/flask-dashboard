import pandas as pd
import datetime
from random import random


def fake_data():

    """
    Generate fake data for testing
    """

    symbols = ["ABC", "DEF", "GHI", "JKL", "MNO"]
    prices = pd.DataFrame({
        s : [random() * 100 for i in range(10)] for s in symbols
    })

    today = datetime.date.today()
    prices.index = pd.DatetimeIndex(
        pd.date_range(today, periods = prices.shape[0], freq = "1D")
    )

    return prices


if __name__ == "__main__":
    print(fake_data())
