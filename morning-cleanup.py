# does two things
# 1) backup data file to archive
# 2) add all known tasks in 'todo' status

import datetime
import shutil
from TaskStatus import WriteData

# 1
t = datetime.date.today()
backupFilename = "archive/data-{}{:02}{:02}.csv".format(t.year, t.month, t.day)
shutil.copyfile("data.csv", backupFilename)

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
        { "group" : "TELEMETRY;NIGHTLY", "task" : "telemetry_server_alive_test" },
]

for task in tasks:
    data["group"] = task["group"]
    data["task"] = task["task"]

    WriteData(data)

