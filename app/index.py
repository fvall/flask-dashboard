from flask import current_app, render_template

app = current_app


@app.route("/")
def home():
    return render_template("index.html")
