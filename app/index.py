import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from flask import current_app, render_template
from .data import (
    calc_return,
    format_data_frame,
    get_price_data
)

from .util import css_variables
from io import BytesIO

app = current_app
matplotlib.use('Agg')


def plot(prices):

    prices = (
        prices
        .sort_index()
        .apply(np.log)
        .diff()
        .fillna(0.0)
        .cumsum()
        .apply(np.exp)
        .apply(lambda x: x - 1)
    )

    return prices.plot()


def export_svg(chart):
    output = BytesIO()
    chart.get_figure().savefig(output, format = "svg")
    return output


def customize_chart(chart):
    fig = plt.gcf()
    css = css_variables()
    
    fig.set_facecolor(css['color_1'])
    chart.set_xlabel(None)
    chart.set_ylabel("Cumulative return", color = css['color_2'])
    chart.tick_params(color = css['color_2'], labelcolor = css['color_2'], which = "both")
    chart.set_facecolor(css['color_1'])
    for s in chart.spines:
        chart.spines[s].set_color(css['color_2'])

    return chart


@app.route("/")
def home():

    symbols = ['SPY', 'EZU', 'IWM', 'EWJ', 'EEM']
    end = datetime.date.today()
    start = end - datetime.timedelta(days = 30 * 3)

    df = get_price_data(symbols, start_date = start, end_date = end)
    _plot = (
        df
        .loc[:, ['date', 'symbol', 'adj_close']]
        .pivot('date', 'symbol', 'adj_close')
        .pipe(plot)
    )
    _plot = customize_chart(_plot)
    
    try:
        chart = export_svg(_plot)
    finally:
        plt.close()

    ret_d01 = calc_return(df, index = 1)
    ret_d21 = calc_return(df, index = 21)
    prices  = (
        df[['symbol', 'date', 'adj_close']]
        .rename(
            columns = {'adj_close' : 'price'}
        )
        .merge(ret_d01.reset_index(), how = 'inner', on = ['date', 'symbol'])
        .rename(columns = {'ret' : 'daily_return'})
        .merge(ret_d21.reset_index(), how = 'inner', on = ['date', 'symbol'])
        .rename(columns = {'ret' : 'monthly_return'})
    )

    # - styling

    return_cols = ['daily_return', 'monthly_return']
    def ret_color(x):
        color = 'tomato' if x < 0 else 'lightgreen'
        return 'color: %s' % color

    prices = (
        prices
        .sort_values('monthly_return', ascending = False)
        .assign(date = lambda df: df['date'].dt.strftime("%Y-%m-%d"))
        .pipe(format_data_frame)
        .format("{:,.2f}", subset = ['price'])
        .applymap(ret_color, subset = return_cols)
        .format("{:+,.2%}", subset = return_cols)
    )

    return render_template(
        "index.html",
        prices = prices.render(),
        chart = chart.getvalue().decode('utf8')
    )
