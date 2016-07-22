from flask import Flask, jsonify,render_template, request,json
import boto.swf.layer2 as SerialWorkflow
from serial_decider import SerialDecider
import boto.swf.layer2 as swf

app = Flask(__name__)

serial_decider = SerialDecider()

@app.route('/tasks',methods=['POST','GET'])
def execute():
	#print "Inside IF!"
	#print "Starting execution"
	execution = swf.WorkflowType(name='SerialWorkflow', domain='Django_WF_v1', version='1.0', task_list='default_tasks', input='adityaadityaaditya').start()
	#print "execution started!"
	#while serial_decider.run(): pass
	print(execution.history())
	return "Success"


if __name__ == '__main__':
	app.run(debug=True, port=8000)