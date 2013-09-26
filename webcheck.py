from flask import Flask, render_template, jsonify, request
from contextlib import closing
from scheduler import WebCheckScheduler
from dbservice import DBService

app = Flask(__name__)

# App config
app.config.update(dict(
	DATABASE='webcheck.db',
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
))

dbservice = DBService()
dbservice.app = app
web_check_scheduler = WebCheckScheduler(dbservice)

# Route functions
@app.route('/add', methods = ['POST'])
def add_site():
    dbservice.execute_db('INSERT INTO sites (url, last_check, status_code) VALUES (?, ?, ?)', [request.json['url'], u'Not checked yet', u'Unknown'])

    return jsonify( dbservice.query_db('SELECT * FROM sites ORDER BY id DESC LIMIT 1')[0] ), 201

@app.route('/delete/<int:site_id>', methods = ['DELETE'])
def delete_site(site_id):
    dbservice.execute_db('DELETE FROM sites WHERE id == ?', [site_id])
 
    return jsonify( { 'sites_number': len(dbservice.query_db('SELECT * FROM sites')) } )

@app.route('/site/<int:site_id>')
def get_site(site_id):
    return render_template('site.html', site = dbservice.query_db('SELECT * FROM sites WHERE id == ?', [site_id])[0] )

@app.route('/')
def index():
    return render_template('index.html', sites = dbservice.query_db('SELECT * FROM sites'))

if __name__ == '__main__':
    web_check_scheduler.start(60)    
    app.run(use_reloader=False)


