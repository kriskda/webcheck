from apscheduler.scheduler import Scheduler


class WebCheckScheduler(object):

    def __init__(self):
        self.sched = None

    def main_job(self):
        print "Will check websites...TBD"
        print "Will send e-mails...TBD"
	
    def change_interval(self, interval_seconds):	
        self.sched.shutdown()
        self.start(interval_seconds)
        	
    def start(self, interval_seconds):
        self.sched = Scheduler()		
        self.sched.start()	
        self.sched.add_interval_job(self.main_job, seconds = interval_seconds)	

