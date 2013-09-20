import sqlite3
from flask import Flask, render_template, jsonify, g, request
from contextlib import closing
from scheduler import WebCheckScheduler

app = Flask(__name__)
web_check_scheduler = WebCheckScheduler()

# App config
app.config.update(dict(
	DATABASE='webcheck.db',
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
))

# Database service
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()    

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()    
    return (rv[0] if rv else None) if one else rv
    
def execute_db(query, values):
	db = get_db()
	db.execute(query, values)
	db.commit()

# Route functions
@app.route('/add', methods = ['POST'])
def add_site():
    execute_db('INSERT INTO sites (url, last_check, status_code) VALUES (?, ?, ?)', [request.json['url'], u'Not checked yet', u'Unknown'])

    return jsonify( query_db('SELECT * FROM sites ORDER BY id DESC LIMIT 1')[0] ), 201

@app.route('/delete/<int:site_id>', methods = ['DELETE'])
def delete_site(site_id):
    execute_db('DELETE FROM sites WHERE id == ?', [site_id])
 
    return jsonify( { 'sites_number': len(query_db('SELECT * FROM sites')) } )

@app.route('/site/<int:site_id>')
def get_site(site_id):
    return render_template('site.html', site = query_db('SELECT * FROM sites WHERE id == ?', [site_id])[0] )

@app.route('/')
def index():
    return render_template('index.html', sites = query_db('SELECT * FROM sites'))

if __name__ == '__main__':
    web_check_scheduler.start(10)
    app.run(use_reloader=False)



