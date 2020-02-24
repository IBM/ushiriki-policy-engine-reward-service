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

import yaml
import importlib
from swagger_ui_bundle import swagger_ui_path
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
from flask import Flask, Blueprint, render_template, request, send_from_directory, jsonify
from sys import exit, exc_info, argv
import os.path

swaggerapi = Blueprint('swagger_ui', __name__, static_url_path='', static_folder=swagger_ui_path, template_folder=swagger_ui_path)

SWAGGER_UI_CONFIG = {
    "openapi_spec_url": "/spec"
}

if len(argv)>1:
    configfile = argv[1]
else:
    configfile = "config.yaml"


if(not os.path.isfile(configfile)):
    raise ValueError("You must provide a valid filename for the config file as an argument")

with open(configfile, 'r') as stream:
    try:
        yamldata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

application = Flask(__name__, static_url_path='')

endpoints = []
for item in yamldata:
    mod = importlib.import_module("%s.%s" % (yamldata[item]['module_path'],yamldata[item]['module']))
    endpoints.append((mod, item))

@swaggerapi.route('/')
def swagger_ui_index():
    return render_template('index.j2', **SWAGGER_UI_CONFIG)

@application.route("/spec")
@cross_origin()
def spec():
    swag = swagger(application)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Rewards API"
    return jsonify(swag)

for item in endpoints:
    application.register_blueprint(item[0].api, url_prefix = '/%s'%item[1])

application.register_blueprint(swaggerapi, url_prefix = "/ui")

port = int(os.getenv('PORT', 19877))

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=port, debug=True)
