# -*- coding: utf-8 -*-

from flask import Flask, request
import json
from bson import json_util
from bson.objectid import ObjectId
import pymongo
import re

app = Flask(__name__)

mongoClient = pymongo.MongoClient('192.168.1.102', 27017)
db = mongoClient['roll']

def toJson(data):
    return json.dumps(data, default=json_util.default)

@app.route('/news', methods=['GET'])
def findNews():
    if request.method == 'GET':
        try:
            limit = int(request.args.get('limit', 10)) 
            offset = int(request.args.get('offset', 0)) 
            results = db['news'].find().skip(offset).limit(limit)
            json_results= []
            for result in results:
                json_results.append(result)
            return toJson(json_results)
        except ValueError:
            abort(404)      # 返回 404

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        try:
            #print request.args.get('kw', "")
            kw=request.args.get('kw', "")
            print "kw",kw
            if kw == "" :
                print "No kw"
                return findNews()
                
            limit = int(request.args.get('limit', 10)) 
            offset = int(request.args.get('offset', 0)) 
            
            regex = re.compile(kw, re.IGNORECASE)
            results = db['news'].find({"title":regex}).skip(offset).limit(limit)
            print results
            json_results= []
            for result in results:
                #print result
                json_results.append(result)
            return toJson(json_results)
            #return "test"
            
        except ValueError:
            print "Error",ValueError
            #abort(404)      # 返回 404
        return "NULL"

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True,host="0.0.0.0")