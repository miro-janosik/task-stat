# does two things
# 1) backup data file to archive
# 2) add all known tasks in 'todo' status
# 3) set a status of maintenance task

import datetime
#import shutil
import zipfile
from TaskStatus import WriteData

# 1
t = datetime.date.today()
#backupFilename = "archive/data-{}{:02}{:02}.csv".format(t.year, t.month, t.day)
#shutil.copyfile("data.csv", backupFilename)
backupFilename = "archive/data-{}{:02}{:02}.zip".format(t.year, t.month, t.day)
with zipfile.ZipFile(backupFilename,'w', zipfile.ZIP_DEFLATED) as zip:
    zip.write('data.csv')

# 2
data = { "group" : "init", "task" : "x", "status" : "none", "text" : "", "desc" : "", "author" : "" }

tasks = [ 
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador--Windows" },
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador-core-Windows" },
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador-api-Windows" },
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador-clients-Windows" },
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador-lmt-Windows" },
        { "group" : "NIGHTLY;BUILD;MMI;Windows", "task" : "matador-singlepassdecoder-Windows x64" },
        { "group" : "NIGHTLY;BUILD;MMI;Linux", "task" : "matador-core-Linux" },
        { "group" : "NIGHTLY;BUILD;MMI;Linux", "task" : "matador-api-Linux" },
        { "group" : "NIGHTLY;BUILD;MMI;Linux", "task" : "matador--Linux" },
        { "group" : "NIGHTLY;BUILD;MMI;Linux", "task" : "matador-singlepassdecoder-Linux x64" },
        { "group" : "NIGHTLY;MMI;TEST;windows", "task" : "mmi-regression-test-windows" },
        { "group" : "NIGHTLY;MMI;TEST;linux", "task" : "mmi-regression-test-linux" },
        { "group" : "NIGHTLY;DOCKER;TEST", "task" : "docker-services" },
        { "group" : "CALLHOME;NIGHTLY", "task" : "telemetry-server-alive" },
]

for task in tasks:
    data["group"] = task["group"]
    data["task"] = task["task"]

    WriteData(data)

# 3
data["group"] = "maintenance"
data["task"] = "task-stat-cleanup"
data["status"] = "good"
WriteData(data)

