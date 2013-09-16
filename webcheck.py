import sqlite3
from flask import Flask, render_template, jsonify, g, request
#from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

app = Flask(__name__)

app.config.update(dict(
	DATABASE='webcheck.db',
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

sites = []

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/sites', methods = ['GET'])
def get_tasks():
    return jsonify( { 'sites': sites } )

@app.route('/add', methods = ['POST'])
def add_site():
    site = {
        'id': len(sites) +1,
        'url': request.json['url'],
        'last_check': u'Not check yet',
        'status_code': u'Unknown'
    }
    
    sites.append(site)
    return jsonify( { 'sites': site } ), 201

@app.route('/')
def index():
    return render_template('index.html', sites = sites)

if __name__ == '__main__':
    app.run(debug = True)

