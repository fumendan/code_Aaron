#!/usr/bin/env bash
#author:Aaron
#version:0.1
#@date:2018-01-27
#
#function:对MySQL操作

#显示界面
menu(){
	echo "=================================================="
	echo "-----MySQL删库脚本/由Aaron开发-----"
	echo "---1、安装MySQL-YUM源"
	echo "---2、安装MySQL数据库"
	echo "---3、删库、删日志"
	echo "---4、初始化开服务"
	echo "---5、修改密码"
	echo "=================================================="
}

#安装MySQL-YUM源
mysql_yum(){
	echo "正在下载mysql的YUM源。。。" 
    local reval
    wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm -O /opt/mysql57-community-release-el7-11.noarch.rpm
    reval=$?
    if [ $reval -eq 0 ];then
        rpm -ivh /opt/mysql57-community-release-el7-11.noarch.rpm
        echo "MySQL的YUM源安装完成！"
    else
        echo "安装失败！检查错误后，请重新安装！"
    fi
}

#安装MySQL数据库
mysql_install(){
	yum -y install mysql-community-server mysql-community-client && echo "MySQL安装成功！" || echo "MySQL安装失败！"
}

#删除/var/log/mysqld.log /var/lib/mysql/*
mysql_delete(){
	systemctl stop mysqld || pkill -9 mysqld
	rm -fr /var/lib/mysql/* && cat /dev/null >/var/log/mysqld.log && echo "可以跑路喽"
}

#启动数据库，第一次启动初始化
mysql_reset(){
	echo "请稍等。。。"
	systemctl start mysqld && echo "启动数据库成功！" || echo "启动数据库失败！"
}

#更改root密码
mysql_root(){
	local reval
	lsof -i:3306 &>/dev/null
	reval=$?
	if [ reval == 0 ];then
		local oldpas newpas
		read -p "请输入一个复杂的mysql密码(包含大小写字母，特殊字符)：" newpas
		oldpas=$(grep 'password is generated for' /var/log/mysqld.log | awk -F'localhost: ' '{print $2}' )
		mysqladmin -uroot -p"$oldpas" password $newpas
	else
		echo "请启动mysqld服务"
	fi
}

#选择功能
select_func(){
	local input
	read -p "请选择相应的操作[1-3]，清屏[c]，退出[q]：" input
	case $input in
	1)
		mysql_yum
		;;
	2)
		mysql_install
		;;
	3)
		mysql_delete
		;;
	4)
		mysql_reset
		;;
	5)
		mysql_root
		;;
	c|C)
		clear
		menu
		;;
	q|Q)
		exit
		;;
	*)
		echo "输入错误，请重新输入！"
		;;
	esac
}

clear
menu
while :
do
	select_func
done

