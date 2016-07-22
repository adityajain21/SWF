# serial_worker.py
import time
import boto.swf.layer2 as swf
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class MyBaseWorker(swf.ActivityWorker):

    domain = 'Django_WF_v1'
    version = '1.0'
    task_list = None

    def run(self):
        activity_task = self.poll()
        if 'activityId' in activity_task:
            # Get input.
            # Get the method for the requested activity.
            try:
                print activity_task.get('input')
                print 'working on activity from tasklist %s at %i' % (self.task_list, time.time())
                self.activity(activity_task.get('input'))

            except Exception as error:
                self.fail(reason=str(error))
                raise error

            return True

    def activity(self, activity_input):
        raise NotImplementedError

class WorkerA(MyBaseWorker):
    task_list = 'a_tasks'

    def activity(self, activity_input):
        print "ActivityAAAA!"

        fromaddr = "adityajuspay@gmail.com"
        toaddr = "aditya.jain@juspay.in"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "HELLO"
         
        body = "http://127.0.0.1:5000/taskB"
        msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "juspay123")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print ("Email sent.")
        self.complete(result="Now don't be givin him sambuca!")
        print "Completed task"

class WorkerB(MyBaseWorker):
    task_list = 'b_tasks'

    def activity(self, activity_input):
        print "ActivityBBBB!"
        
        fromaddr = "adityajuspay@gmail.com"
        toaddr = "aditya.jain@juspay.in"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "HELLO"
         
        body = "http://127.0.0.1:5000/taskC"
        msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "juspay123")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print ("Email 2 sent.")

        self.complete()

class WorkerC(MyBaseWorker):
    task_list = 'c_tasks'

    def activity(self, activity_input):
        print "ActivityCCCC!"
        self.complete()
