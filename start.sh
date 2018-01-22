#!/usr/bin/expect -- 	

spawn icegridadmin -H 192.168.1.10 -P 4061 -u user -p pass
expect ">>>"
send "application patch drobotsJCO2_App\r"
expect ">>>"
send "server start game_observer\r"
expect ">>>"
send "server start Robot_Factory1\r"
expect ">>>"
send "server start Robot_Factory2\r"
expect ">>>"
send "server start Robot_Factory3\r"
expect ">>>"
send "server start DetectorFactory\r"
expect ">>>"
send "server start Player\r"
expect ">>>"




