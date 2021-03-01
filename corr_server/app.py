import os
import sys
import flask
from flask_sqlalchemy import SQLAlchemy

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/rna3dhub-next?' \
                                 'unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'

db = SQLAlchemy(app)


def main():
    register_blueprints()
    app.run(debug=True)


def setup_db():
    pass


def register_blueprints():
    import views.correspondence_views
    import views.home_views
    import views.double_correspondence_views
    import views.interaction_views

    app.register_blueprint(views.correspondence_views.blueprint)
    app.register_blueprint(views.home_views.blueprint)
    app.register_blueprint(views.double_correspondence_views.blueprint)
    app.register_blueprint(views.interaction_views.blueprint)


if __name__ == '__main__':
    main()
