case "$1" in 
    start)
	echo "=========================================Starting FBVis Server============================================"
	nohup python manage.py runserver 0.0.0.0:7000 &
	LASTPID=$!
	echo $LASTPID > FBVis.pid
    ;;
    stop)
	echo "=========================================Stoping FBVis Server============================================"
	FBVISID=$(cat /home/jhun88/FBVis/pheonix.pid)
	echo $FBVISID
	pkill -9 -P $FBVISID
    ;;
esac
exit 0
