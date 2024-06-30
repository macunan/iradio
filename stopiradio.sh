#!/bin/bash
pkill sox;
ps ux |grep ffmpeg |grep wav |awk '{print $2}'| xargs kill -9 
ps -ef | grep -v grep | grep fm_transmitter | awk '{print $2}'|xargs kill -INT;
sleep 2;
pkill fm_transmitter
