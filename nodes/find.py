import sys
import pymongo
from pymongo import Connection
from pymongo.errors import ConnectionFailure

global users

def ConnectDB():
	try:
        	c = Connection(host="localhost", port=27017)
    	except ConnectionFailure, e:
        	sys.stderr.write("Could not connect to MongoDB: %s" % e)
        	sys.exit(1)
    	
def InsertDB(doc):
	ConnectDB()
	c = Connection(host="localhost", port=27017)
	dbh = c["mydb"]
    	assert dbh.connection == c
	dbh.users.insert(doc, safe=True)
    	print "Successfully inserted document: %s" % doc

def FindDB(name,feature):
	mon_con = Connection('localhost', 27017)
	mon_db = mon_con.mydb
	try:
		query =mon_db.users.find({"name":name},{"_id":1,feature:1})
		#print ans1
		ans = mon_db.users.find({"name":name},{"_id":1,feature:1})[query.count()-1][feature]
		return ans
	except :
		return "Not Found"
	#print "Successfully searched"

def AddData(name,feature,data_fea):
	mon_con = Connection('localhost', 27017)
	mon_db = mon_con.mydb
	try:
		query =mon_db.users.find({"name":name},{"_id":1,feature:1})
		#print ans1
		ans = mon_db.users.find({"name":name},{"_id":1,feature:1})[query.count()-1]["_id"]
		print ans
		mon_db.users.update({"_id":ans},{"$set" : {feature:data_fea} })
		
	except :
		print "Not Found."
	#print "Successfully searched"

def RemoveDoc(name):
	mon_con = Connection('localhost', 27017)
	mon_db = mon_con.mydb
	try:
		query =mon_db.users.find({"name":name},{"_id":1})
		#print ans1
		ans = mon_db.users.find({"name":name},{"_id":1})[query.count()-1]["_id"]
		print ans
		mon_db.users.remove({"_id":ans})
	except :
		print "Not Found."
	#print "Successfully searched"	

def RemoveBlank():
	mon_con = Connection('localhost', 27017)
	mon_db = mon_con.mydb

	"""cols = mon_db.collection_names()
	for c in cols:
	    print c
	col = raw_input('Input a collection from the list above to show its field names: ')
	collection = mon_db[col].find()"""
	
	collection = mon_db.users.find()
	keylist = []
	for item in collection:
	    for key in item.keys():
		if key not in keylist:
		    keylist.append(key)
		if isinstance(item[key], dict):
		    for subkey in item[key]:
		        subkey_annotated = key + "." + subkey
		        if subkey_annotated not in keylist:
		            keylist.append(subkey_annotated)
		            if isinstance(item[key][subkey], dict):
		                for subkey2 in item[subkey]:
		                    subkey2_annotated = subkey_annotated + "." + subkey2
		                    if subkey2_annotated not in keylist:
		                        keylist.append(subkey2_annotated)
		if isinstance(item[key], list):
		    for l in item[key]:
		        if isinstance(l, dict):
		            for lkey in l.keys():
		                lkey_annotated = key + ".[" + lkey + "]"
		                if lkey_annotated not in keylist:
		                    keylist.append(lkey_annotated)
	keylist.sort()
	for key in keylist:
		keycnt = mon_db.users.find({key:{'$exists':1}}).count()
		print "%-5d\t%s" % (keycnt, key)
	print "--------------------------------"

	for key in keylist:
		mon_db.users.update( { key: "no" },{ '$unset': { key: ""}})
		keycnt = mon_db.users.find({key:{'$exists':1}}).count()
		print "%-5d\t%s" % (keycnt, key)


