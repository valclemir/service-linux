#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='classificador-service.log'
DIR='/home/service-linux/classificador-fichas' #@ Diretorio do arquivo .py
DIRECTORYTOEXEC=$DIR

TIMESLEEP=$(cat config-server.json | jq '.config.timesleep')

FLGSILENT=1

FILELOG=$LOGDIRECTORY/$FILELOGNAME

print () {
    if [[ $FLGSILENT -gt 0 ]]; then
	echo $1 >> $FILELOG &
    fi
}

execTo () {
    python3 $1 1>> $2 2>> $2  #Executa em paralelo
}

if [[ -e $DIRECTORYTOEXEC ]]; then
    print "Run Files"
    FILESTORUN=$(ls $DIRECTORYTOEXEC)
    echo $FILESTORUN
    while [[ true ]]; do
	for i in $FILESTORUN; do
	    FILESPY="$(find -name classificador.py)"
            echo $FILESPY
	    execTo $FILESPY $FILELOG & #@ Roda em paralelo
	    #echo $FILESPY
	done;
	sleep $TIMESLEEP
    done;
else
    print "not exist directory"
fi


