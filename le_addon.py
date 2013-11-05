#The MIT License (MIT)

#Copyright (c) 2013 Logentries

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


import json
#!/usr/bin/env python

import sys
import urllib
import urllib2
import json


CloudAMQP_TAG_NAMES=["AMQP Blocked Transfer-Limit", "AMQP Transfer-Ok", "AMQP Blocked Connections-Limit","AMQP Connections-Ok", "AMQP Disconnected Channels-Limit", "AMQP Disconnected Consumers-Limit"]
CloudAMQP_TAG_PATTERNS=["event=account.blocked AND reason=transfer.max","event=account.unblocked && reason=transfer.ok","event=account.blocked && reason=connections.max","event=account.unblocked && reason=connections.ok","event=account.disconnected && reason=channels.max","event=account.disconnected && reason=consumers.max"]
CloudAMQP_EVENT_COLOR=["ff0000", "009900","314046", "66ff66", "000099", "0099ff"]
""
ADEPT_TAG_NAME=["Scaling Event","AS 1-9 dynos", "AS 10-19 dynos","AS 20-29 dynos","AS 30-39 dynos","AS 40-49 dynos","AS >50 dynos"]
ADEPT_TAG_PATTERNS=["event=scale AND dyno_type=web","scaled_from>=0 AND scaled_to <10","scaled_from>=10 AND scaled_to <20","scaled_from>=20 AND scaled_to <30","scaled_from>=30 AND scaled_to <40","scaled_from>=40 AND scaled_to <50","scaled_to>50"]
ADEPT_EVENT_COLOR=["00B8FF","FFFF3D","FFB800","E68A00","996600","5C2E2E","E62E00"]

PG_TAG_NAME=["PG Duration > 50ms","PG Client Connect Reset", "PG Connection-Limit","PG Data Not Received","PG Role-Name","PG Permission Denied","PGError Operator","PGError: Table-name","PGError Column","PGError SSL SYSCALL","PGError prepared statement","PG Forking Not Supported"]
PG_TAG_PATTERN=["/duration:/","/could not receive data from client: Connection reset by peer/","/too many connections/","/could not receive data/","/not permitted to log in/","/PGError: ERROR:  permission denied for relation/","/PGError: ERROR: operator does not exist:/","/PGError: ERROR: relation/  AND /does not exist/","PGError: ERROR: column","/no connection to the server/ OR /SSL error: decryption failed/ OR /could not receive data from server: Connection timed out/","/prepared statement AND already exists/","/This database does not support forking/"]
PG_EVENT_COLOR=["E62E2E","FFFF00","E68A2E","E65C2E","2E8A8A","8A0000","005CE6","2E2E8A","005C8A","002E2E","2E8A2E","008AE6"]


PG_GRAPH="""{
	"widgets": [
		{
			"descriptor_id": "le.user-image",
			"options": {
				"title": "Heroku Postgres",
				"url": "https://raw.github.com/StephenHynes7/LogentriesHerokoImages/master/heroku-postgres-logo.png",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-timeline",
			"options": {
				"title": "Postgres Slow Queries",
				"tags_to_show": [
					"PG Duration > 50ms"
				],
				"style": [],
				"position": {
					"width": "4",
					"height": "1",
					"row": "2",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-bars-summary",
			"options": {
				"title": "Postgres Errors",
				"tags_to_show": [
					"PGError Column",
					"PGError Operator",
					"PGError prepared statement",
					"PGError SSL SYSCALL",
					"PGError: Table-name"
				],
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "2"
				}
			}
		},
		{
			"descriptor_id": "le.plot-timeline",
			"options": {
				"title": "Postgres",
				"tags_to_show": [
					"PG Client Connect Reset",
					"PG Connection-Limit",
					"PG Data Not Received",
					"PG Role-Name"
				],
				"style": [],
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "3"
				}
			}
		},
		{
			"descriptor_id": "le.plot-table",
			"options": {
				"title": "Postgres Events",
				"tags_to_show": [
					"PG Client Connect Reset",
					"PG Connection-Limit",
					"PG Data Not Received",
					"PG Duration > 50ms",
					"PG Forking Not Supported",
					"PG Permission Denied",
					"PG Role-Name",
					"PGError Column",
					"PGError Operator",
					"PGError prepared statement",
					"PGError SSL SYSCALL",
					"PGError: Table-name"
				],
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "4"
				}
			}
		}
	],
	"custom_widget_descriptors": {}
}
"""

