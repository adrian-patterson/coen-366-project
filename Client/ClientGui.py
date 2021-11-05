from flask import (Flask, render_template)

app = Flask("__main__", static_url_path='', static_folder='build', template_folder='build')


@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True)
