import logging
logging.basicConfig()

from apscheduler.scheduler import Scheduler
from model import URLCheck
from datetime import datetime


class WebCheckScheduler(object):

    def __init__(self, dbservice):
        self.dbservice = dbservice		
        self.sched = None
        self.url_check = URLCheck()

    def main_job(self):		  
        websites = self.dbservice.query_db('SELECT * FROM sites')
  
        if len(websites) != 0:
            for	website in websites:	            
                url = website['url']    
                webid = website['id']
                status_code = self.url_check.get_url_status(url)	
                last_check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')            
                
                self.dbservice.execute_db('UPDATE sites SET last_check=?, status_code=? WHERE id=?', [last_check, status_code, webid])
                            
                print "Will send e-mails...TBD\n"
            
            self.dbservice.execute_db('UPDATE dbutil SET db_code=? WHERE id=?', [1, 1])
                  	
    def change_interval(self, interval_seconds):	
        self.sched.shutdown()
        self.start(interval_seconds)
        	
    def start(self, interval_seconds):
        self.sched = Scheduler()		
        self.sched.start()	
        self.sched.add_interval_job(self.main_job, seconds = interval_seconds)	
        
