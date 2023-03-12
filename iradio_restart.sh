#!/bin/bash
connection_test=`ping -c1 192.168.31.1 | grep  -o '1 packets transmitted, 1 received'`
decoder_program_running=`ps ucx  |grep -e 'ffmpeg' -e 'sox'| wc -l`
fm_transmitter_running=`ps ucx|grep fm_transmitter|wc -l`
iradio_running=`systemctl status iradio|grep -o running`
good_connection="1 packets transmitted, 1 received"
# echo $good_connection
# echo $connection_test
# echo $fm_transmitter_running
# echo $sox_program_running

if [ "$iradio_running" == "running" ] 
then	
if [ "$connection_test" != "1 packets transmitted, 1 received" ] 
then
echo "network and iradio restarting not ok there was a network issue"
restart_iradio=` systemct restart iradio_networkrestart.service;systemctl restart iradio`
else 
echo "network ok"
fi
if [ "$fm_transmitter_running" == "0" ] || [ "$decoder_program_running" == "0" ]
then
echo "decoder not running restarting iradio"
restart_iradio=`systemctl restart iradio`
else
echo "sox/ffmpeg and fm_tranmitter is ok"
fi
fi
