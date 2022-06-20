#!/bin/bash
ps -ef | grep -v grep | grep fm_transmitter | awk '{print $2}'|xargs kill -INT
