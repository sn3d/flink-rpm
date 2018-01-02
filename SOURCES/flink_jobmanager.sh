#!/bin/sh
# flink daemon
# chkconfig: 345 20 80
# description: flink daemon
# processname: flink

NAME=flink
DESC="Flink Jobmanager"
SCRIPTNAME=/etc/init.d/$NAME
SUCMD="runuser - flink -c "
PIDFILE="/tmp/flink-flink-jobmanager.pid"

case "$1" in
  start)
    $SUCMD "/usr/share/flink/bin/flink-daemon.sh start jobmanager --configDir /usr/share/flink/conf --executionMode cluster"
  ;;

  status)
    printf "%-50s" "Checking $NAME..."
    if [ -f $PIDFILE ]; then
      PID=`tail -n 1 ${PIDFILE}`
      if [ -z "`ps axf | grep ${PID} | grep -v grep`" ]; then
        printf "%s\n" "Process dead but pidfile exists"
        exit 1
      else
        echo "Running"
      fi
    else
      printf "%s\n" "Service not running"
      exit 1
    fi
  ;;

  stop)
    $SUCMD "/usr/share/flink/bin/flink-daemon.sh stop jobmanager"
  ;;

  restart)
    $0 stop
    $0 start
  ;;

  *)
    echo "Usage: $0 {status|start|stop|restart}"
    exit 1

esac
