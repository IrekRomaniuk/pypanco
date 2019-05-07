# pypanco
Palo Alto Network toolset based on pan-python an pandevice

```
$ python pypanco.py
Palo Alto Network toolset
(Panco)Ctrl-D
```

### help

```
Palo Alto Network toolset, remember to setup credentails (cred [user] [pass])


(Panco) help

Documented commands (type help <topic>):
----------------------------------------
check_soft     help          set_time     upgrade_soft
cred           restart       show_job     upgrade_soft_pandevice
download_soft  set_panorama  show_system

Undocumented commands:
----------------------
EOF
```
### download_soft

```
(Cmd) download_soft 9.0.0 10.111.3.7 admin password
Downloading software 9.0.0 on 10.111.3.7 with admin and pa...
Download job enqueued with jobid 248
(Cmd)
```
### show_job

```
(Panco) show_job 87 10.111.3.6 admin password
Looking for jobid 87 on 10.111.3.6 with admin and pa...
OK
(Panco)
```

### set_time

```
(Panco) set_time 52.190.27.136 admin password
success
Commiting... timezone: US/Eastern ntp: 10.10.21.215 and  10.20.21.215
success
(Panco)
```

### check_soft 

```
(Panco) check_soft 10.111.131.6 admin password 1
Checking software on 10.111.131.6 with admin and pa...
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


### upgrade_soft

```
(Panco) show_system 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
8.1.5
(Panco) upgrade_soft 8.1.6 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
Software install job enqueued with jobid 25. Run 'show jobs id 25' to monitor its status. Please reboot the device after the installation is done.
(Panco) show_job 25 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
PEND
(Panco) show_job 25 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
PEND
(Panco) show_job 25 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
OK
(Panco) restart 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
(Panco) show_system 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
URLError: reason: [Errno 111] Connection refused
(Panco) show_system 1.1.1.1
Running command on 1.1.1.1 with user admin and password p...
8.1.6
```
### upgrade_soft_pandevice

```
(Panco) upgrade_soft_pandevice 8.1.7 10.111.2.20
Device xxxx attempt to install content version latest failed: ['Failed to update content with following message: encfilesize is 48722240\nNo threat content update is applied. No valid Threat prevention license.\nexiting with 255\n']
```

### waitfor_url 

```
(Panco) waitfor_url 30 5 10.44.2.20
No Response: Sleeping for 30s...Remaining 298s
No Response: Sleeping for 30s...Remaining 267s
No Response: Sleeping for 30s...Remaining 216s
No Response: Sleeping for 30s...Remaining 165s
Up but not auth, sleeping for 30s...Remaining 132s
Up but not auth, sleeping for 30s...Remaining 102s
Portal https://10.44.2.20 is up and running
(Panco)
```