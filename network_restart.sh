#!/bin/bash
connection_test=`ping -c1 192.168.31.1 | grep  -o '1 packets transmitted, 1 received'`
good_connection="1 packets transmitted, 1 received"
#echo $good_connection
#echo $connection_test

if [ "$connection_test" != "1 packets transmitted, 1 received" ]
then
echo "issues"
restart_iradio=`netctl restart wlan`
 else
echo "all ok"
 fi

