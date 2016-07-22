#!flask/bin/python
from flask import Flask, jsonify,render_template, request,json
import boto.swf.layer2 as SerialWorkflow
from serial_decider import SerialDecider
from serial_worker import WorkerA,WorkerB,WorkerC

workerA = WorkerA()
workerB = WorkerB()
workerC = WorkerC()


app = Flask(__name__)

@app.route('/taskA', methods=['GET','POST'])
def taskA():
    print "starting task A from app."
    workerA.run()
    print "Task A complete!"
    return "Task A"

@app.route('/taskB',methods=['POST','GET'])
def taskB():
    if(request.method == 'GET'):
        print "starting task B from app."
        workerB.run()
        print "Task B complete!"
    return "Task B"

@app.route('/taskC',methods=['GET','POST'])
def taskC():
    print "starting task C from app."
    workerC.run()
    print "Task C complete!"
    return "Task C"


if __name__ == '__main__':
    app.run(debug=True)