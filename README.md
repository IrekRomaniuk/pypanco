# pypanco
Palo Alto Network toolset based on pan-python

```
$ python pypanco.py
Palo Alto Network toolset
(Panco)Ctrl-D
```

### help

```
python pypanco.py
Palo Alto Network toolset
(Panco) help

Documented commands (type help <topic>):
----------------------------------------
check_soft  download_soft  help  set_time  show_job

Undocumented commands:
----------------------
EOF
```
### download_soft

```
(Cmd) download_soft 9.0.0 10.1.3.7 admin password
Downloading software 9.0.0 on 10.1.3.7 with admin and pa...
Download job enqueued with jobid 248
(Cmd)
```
### show_job

```
(Panco) show_job 87 10.1.3.6 admin password
Looking for jobid 87 on 10.1.3.6 with admin and pa...
OK
(Panco)
```

### set_time

```
(Panco) set_time 52.190.27.136 admin password
success
Commiting... timezone: US/Eastern ntp: 10.34.21.215 and  10.41.21.215
success
(Panco)
```

### check_soft 

```
(Panco) check_soft 10.1.131.6 admin password 1
Checking software on 10.1.131.6 with admin and pa...
9.0.1
9.0.0
8.1.7
8.1.6
....
7.1.2
7.1.1
7.1.0
(Panco)
```
