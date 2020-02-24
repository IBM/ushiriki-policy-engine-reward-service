'''
Copyright 2019 IBM Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

from flask import Flask, Blueprint, send_from_directory, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from base64 import b64decode
from io import BytesIO
from sys import exit, exc_info, argv
from numpy import logical_and, genfromtxt, sum, max, tile, array, unique, array

api = Blueprint('mashmalariav3', __name__)


@api.route('/prevalence', methods=['POST'])
@cross_origin()
def calculatePrevalenceMashMalariaV3():
    """
        Evaluates the prevalence when performing the considered intervention.
        ---
        parameters:
          - in: body
            name: body
            schema:
              id: PrevalenceObject
              required:
                  - outputDocWithIntervention
              properties:
                 outputDocWithIntervention:
                    type: string
                    description: The base64 encoded output.txt for the experiment with the intervention performed
        responses:
            200:
                description: Valid response from server (contains payload with actual status).
            404:
                description: Not Found.
            405:
                description: Method not allowed.
        """
    #dedba102ff7d490686397db2ace6b0ee
    reward = []
    try:
        outputDocWithIntervention = b64decode(request.json['outputDocWithIntervention'])

        a = genfromtxt(BytesIO(outputDocWithIntervention),delimiter=",", skip_header=True)
        if len(a.shape) == 1:
            a = a.reshape(1,-1)
        
        if "aggregate" in request.args:
            raise ValueError("Aggregate intervals unavailable for this model.")
        elif "monthly" in request.args:
            raise ValueError("Monthly intervals unavailable for this model.")
        elif "annual" in request.args:
            times = a[:,1]
            end = a[:,10]
            type = "Max Prevalence per Annum"
        elif "december" in request.args:
            raise ValueError("December intervals unavailable for this model.")
        else:
            raise ValueError("Request unavailable for this model.")
    
        reward = end.round(3).tolist()
        response={"statusCode":200, "data": {int(time): [value] for time,value in zip(times, reward)}, "type": type}
    except:
        response={"statusCode":400, "message": str(exc_info()[1]), "type": "Prevalence"}
        print(exc_info()[1])
    return jsonify(response)

@api.route('/cost', methods=['POST'])
@cross_origin()
def calculateCostMashMalariaV3():
    """
        Evaluates the cost when performing the considered intervention.
        ---
        parameters:
          - in: body
            name: body
            schema:
              id: PrevalenceObject
              required:
                  - outputDocWithIntervention
              properties:
                 outputDocWithIntervention:
                    type: string
                    description: The base64 encoded output.txt for the experiment with the intervention performed
        responses:
            200:
                description: Valid response from server (contains payload with actual status).
            404:
                description: Not Found.
            405:
                description: Method not allowed.
        """
    #dedba102ff7d490686397db2ace6b0ee
    reward = []
    try:
        outputDocWithIntervention = b64decode(request.json['outputDocWithIntervention'])

        a = genfromtxt(BytesIO(outputDocWithIntervention),delimiter=",", skip_header=True)
        if len(a.shape) == 1:
            a = a.reshape(1,-1)

        alpha, beta = 500000, 1000000
        if "aggregate" in request.args:
            raise ValueError("Aggregate intervals unavailable for this model.")
        elif "monthly" in request.args:
            raise ValueError("Monthly intervals unavailable for this model.")
        elif "annual" in request.args:
            times = a[:,1]
            end = alpha * a[:,3] + beta * a[:,5]
            type = "Cost per Annum"
        elif "december" in request.args:
            raise ValueError("December intervals unavailable for this model.")
        else:
            raise ValueError("Request unavailable for this model.")

        reward = end.round(3).tolist()
        response={"statusCode":200, "data": {int(time): [value] for time,value in zip(times, reward)}, "type": type}
    except:
        response={"statusCode":400, "message": str(exc_info()[1]), "type": "Prevalence"}
        print(exc_info()[1])
    return jsonify(response)

if __name__ == "__main__":
    import os
    application = Flask(__name__, static_url_path='')
    application.register_blueprint(api)
    port = int(os.getenv('PORT', 19877))
    application.run(host='0.0.0.0', port=port, debug=True)

