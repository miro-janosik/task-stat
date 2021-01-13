#!/usr/bin/env python3

from flask import request, jsonify, make_response, Response, render_template
from flask_restful import Resource
import csv
from datetime import datetime, date, timedelta
import traceback
from collections import defaultdict

import Common

# handle requests:
# Add information about task status:
# POST /task-stat/?group=<group>&task=nightly_linux&status=<status>&text=Finished&desc=Finished%20fine&author=<author>
# <group> should be in all caps, multiple values separated by semicolon "MMI;BUILD", should contain word naming project (MMI,ELG), and word naming process (TEST,BUILD)
# <status> can be "none", "running", "good", "warn", "failed"
# <author> Should name machine where it runs and process (sisyphos_nightly_build)
# Get information on status of tasks today:
# GET /task-stat/?group=MMI&period=<period>
# <period> can be "today", "yesterday", "week", "2019-01-31", 2019-01-15-2019-01-31" (limited to 30 days)
# <group> limiting to a specific group
# <type> can be "all" = all status changes, "last" = only last task change today, "last_or_error" = last + all errors

DATAFILE = "data.csv"
CSV_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class TaskStatus(Resource):
    
    def post(self):
        self.log("Received new request")

        try:
            # post - data are in request.form ; get - data are in request.args
            data = {}
            for key in ('group', 'task', 'status', 'text', 'desc', 'author'):
                text = request.args.get(key, '')
                # escape commas, those would not be good in CSV
                data[key] = text.replace(',', ';')

            # get data into string CSV format
            d = "{group},{task},{status},{text},{desc},{author}".format(**data)
            dt = datetime.now().strftime(CSV_DATETIME_FORMAT)
            textline = dt + "," + d + "\n"

            with open(DATAFILE, "a") as f:
                f.write(textline)
        except Exception as e:
            self.log(traceback.format_exc())
            return make_response(str(e), 500)

        self.log("Request finished.")
        return make_response("Ok", 200)

    def get(self):
        try:
            args = defaultdict(str, request.args.to_dict())

            period = args["period"]
            self.log("Parsing period:" + period)
            # today is the default:
            dateFrom = date.today()
            dateTo = date.today()

            if period == "today":
                pass # take default
            elif period == "yesterday":
                dateFrom = date.today() - timedelta(days=1)
                dateTo = dateFrom
            # last option is date in format 2019-01-31 or 2019-01-15-2019-01-31
            elif len(period) == 10:
                dateFrom = datetime.strptime(period, '%Y-%m-%d').date()
                dateTo = dateFrom
            elif len(period) == 21:
                dateFrom = datetime.strptime(period[0:10], '%Y-%m-%d').date()
                dateTo = datetime.strptime(period[11:21], '%Y-%m-%d').date()
            else:
                pass # take default
            
            # fix incorrect from-to
            delta = dateTo - dateFrom
            if (delta.days < 0):
                # if reversed then set to same day
                dateTo = dateFrom
            if (delta.days > 31):
                dateTo = dateFrom + timedelta(days=31)

            periodText = ""
            if dateFrom == dateTo:
                periodText = dateFrom.strftime("%Y-%m-%d")
            else:
                periodText = dateFrom.strftime("%Y-%m-%d") + " - " + dateTo.strftime("%Y-%m-%d")
            self.log("Parsed period:" + periodText)

            # read data and filter out
            tasks = []
            with open(DATAFILE, 'rt') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in reader:

                    # append item that did not exist in past
                    while len(row) < 7:
                        row.append("")

                    rowDateTime = datetime.strptime(row[0], CSV_DATETIME_FORMAT)
                    rowDate = rowDateTime.date()
                    
                    if rowDate < dateFrom or rowDate > dateTo:
                        continue

                    # 2020-03-30 18:23:42,MMI,nightly_linux,good,Finished,Finished fine
                    task = { 
                        'datetime':row[0], 
                        'groups':row[1], 
                        'name':row[2], 
                        'status':row[3], 
                        'text':row[4], 
                        'description':row[5], 
                        'author':row[6],
                        'display':"True",
                        }
                    tasks.append(task)

            # == type of display ==
            # options: all/last/last_or_error
            displayType = args["type"]
            if displayType is None or displayType == "":
                displayType = "last_or_error"
            self.log("Display type:" + displayType)

            if displayType != "all":
                for i,task in enumerate(tasks):
                    # display=False on items that are older, except for errors
                    if (displayType == "last_or_error") and (task['status'] == 'failed'):
                        continue
                    for j in range(i+1, len(tasks)):
                        if (task['name'] == tasks[j]['name']):
                            task['display'] = "False"
                            break

            displayingCount = sum((i['display'] == "True") for i in tasks)
            
            self.log("Rendering template with {}/{} tasks for display".format(displayingCount, len(tasks)))
            
            params = { 
                'baseurl' : 'http://thanos:8081/task-stat/',
                'group' : 'MMI',
                'period' : period,
                'type' : displayType,
            }
            
            html = render_template('tasks.html', period=periodText, tasks=tasks, params=params)
            res = make_response(html, 200)
            return res
        except Exception as e:
            self.log(traceback.format_exc())
            error = str(e)
            return make_response("<HTML><BODY>Error rendering page: {}</BODY></HTML>".format(error), 200)

    def log(self, text):
        Common.log(text)
