# -*- coding: utf-8 -*-

"""Public controllers."""
from flask import Blueprint
from flask import render_template

from .models import Location

blueprint = Blueprint('public', __name__, static_url_path='/public/static', static_folder='../../static',
                      template_folder='../../templates')


@blueprint.route('/')
def index():
    return render_template('index.html', title='CRD Početna')


@blueprint.route('/locations')
def locations():
    locations_list = Location.get_all()
    return render_template('locations.html',
                           title='Lokacije',
                           locs=locations_list)


@blueprint.route('/map')
def map():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT latitude, longitude, name FROM locations;
    ''')
    response = cur.fetchall()
    return render_template('map.html',
                           title='Karta',
                           locs=response)


@blueprint.route('/statistics')
def statistics():
    return render_template('index.html', title='CRD Početna')


@blueprint.route('/compare_locations')
def compare_locations():
    return render_template('index.html', title='CRD Početna')


@blueprint.route('/documentation')
def documentation():
    return render_template('documentation.html',
                           title='Dokumentacija')


# Request browser not to cache responses (we need this for plots and other variable static content to work reliably)
@blueprint.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
