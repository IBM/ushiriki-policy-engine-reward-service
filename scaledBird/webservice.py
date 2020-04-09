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

from flask import Flask, request, jsonify, Blueprint
import os
from sys import exit, exc_info, argv
import json

import numpy as np
import math
import numpy.ma as ma
import random

from pathlib import Path

base_path = Path(__file__).parent

api = Blueprint('sample', __name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from math import sin, cos, exp

def ff(x,y):
    x = np.clip(x,0,1)
    y = np.clip(y,0,1)
    x *= -10
    y *= -10
    return - random.uniform(.9,1.1)*(sin(y)*exp((1-cos(x))**2) + cos(x)*exp((1-sin(y))**2) + (x-y)**2)


def ffprime(x,y,oldx,oldy):
    return ff(x*(1-oldx), y*(1-oldy))

@api.route('/evaluate/policy/', methods=['POST'])
def evaluatePolicy():
    try:
        print(request.data)
        data = request.get_json(force=True)

        if set(data.keys()) != {'1', '2', '3', '4', '5'}: raise ValueError("Improperly formatted policy")
        reward = ff(data['1'][0], data['1'][1])
        reward += ffprime(data['2'][0], data['2'][1],data['1'][0], data['1'][1]) + math.e
        reward += ffprime(data['3'][0], data['3'][1],data['2'][0], data['2'][1]) + math.e
        reward += ffprime(data['4'][0], data['4'][1],data['3'][0], data['3'][1]) + math.e
        reward += ffprime(data['5'][0], data['5'][1],data['4'][0], data['4'][1]) + math.e

        response={"statusCode":202, "data": str(reward)}
        if hasattr(request.headers,'userID'):
            print("userID: ",request.headers['userID'], response)
        else:
            print("No userID")
    except:
        print(exc_info())
        response={"statusCode":400, "message": exc_info()[0]}
    return jsonify(response)

@api.route('/evaluate/action/', methods=['POST'])
def evaluate():
    try:
        data = request.get_json(force=True)

        if data['state'] > 1:
            x,y,oldx,oldy = data['action'][0], data['action'][1], data['old'][0], data['old'][1]
            reward = ffprime(x,y,oldx,oldy) + math.e
        elif data['state'] == 1:
            reward = ff(data['action'][0], data['action'][1])
        else:
            raise ValueError('invalid state %s'%data['state'])
        
        response={"statusCode":202, "data": str(reward)}
        if hasattr(request.headers,'userID'):
            print("userID: ",request.headers['userID'], response)
        else:
            print("No userID")
    except:
        print(exc_info())
        response={"statusCode":400, "message": exc_info()[0]}
    return jsonify(response)


if __name__ == "__main__":
    application = Flask(__name__, static_url_path='')
    application.register_blueprint(api)
    port = int(os.getenv('PORT', 19877))
    application.run(host='0.0.0.0', port=port, debug=True)
