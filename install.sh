#!/bin/sh

PATH=/usr/bin:/bin
CURDIR=`pwd`

echo " "
echo "RRDWeather installer"
echo "--------------------"
echo " "
echo "Make sure you have edited rrdweather.conf and rrdweather_cron before continuing"
echo -n "Do you want to (c)ontinue or (q)uit ? : "
read CONTINUE

if [ $CONTINUE != "c" ]
then

	exit 1

else

	# *.sh
	
	if [ ! -d /usr/share/rrdweather ]
	then
		echo "Making directory /usr/share/rrdweather ..."
		mkdir /usr/share/rrdweather
	fi
	echo "Copying script files..."
	cp $CURDIR/files/*.sh /usr/share/rrdweather
	
	# rrdweather.conf
	
	echo "Copying config file..."
	cp $CURDIR/files/rrdweather.conf /etc
	
	# rrdweather_cron
	
	echo "Copying cron file..."
	cp $CURDIR/files/rrdweather_cron /etc/cron.d/rrdweather
	
	# weather.cgi
	
	echo "Copy weather.cgi in a cgi-bin enabled directory of the webserver."

fi
