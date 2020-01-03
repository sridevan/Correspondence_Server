import flask
from flask import render_template

# from pypi_org.infrastructure.view_modifiers import response

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

@blueprint.route('/')
def index():
    return render_template("index.html")


