# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import mongo_operations as m
from flask import Flask, render_template, request, Response, jsonify
import json
import logging
import clustering as clus

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
logger = logging.getLogger()
features = clus.Features() 

# def main():
#     app = Flask(__name__)
#     logger = logging.getLogger()
#     features = clus.Features() 

@app.route('/getQueries')
def getJSONDumps():
    #SampleURL#
    #http://10.1.1.1:5000/getJSON?queryNum=1&password=pw1
    qNum = int(request.args.get('queryNum'))
    print("qNum", qNum)
    # password = request.args.get('password')
    mongo = m.MongoDB("Queries")
    data = mongo.read_one_query({'queryNum': qNum})
    logger.warning(data)
    logging.warning("HI")
    logging.warning(data)
    print(data)
    # console.log(data)
        # data = make_summary()
    # response = app.response_class(
    #     response=json.dumps(data),
    #     status=200,
    #     mimetype='application/json'
    # )
    # return response
    extract_data = {}
    for key in data:
    	if key == '_id':
    		continue
    	else:
    		extract_data[key] = data[key]
    return jsonify(extract_data)

@app.route('/viz')
def vizualise():
    return render_template('viz.html')

@app.route('/getClusters')
def callCluster():
    #SampleURL#
    #http://10.1.1.1:5000/getClusters?algo=1&password=pw1
    # features = clus.Features() 
    kwargs=dict(name=None, n_clusters=None, dist=None, link=None, 
    q_type=None, emb_type=None, printing=None)
    if 'algo' in request.args:
        algo = request.args.get('algo')
        kwargs['name']=algo
        print("algo", algo)
    if 'n_clusters' in request.args:
        n_clusters = int(request.args.get('n_clusters'))
        kwargs['n_clusters']=n_clusters
        print("n_clusters", n_clusters)
    if 'dist' in request.args:
        dist = float(request.args.get('dist'))
        kwargs['dist']=dist
        print("dist", dist)
    if 'q_type' in request.args:
        q_type = request.args.get('q_type')
        kwargs['q_type']=q_type
        print("q_type", q_type)
    if 'emb_type' in request.args:
        emb_type = request.args.get('emb_type')
        kwargs['emb_type']=emb_type
        print("emb_type", emb_type)
    if 'printing' in request.args:
        printing = request.args.get('printing')
        kwargs['printing']=printing
        print("printing", printing)
    a = features.cluster(**{k: v for k, v in kwargs.items() if v is not None})
    # print("Type!", type(a))
    obj = json.loads(a)
    # print("Type after parsing!", type(obj))
    return obj

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hi! Your options are at /getQueries (queryNum as mandatory param)  & /getClusters (name, n_clusters, dist, printing, q_type & emb_type as params). '


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # features = clus.Features() 
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
