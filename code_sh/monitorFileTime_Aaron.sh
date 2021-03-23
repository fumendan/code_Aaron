#!/usr/bin/env bash
#author:Aaron
#date:2018-03-24
#version:0.2
#
#function:监控某个文件的三个时间
#	$1	监控的文件
#
#	输出格式:当前时间 Access|Modify|Change old_time ===> new_time

#得到某个文件的三个时间
getAMCtime(){
	local file
	file=$1
	atime=$(stat $file | grep -i "Access" | awk 'NR==2{print $2" "$3}')
	mtime=$(stat $file | grep -i "Modify" | awk '{print $2" "$3}')
	ctime=$(stat $file | grep -i "Change" | awk '{print $2" "$3}')
}

show(){
	getAMCtime $1
	echo "Access: $atime"
	echo "Modify: $mtime"
	echo "Change: $ctime"
}

monitor(){
	getAMCtime $1
	while :
	do
		at=$atime
		mt=$mtime
		ct=$ctime
		getAMCtime $1
		if [ "$at" != "$atime" ];then
			echo "`date +%F" "%T` Access: $at ==> $atime"
			at=$atime
		elif [ "$mt" != "$mtime" ];then
			echo "`date +%F" "%T` Modify: $mt ==> $mtime"
			mt=$mtime
		elif [ "$ct" != "$ctime" ];then
			echo "`date +%F" "%T` Change: $ct ==> $ctime"
			ct=$ctime
		fi
	done
}

case $1 in
show)
	show $2
	;;
monitor)
	show $2
	monitor $2
	;;
*)
	echo "Usage: $0 {show|monitor} file"
	exit
	;;
esac
