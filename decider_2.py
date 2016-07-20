from flask import Flask, jsonify,render_template, request,json
import boto.swf.layer2 as SerialWorkflow
from serial_decider import SerialDecider
import boto.swf.layer2 as swf

app = Flask(__name__)

serial_decider = SerialDecider()

@app.route('/tasks',methods=['POST','GET'])
def execute():
	if(request.json['ph_no']=='1'):
		print "Starting decider 2."
		while serial_decider.run(): pass
		print "Decider 2 started!"
		
		return "Success"


if __name__ == '__main__':
	app.run(debug=True, port=5001)