
# Date night app using multiple APIs

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# Basic app setup
app = Flask(__name__)
app.secret_key = "Saturday Night"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/date-type', methods=['POST'])
def decide_date_type():
    """Intake form with user choice and route to next step."""

    date_type = request.form['date-type']

    if date_type == 'out':
        session['date-type'] = 'out'
        flash('Let\'s go out')
        return redirect('/go-out')
    else:
        session['date-type'] = 'in'
        flash('Let\'s stay in')
        return redirect('/stay-in')


@app.route('/go-out')
def going_out():
    """Homepage."""

    return render_template("date-location.html")


@app.route('/stay-in')
def staying_in():
    """Homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":
    app.debug = True
    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
