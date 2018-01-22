#!/usr/bin/expect -- 	

spawn icegridadmin -H 192.168.1.133 -P 4061 -u user -p pass
expect ">>>"
send "application patch MyDrobotsApp\r"
expect ">>>"
send "server stop MyDrobotsApp.IcePatch2\r"
expect ">>>"
send "server start Container\r"
expect ">>>"
send "server start FactoryContainer\r"
expect ">>>"
send "server start DetectorFactoryContainer\r"
expect ">>>"
send "server start Factory1\r"
expect ">>>"
send "server start Factory2\r"
expect ">>>"
send "server start Factory3\r"
expect ">>>"
send "server start DetectorFactory1\r"
expect ">>>"
send "server start client\r"
expect ">>>"
send "server start client2\r"
expect ">>>"




