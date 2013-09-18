import sqlite3
from flask import Flask, render_template, jsonify, g, request
#from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

app = Flask(__name__)

# App config
app.config.update(dict(
	DATABASE='webcheck.db',
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

sites = []

# Database service
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Route functions
@app.route('/add', methods = ['POST'])
def add_site():
    site = {
        'id': len(sites),
        'url': request.json['url'],
        'last_check': u'Not check yet',
        'status_code': u'Unknown'
    }
    
    sites.append(site)
    return jsonify( { 'site': site } ), 201

@app.route('/delete/<int:site_id>', methods = ['DELETE'])
def delete_site(site_id):
    site = filter(lambda t: t['id'] == site_id, sites)
    
    if len(site) == 0:
        abort(404)
        
    sites.remove(site[0])
    
    return jsonify( { 'sites_number': len(sites) } )

@app.route('/site/<int:site_id>')
def get_site(site_id):
    return render_template('site.html', site = sites[site_id])

@app.route('/')
def index():
    return render_template('index.html', sites = sites)

if __name__ == '__main__':
    app.run(debug = True)

