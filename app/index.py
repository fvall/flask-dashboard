import matplotlib
import matplotlib.pyplot as plt
from flask import current_app, render_template
from .data import fake_data
from io import BytesIO

app = current_app
matplotlib.use('Agg')


@app.route("/")
def home():

    df = fake_data()
    plot = df.plot()
    chart = BytesIO()

    try:
        plot.get_figure().savefig(chart, format = "svg")
    finally:
        plt.close()

    return render_template(
        "index.html",
        prices = df.to_html(),
        chart = chart.getvalue().decode('utf8')
    )
