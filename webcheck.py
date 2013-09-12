from flask import Flask, render_template, jsonify

app = Flask(__name__)

sites = [
	{
		'id': 1,
		'url': 'http://icse.us.edu.pl',
		'last_check': '07.09.2013 @ 13:21',
		'status_code': 200
	},
	{
		'id': 2,
		'url': 'http://forszt.us.edu.pl',
		'last_check': '07.09.2013 @ 13:22',
		'status_code': 200
	},
	{
		'id': 3,
		'url': 'http://manager.us.edu.pl',
		'last_check': '07.09.2013 @ 13:23',
		'status_code': 404
	}	
]

@app.route('/sites', methods = ['GET'])
def get_tasks():
    return jsonify( { 'sites': sites } )

@app.route('/')
def index():
    return render_template('index.html', sites = sites)

if __name__ == '__main__':
    app.run(debug = True)

