import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from flask import current_app, render_template
from .data import fake_data, format_data_frame
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

    df = fake_data()
    _plot = plot(fake_data())
    _plot = customize_chart(_plot)
    
    try:
        chart = export_svg(_plot)
    finally:
        plt.close()

    return render_template(
        "index.html",
        prices = format_data_frame(df).render(),
        chart = chart.getvalue().decode('utf8')
    )