AMQP_GRAPHS="""{
	"widgets": [
		{
			"descriptor_id": "le.user-image",
			"options": {
				"title": "CloudAMQP",
				"url": "https://raw.github.com/StephenHynes7/LogentriesHerokoImages/master/rabbit_256.png",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-bars-summary",
			"options": {
				"title": "CloudAMPQ Events",
				"tags_to_show": [
					"AMQP Blocked Connections-Limit",
					"AMQP Blocked Transfer-Limit",
					"AMQP Connections-Ok",
					"AMQP Disconnected Channels-Limit",
					"AMQP Disconnected Consumers-Limit",
					"AMQP Transfer-Ok"
				],
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "3"
				}
			}
		},
		{
			"descriptor_id": "le.plot-table",
			"options": {
				"title": "CloudAMPQ Events",
				"tags_to_show": [
					"AMQP Blocked Connections-Limit",
					"AMQP Blocked Transfer-Limit",
					"AMQP Connections-Ok",
					"AMQP Disconnected Channels-Limit",
					"AMQP Disconnected Consumers-Limit",
					"AMQP Transfer-Ok"
				],
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "2"
				}
			}
		},
		{
			"descriptor_id": "le.plot-timeline",
			"options": {
				"title": "CloudAMPQ Events Timeline",
				"tags_to_show": [
					"AMQP Blocked Connections-Limit",
					"AMQP Blocked Transfer-Limit",
					"AMQP Connections-Ok",
					"AMQP Disconnected Channels-Limit",
					"AMQP Disconnected Consumers-Limit",
					"AMQP Transfer-Ok"
				],
				"style": [],
				"position": {
					"width": "4",
					"height": "1",
					"row": "2",
					"column": "1"
				}
			}
		}
	],
	"custom_widget_descriptors": {}
}"""

ADEPT_GRAPH="""{
	"widgets": [
		{
			"descriptor_id": "le.user-image",
			"options": {
				"title": "Adept Scale",
				"url": "https://raw.github.com/StephenHynes7/LogentriesHerokoImages/master/logo-47ee48a6336cb2a990fe01500f5ddc93.png",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-timeline",
			"options": {
				"title": "Adept Scale Timeline",
				"tags_to_show": [
					"AS 1-9 dynos",
					"AS 10-19 dynos",
					"AS 20-29 dynos",
					"AS 30-39 dynos",
					"AS 40-49 dynos",
					"AS >50 dynos"
				],
				"style": [],
				"position": {
					"width": "4",
					"height": "1",
					"row": "3",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dyno 1-9",
				"event": "AS 1-9 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "2"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dyno 10-19",
				"event": "AS 10-19 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "3"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dyno 20-29",
				"event": "AS 20-29 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "1",
					"column": "4"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dyno 30-39",
				"event": "AS 30-39 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "2",
					"column": "1"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dyno 40-49",
				"event": "AS 30-39 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "2",
					"column": "2"
				}
			}
		},
		{
			"descriptor_id": "le.plot-radial-gauge",
			"options": {
				"title": "Scaling Dynos >50",
				"event": "AS 30-39 dynos",
				"high_threshold": "100",
				"high_threshold_rate": "Per Day",
				"position": {
					"width": "1",
					"height": "1",
					"row": "2",
					"column": "3"
				}
			}
		},
		{
			"descriptor_id": "le.plot-table",
			"options": {
				"title": "Adept Scale Events",
				"tags_to_show": [
					"AS 1-9 dynos",
					"AS 10-19 dynos",
					"AS 20-29 dynos",
					"AS 30-39 dynos",
					"AS 40-49 dynos",
					"AS >50 dynos"
				],
				"position": {
					"width": "1",
					"height": "1",
					"row": "2",
					"column": "4"
				}
			}
		}
	],
	"custom_widget_descriptors": {}
}"""



USER_KEY=""
TAG_ID=[]
# Standard boilerplate to call the main() function to begin
# the program.



def createEvent(LOG_KEY,TAG_NAMES,TAG_PATTERNS,EVENT_COLOR):
	print "Checking for existing Events."
	if accountEventsAlreadyExist(LOG_KEY,TAG_NAMES,TAG_PATTERNS):
		print "Events already exist."
	else:
		for idx, val in enumerate(TAG_NAMES):
			params = urllib.urlencode ({
				'request':'set_tag',
				'user_key':USER_KEY,
				'tag_id': '',
				'name': TAG_NAMES[idx],
				'title': TAG_NAMES[idx],
				'desc':TAG_NAMES[idx],
				'color':EVENT_COLOR[idx],
				'vtype':'bar'

			})
			response = urllib2.urlopen("http://api.logentries.com", params)
			response_dict = json.loads(response.read())
			TAG_ID.append(response_dict['tag_id'])
	createTag(LOG_KEY,TAG_NAMES,TAG_PATTERNS)


