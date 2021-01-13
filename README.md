** Task status **

Script that runs as REST API that can write status of tasks and return summary of task status.

** Dependencies **

flask, flask_restful, jsonify

** Running **
nohup python3 main.py &

** Send data **
> POST to /task-stat/?group=<group>&task=<task>&status=<status>&text=Finished&desc=Finished%20fine&author=<author>

<group> should be in all caps, multiple values separated by semicolon "MMI;BUILD", should contain word naming project (MMI,ELG), and word naming process (TEST,BUILD)
<task> name of what is being done, for example mmi-regression-test-windows
<status> value from "none", "running", "good", "warn", "failed"
<author> Should name machine where it runs and process (sisyphos_nightly_build) and name of script

Send it from shell script:
> #!/bin/sh
> # changing task status: set_task_status good Task%20finished Finished%20well
> # info: http://hydra/mediawiki/index.php/Task_Stat
> HOSTNAME=$(hostname)
> set_task_status() {
>    echo $(curl -X POST "http://thanos:8081/task-stat/?group=ELG;TEST&task=elg-test-services&status=$1&text=$2&desc=$3&author=${HOSTNAME}_nightly_elg")
> }
> 
> set_task_status running Started


Send it from python:
> import requests
> def setTaskStatus(status, text, description):
>     r = requests.post("http://localhost:port/task-stat/", data={'group': 'MMI', 'task': 'nightly_linux', 'status': status, 'text' : text, 'desc' : description, 'author': 'sisyphos_nightly_build_x64' })
>     print(r.status_code, r.reason)

Send it from perl:
> sub setTaskStatus {
>   ($status, $text, $description) = @_;
>  my $res=`curl http://localhost:port/task-stat/?group=MMI&task=nightly_linux&status=$status&text=$text&desc=$description&author=sisyphos_nightly_build_x64`

** Seeing results **
> GET /task-stat/?group=MMI&period=<period>

Returns HTML page, so it can be directly requested in a browser: http://localhost:port/task-stat/?period=today

<period> can be "today", "yesterday", "week", "2019-01-31", 2019-01-15-2019-01-31" (limited to 30 days)

To implement:
* period = week (from Monday to Sunday)
* changes = yes/no (display all task changes / display only final state)
* group = filtering tasks by group(s)
* database = instead of CSV store data in DB for faster reading
