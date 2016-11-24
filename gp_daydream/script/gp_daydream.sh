#!/bin/sh

# defaults
# actions
if [ "$1" == "start" ]; then
	echo "[gp_daydream.sh] starting process..."
	$0 gp_daydream> /dev/null 2>&1 &
	echo "[gp_daydream.sh] started process."
	exit 0
elif [ "$1" == "stop" ]; then
	echo "[gp_daydream.sh] killing process..."
#    killall $(basename $0)
	ps aux | grep "$0" | grep "gp_daydream" | awk '{print "kill " $2 }' | sh
    ps -ef|grep "$0"|grep -v grep | grep -v stop
	exit 0
elif [ "$1" == "restart" ]; then
	$0 stop
	$0 start
	exit 0
elif [ "$1" != "gp_daydream" ]; then
	exit 1
fi

export PATH=$PATH:/usr/local/bin
cd /home/ghn1534/ProTest/scrapy/gp_vpn_crawler/gp_daydream
#today=`date "+%j"`
#echo "today:" + $today
#lastday=$today

today=`date +"%Y-%m-%d"`
echo $today
#next_date=`date +"%Y-%m-%d" -d "+7day"`
next_date="2016-11-30"
echo $next_date

while true; do
    today=`date +"%Y-%m-%d"`
    if [ $next_date != $today ]; then
        sleep 1800
        continue
    fi
    echo "start:"
    next_date=`date +"%Y-%m-%d" -d "+7day"`
    echo $next_date
    echo "connecting l2tp vnp ..."
    echo "d example" > /var/run/xl2tpd/l2tp-control
    sleep 15
    echo "c example" > /var/run/xl2tpd/l2tp-control
    sleep 15
    echo "route -n info:"
    route -n
    echo "add route info ... "
    route add -host  216.58.199.238/32 dev ppp0
    sleep 1
    route add -host  216.58.196.238/32 dev ppp0
    sleep 1
    route add -host  216.58.197.14/32 dev ppp0
    sleep 1
    route add -host  172.217.26.110/32 dev ppp0
    sleep 3
    echo "route -n info:"
    route -n
    scrapy crawl daydream
    sleep 10
    echo "----------------------------------------------------\n"
    python /home/ghn1534/ProTest/scrapy/gp_vpn_crawler/gp_daydream/script/pymail.py
    sleep 15
    echo "l2tp vpn disconnected"
    echo "d example" > /var/run/xl2tpd/l2tp-control
    sleep 15
done
