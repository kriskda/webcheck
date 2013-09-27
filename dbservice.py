import sqlite3
from flask import g

class DBService(object):
    app = None
	
    def connect_db(self):
        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    def init_db(self):
        with closing(self.connect_db()) as db:
            with self.app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.connect_db()
        return db
    
#    @app.teardown_appcontext
#    def close_connection(exception):
#        db = getattr(g, '_database', None)
#        if db is not None:
#            db.close()    

    def query_db(self, query, args=(), one=False):
        with self.app.app_context():
            cur = self.get_db().execute(query, args)
            rv = cur.fetchall()
            cur.close()    
            return (rv[0] if rv else None) if one else rv
    
    def execute_db(self, query, values):
	    with self.app.app_context():
	        db = self.get_db()
	        db.execute(query, values)
	        db.commit()
