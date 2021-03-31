#!/bin/sh

#rm /root/output/*
while read line
do
	NAME=$(echo $line | cut -d' ' -f1 | sed 's,.*/,,')
	DIR=$(echo $line | cut -d' ' -f1)
	MASTERDIR=$(echo $line | cut -d' ' -f2)
	echo "DEBUG: $LINE NAME=$NAME DIR=$DIR"
	if [ ! -e /root/output/$DIR/zmq_auth/${NAME}.key ];then
		/root/create_certificate.py $NAME --directory /root/output/$DIR/zmq_auth/ || exit $?
	else
		echo "DEBUG: ZMQ files for $NAME already exists"
	fi
	if [ ! -z "$MASTERDIR" -a "$MASTERDIR" != "$DIR" ];then
		MASTERNAME=$(echo $MASTERDIR | sed 's,.*/,,')
		cp /root/output/$MASTERDIR/zmq_auth/$MASTERNAME.key /root/output/$DIR/zmq_auth/master.key || exit $?
		cp /root/output/$DIR/zmq_auth/$NAME.key /root/output/$MASTERDIR/zmq_auth/ || exit $?
		chown $(cat /root/id) /root/output/$MASTERDIR/zmq_auth/* || exit $?
	fi
	# All files are generated by root, chown them to the user using the docker
	chown $(cat /root/id) /root/output/$DIR/zmq_auth/* || exit $?
done < /root/zmq_genlist