#!/usr/bin/env bash
#author：aaron
#version：0.2
#@date：2018-01-12
#
#function：编译安装MySQL(5.7.20)脚本
#

menu(){	
	echo "=================================================="
	echo "-----LNMP、LNMPA、LAMP环境搭建/由Aaron开发-----"
	echo "功能菜单："
	echo "===1、安装MySQL(5.7.20)"
	echo "===2、安装MySQL-YUM源"
	echo "--------------------------------------------------"
	echo "---c清屏、m菜单、q退出"
	echo "=================================================="
}

#清理环境_MySQL
mysql_clear(){
	echo "正在清理mariadb。。。"
	local reval
	rpm -q mariadb &>/dev/null
	reval=$?
	if [ $reval -ne 0 ];then
		yum earse -y mariadb mariadb-server mariadb-libs mariadb-devel
		userdel -r mysql &>/dev/null
		rm -fr /etc/my* &>/dev/null
		rm -fr /var/lib/mysql &>/dev/null
		echo "mariadb清理完成。"
	fi
}
#下载安装包_MySQL	安装包解压到/usr/local/src/下
mysql_download(){
	echo "检测安装包。。。"
	if [ ! -f /opt/mysql-5.7.20.tar.gz ];then
		echo "未监测到安装包，正在下载安装包。。。"
		local reval
		which wget &>/dev/null
		reval=$?
		if [ $reval -ne 0 ];then
			wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.20.tar.gz -O /opt/mysql-5.7.20.tar.gz
		fi
	fi
	echo "正在解压MySQL。。。"
	if [ -f /usr/local/src/mysql-5.7.20 ];then
		rm -fr /usr/local/src/mysql-5.7.20
	fi
	tar xvf /opt/mysql-5.7.20.tar.gz -C /usr/local/src/
}
#mysql环境变量/usr/local/mysql/bin写进PATH	添加的环境变量到～/.bash_profile文件
mysql_path(){
	echo "MySQL环境变量正在写入文件。。。"
	echo 'export PATH=$PATH:/usr/local/mysql/bin' >> ~/.bash_profile
	source ~/.bash_profile
	echo "MySQL环境变量配置完成！"
}

#编译安装MySQL
mysql_install(){
	local yn reval
	read -p "安装MySQL需要清理系统内的mariadb数据库，是否编译安装MySQL[y|n]" yn
	if [ $yn != "y" ] && [ $yn != "Y" ];then
		exit
	fi
	#调用函数清理MySQL安装环境
	mysql_clear
	#下载安转包
	mysql_download
	echo "正在准备安装环境。。。"
	yum install -y ncurses ncurses-devel openssl-devel bison gcc gcc-c++ make cmake
	echo "创建MySQL系统用户。。。"
	useradd -r -M -s /sbin/nologin mysql
	echo "MySQL正在编译安装。。。"
	cd /usr/local/src/mysql-5.7.20/
	cmake . -DDOWNLOAD_BOOST=1 -DWITH_BOOST=boost_1_59_0/ -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DSYSCONFDIR=/etc -DMYSQL_DATADIR=/usr/local/mysql/data -DINSTALL_MANDIR=/usr/share/man -DMYSQL_TCP_PORT=3306 -DMYSQL_UNIX_ADDR=/tmp/mysql.sock -DDEFAULT_CHARSET=utf8 -DEXTRA_CHARSETS=all -DDEFAULT_COLLATION=utf8_general_ci -DWITH_READLINE=1 -DWITH_SSL=system -DWITH_EMBEDDED_SERVER=1 -DENABLED_LOCAL_INFILE=1 -DWITH_INNOBASE_STORAGE_ENGINE=1 
	reval=$?
	if [ $reval -ne 0 ];then
		exit
	fi
	make && make install
	echo "初始化MySQL。。。"
	local input pas
	read -p "请尝试修改MySQL初始密码：" input
	echo "请稍等。。。"
	#修改权限
	chown -R mysql.mysql /usr/local/mysql
	#mysql初始化，生成随机密码，并生成/usr/local/mysql/data文件
	/usr/local/mysql/bin/mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data &>/tmp/mysql_init.log
	cat /tmp/mysql_init.log
	#获取随机密码
	pas=$(cat /tmp/mysql_init.log |awk -F'host: ' '/localhost: /{print $2}')
	echo -e "=====初始密码：\t$pas\t====="
	echo -e "[mysqld]\nbasedir=/usr/local/mysql\ndatadir=/usr/local/mysql/data" >/etc/my.cnf
	#启动MySQl
	/usr/local/mysql/bin/mysqld_safe --user=mysql &
	sleep 10		#静静的等待MySQL启动
	/usr/local/mysql/bin/mysqladmin -u root -p$pas passwd $input && echo "MySQL密码修改成功！" || input=$pas
	echo "MySQL已安装完成！"
	#建议添加MySQL的
	read -p "是否把MySQL的环境变量添加到PATH？[y|n]" yn
	if [ $yn == "y" ];then
		mysql_path
	fi
	echo -e "你可以使用MySQL了，用户名：root\t密码：$input"
}

#安装mysql的yum源
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

#选择功能函数
select_function(){
	read -p "请选择相应的操作[1-5]，清屏[c]，显示菜单[m]:" input
	case $input in
	1)
		mysql_install
		;;
	2)
		mysql_yum
		;;
	c|C)
		clear
		menu
		;;
	m|M)
		menu
		;;
	q|Q)
		exit
		;;
	*)
		echo "输入错误！"
		;;
	esac
}

#程序真正开始执行的入口
clear
menu
while true
do
	select_function
done
