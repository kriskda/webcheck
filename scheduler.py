import logging
logging.basicConfig()
from apscheduler.scheduler import Scheduler
from model import URLCheck


class WebCheckScheduler(object):

    def __init__(self, dbservice):
        self.dbservice = dbservice		
        self.sched = None
        self.url_check = URLCheck()

    def main_job(self):		  
        websites = self.dbservice.query_db('SELECT * FROM sites')
        print "\n\n"
           
        for	website in websites:	
            url = website['url']    
            status = self.url_check.get_url_status(url)		
            print "Checked " + url + " status: " + status
            print "Will send e-mails...TBD\n"
                  	
    def change_interval(self, interval_seconds):	
        self.sched.shutdown()
        self.start(interval_seconds)
        	
    def start(self, interval_seconds):
        self.sched = Scheduler()		
        self.sched.start()	
        self.sched.add_interval_job(self.main_job, seconds = interval_seconds)	

