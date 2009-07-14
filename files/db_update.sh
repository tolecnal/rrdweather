#!/bin/sh

# RRDWeather
# Released under the GNU General Public License
# http://www.wains.be/projects/rrdweather/

PATH=/usr/bin:/bin

. /etc/rrdweather.conf

##########################################################################################
###### YOU SHOULD NOT EDIT ANYTHING BELOW THIS LINE ######################################
##########################################################################################

for ZIP in ${ZIPS}
do

	if [ -d "${TMPDIR}" ]; 
		then 			
			cd ${TMPDIR}
		else
			mkdir ${TMPDIR}
			chown ${WWWUSER}:${WWWGROUP} ${TMPDIR}
			chmod 777 ${TMPDIR}
			cd ${TMPDIR}
	fi
	
	cd ${TMPDIR}

	if [ $DEBUG = "y" ]	
	then
		echo "Debug mode"
		echo "1. Connection test to www.google.com"
		echo "===================================="
		ping -c 4 www.google.com
		echo ""
	else
		curl -q yahoowidget.weather.com > /dev/null 2>&1
	fi

	sleep 3s
	if [ $? -eq 0 ]
	then
	
		if [ $DEBUG = "y" ]
		then
			echo "2. XML retrieval from xoap.weather.com"
			echo "======================================"
			wget "http://yahoowidget.weather.com/weather/local/${ZIP}?cc=*&unit=${UNIT}"
			echo ""
		else
			wget -q "http://yahoowidget.weather.com/weather/local/${ZIP}?cc=*&unit=${UNIT}"
		fi

		mv "${ZIP}?cc=*&unit=${UNIT}" "${ZIP}.xml"
		sleep 5s
		
		if [ ${UNIT} = "m" ]
		then
			REAL=`cat ${ZIP}.xml | grep "<tmp>" |  awk -F'>' '{print $2}' | awk -F'<' '{print$1}' | sed -re 's/(N|n|A|a|\/)//g'`
			FELT=`cat ${ZIP}.xml | grep "<flik>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
			DEW=`cat ${ZIP}.xml | grep "<dewp>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
			HUMIDITY=`cat ${ZIP}.xml | grep "<hmid>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
			WIND=`cat ${ZIP}.xml | grep "<s>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(C|c|L|l|M|m|N|n|A|a|\/)//g'` 
			PRESSURE=`cat ${ZIP}.xml | grep "<r>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g;s/\.[0-9]{1,2}//g'`
			UV=`cat ${ZIP}.xml | grep "<i>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		
		else
		        REAL=`cat ${ZIP}.xml | grep "<tmp>" |  awk -F'>' '{print $2}' | awk -F'<' '{print$1}' | sed -re 's/(N|n|A|a|\/)//g'`
		        FELT=`cat ${ZIP}.xml | grep "<flik>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		        DEW=`cat ${ZIP}.xml | grep "<dewp>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		        HUMIDITY=`cat ${ZIP}.xml | grep "<hmid>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		        WIND=`cat ${ZIP}.xml | grep "<s>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(C|c|L|l|M|m|N|n|A|a|\/)//g'`
		        PRESSURE=`cat ${ZIP}.xml | grep "<r>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		        UV=`cat ${ZIP}.xml | grep "<i>" |  awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | sed -re 's/(N|n|A|a|\/)//g'`
		fi
		
		if [ ${DEBUG} = "y" ]
		then
			echo "3. Values found"
			echo "==============="
			echo "Real temperature . :" ${REAL}
			echo "Felt temperature . :" ${FELT}
			echo "Dew point ........ :" ${DEW}
			echo "Humidity ......... :" ${HUMIDITY}
			echo "Wind ............. :" ${WIND}
			echo "Pressure ......... :" ${PRESSURE}
			echo "UV index ......... :" ${UV}
		
		else
			rrdtool update ${RRDDIR}/${ZIP}/real.rrd N:${REAL}
			rrdtool update ${RRDDIR}/${ZIP}/felt.rrd N:${FELT}
			rrdtool update ${RRDDIR}/${ZIP}/dew.rrd N:${DEW}
			rrdtool update ${RRDDIR}/${ZIP}/humidity.rrd N:${HUMIDITY}
			rrdtool update ${RRDDIR}/${ZIP}/wind.rrd N:${WIND}
			rrdtool update ${RRDDIR}/${ZIP}/pressure.rrd N:${PRESSURE}
			rrdtool update ${RRDDIR}/${ZIP}/uv.rrd N:${UV}
		fi
		
	else 
	
		echo "RRDWeather thinks the connection is down."
		echo "It won't do anything until the connection is back."
		exit 1
	
	fi

done

exit 0
