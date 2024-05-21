#!/bin/bash
ps -ef | grep -v grep | grep fm_transmitter | awk '{print $2}'|xargs kill -INT;
ps ux  | grep ffmpeg|grep wav | awk '{print $2}'|xargs kill -INT;
ps ux  | grep sox | grep wav| awk '{print $2}'|xargs kill -INT;