def accountEventsAlreadyExist(LOG_KEY,TAG_NAMES,TAG_PATTERNS):
	params = urllib.urlencode ({
		'request':'list_tags',
		'user_key':USER_KEY,
		'id':'init_menu'
	})
	response = urllib2.urlopen("http://api.logentries.com", params)
	response_dict = json.loads(response.read())
	for id in TAG_NAMES:
		for item in response_dict['tags']:
			if item['title'] == id:
				TAG_ID.append(item['id'])
	if len(TAG_ID) == 0:
		return False
	else:
		return True

def createTag(LOG_KEY,TAG_NAMES,TAG_PATTERNS):
	for idx, val in enumerate(TAG_ID):
		if idx < len(TAG_NAMES):
			params = urllib.urlencode({
				'request':'set_tagfilter',
				'user_key':USER_KEY,
				'log_key': LOG_KEY,
				'name': TAG_NAMES[idx],
				'pattern': TAG_PATTERNS[idx],
				'tags': TAG_ID[idx],
				'tagfilter_key':''

			})
			response = urllib.urlopen("http://api.logentries.com", params)
			print "Creating tag " + TAG_NAMES[idx]

def createGraph(LOG_KEY,graph):
		print "Creating Report."
		data=urllib.quote(graph)
		params ="request=set_dashboard&log_key="+LOG_KEY+"&dashboard="+data
		req= urllib2.Request("https://api.logentries.com",params)
		response=urllib2.urlopen(req)
		the_page = response.read()

def createAdeptData(LOG_KEY):
	createEvent(LOG_KEY,ADEPT_TAG_NAME,ADEPT_TAG_PATTERNS,ADEPT_EVENT_COLOR)
	createGraph(LOG_KEY,ADEPT_GRAPH)

def createCloudAMQPData(LOG_KEY):
	createEvent(LOG_KEY,CloudAMQP_TAG_NAMES,CloudAMQP_TAG_PATTERNS,CloudAMQP_EVENT_COLOR)
	createGraph(LOG_KEY,AMQP_GRAPHS)

def createPGData(LOG_KEY):
	createEvent(LOG_KEY,PG_TAG_NAME,PG_TAG_PATTERN,PG_EVENT_COLOR)
	createGraph(LOG_KEY,PG_GRAPH)

def query_yes_no_quit(question, default="yes"):
	"""Ask a yes/no/quit question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no", "quit" or None (meaning
		an answer is required of the user).

	The "answer" return value is one of "yes", "no" or "quit".
	"""
	valid = {"yes":"yes",   "y":"yes",    "ye":"yes",
			 "no":"no",     "n":"no",}
	if default == None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while 1:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return default
		elif choice in valid.keys():
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes', 'no' or 'quit'.\n")

def createPartnerData(partner,LOG_KEY):
	if(partner == "Adept Scale"):
		createAdeptData(LOG_KEY)
	elif(partner == "CloudAMQP"):
		createCloudAMQPData(LOG_KEY)
	elif(partner == "Heroku Postgres"):
		createPGData(LOG_KEY)

def getLogs(partner):
	params = {
		'user_key': USER_KEY,
		'request': 'get_user',
		'load_hosts': 'true',
		'load_logs': 'true',
	}
	data=urllib.urlencode(params)
	req= urllib2.Request("https://api.logentries.com",data)
	response=urllib2.urlopen(req)
	the_page = response.read()
	test=json.loads(the_page)
	host = test["hosts"][0]["logs"]
	for log in host:
		user_answer =query_yes_no_quit("Do we wish to add default "+partner+" tags and graphs for log " +log["name"] +"?")
		print user_answer
		if(user_answer=="yes"):
			print "Creating default data for log " + log["name"]
			createPartnerData(partner,log["key"])
		else:
			print "Not creating default data for log " + log["name"]

	print "Finished createing default "+partner+" data. Please view your Logs and Graphs page to see changes."

if __name__ == '__main__':
	# Map command line arguments to function arguments.
	USER_KEY=sys.argv[1]
	print "DISCLAIMER: The following script will REPLACE any existing Graph that you have on log that you choose."
	print "If you are unsure as to what to do contact support@logentries.com."
	print ""
	print "Logentries provides default Tags and Reports for the following partner Heroku Addons"
	print "(1): Heroku Postgres"
	print "(2): Adept Scale"
	print "(3): CloudAMQP"
	choice = raw_input("Please choose 1, 2 or 3.\n")
	print ""
	while choice not in ["1", "2", "3"]:
		choice = raw_input("choose 1, 2 or 3.")

	reaction = {"1": "Heroku Postgres", "2":  "Adept Scale", "3": "CloudAMQP"}
	getLogs(reaction[choice])
