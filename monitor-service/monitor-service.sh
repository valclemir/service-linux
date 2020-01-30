#!/bin/bash 

TIMESLEEP=$(cat config-monitor.json | jq '.config.timesleep')
LOG='/var/log/monitor-classificador.log'
FILEPY='monitor.py'

funcExec () {
	python3 $1 >> $2

}

while [[ true ]]; do
	funcExec $FILEPY $LOG
done;
