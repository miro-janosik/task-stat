#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api

from TaskStatus import TaskStatus

app = Flask(__name__)
api = Api(app)

api.add_resource(TaskStatus, "/task-stat/")

# debug=True makes application to run twice, so two times starting a master...
app.run(host='0.0.0.0', port=8081, debug=False)
