#!/usr/bin/expect -- 	

spawn icegridadmin -H 192.168.1.10 -P 4061 -u user -p pass
expect ">>>"
send "server stop Robot_Factory1\r"
expect ">>>"
send "server stop Robot_Factory2\r"
expect ">>>"
send "server stop Robot_Factory3\r"
expect ">>>"
send "server stop DetectorFactory\r"
expect ">>>"
send "server stop game_observer\r"
expect ">>>"
send "server stop ContainerManager\r"
expect ">>>"




