#!/usr/bin/env bash
#author：aaron
#version：1.1
#@date：2018-01-04
#
#function：
#1.当前网络通过ping www.baidu.com判断是否能连网，如果能连网则返回0，否则返回1
#2.对于北京千锋的内网，新机器的yum是不能使用的，通过这项功能可以使用yum
#3.安装KVM等有关的软件
#4.安装cherrytree，安装之前要先安装epel
#5.安装ntfs-3g，安装之前要先安装epel
#
#更新：
#	2018-02-02：优化设置vim编辑环境的方法
#

#全局变量
# input		用户输入的日容

menu(){
	echo "=================================================="
	echo "----------系统初始化本脚本/由Aaron开发----------"
	echo "功能菜单："
	echo "===1、检查网络是否通畅"
	echo "===2、配置YUM(仅供千锋内网使用)"
	echo "===3、安装虚拟化脚本"
	echo "===4、安装cherrytree"
	echo "===5、安装ntfs-3g"
	echo "===6、优化vim编辑环境"
	echo "-------------------------------------------------"
	echo "---c清屏、m菜单、q退出"
	echo "=================================================="
}

#检查网络是否畅通
internet(){
	ping -c1 -W1 www.baidu.com &>/dev/null
	local reval=$?
	if [ $reval -ne 0 ];then
		echo "网络不通！请检查网络后重试！"
		return 1
	else
		echo "网络通畅！！！"
		return 0
	fi
}

#配置YUM
yum_conf(){
	local yn
	read -p "仅限于北京千锋内网，是否继续(y|n)" yn
	if [ $yn == "y" ];then
		echo "正在检测...请稍等"
		sed -i 's/^mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Base.repo
		sed -i 's/^#baseurl/baseurl/g' /etc/yum.repos.d/CentOS-Base.repo
		echo "正在修改YUM配置文件。。。"
		echo "YUM配置完成!"	
	fi
	read -p "是否安装epel-release(y|n)" yn
	if [ $yn == "y" ];then
		yum -y install epel-release
		sed -i 's/^#baseurl/baseurl/' /etc/yum.repos.d/epel.repo
		sed -i 's/^mirrorlist/#mirrorlist/' /etc/yum.repos.d/epel.repo
		yum clean all
		yum makecache
	fi
}

#安装虚拟化脚本
virtual_install(){
	internet 1>/dev/null
	local reval=$?
	if [ $reval -eq 0 ];then
		yum -y install *virt* *qume* *kvm*
		systemctl start virtd
		systemctl enable virtd
	fi
}

#安装cherrytree
cherrytree_install(){
	yum -y install cherrytree
}

#安装ntfs-3g
ntfs_install(){
	yum -y install ntfs-3g
}

#优化vim编辑环境
vim_profile(){
	local reval
	grep "set ai" /etc/vimrc &>/dev/null
	reval=$?
	if [ $reval != 0 ];then
		echo "set ai" >>/etc/vimrc
	fi
	grep "set sw=4" /etc/vimrc &>/dev/null
	reval=$?
	if [ $reval != 0 ];then
		echo "set sw=4" >>/etc/vimrc
	fi
	grep "set ts=4" /etc/vimrc &> /dev/null
	reval=$?
	if [ $reval != 0 ];then
		echo "set ts=4" >>/etc/vimrc
	fi
	grep "set si" /etc/vimrc &>/dev/null
	reval=$?
	if [ $reval != 0 ];then
		echo "set si" >>/etc/vimrc
	fi
	grep "set ci" /etc/vimrc &>/dev/null
	reval=$?
	if [ $reval != 0 ];then
		echo "set ci" >>/etc/vimrc
	fi
	#grep "set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" /etc/vimrc &>/dev/null
	#reval=$?
	#if [ $reval != 0 ];then
	#	echo "set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" >>/etc/vimrc
	#fi
	#grep "set termencoding=utf-8" /etc/vimrc &>/dev/null
	#reval=$?
	#if [ $reval != 0 ];then
	#	echo "set termencoding=utf-8" >>/etc/vimrc
	#fi
	#grep "set encoding=utf-8" /etc/vimrc &>/dev/null
	#reval=$?
	#if [ $reval != 0 ];then
	#	echo "set encoding=utf-8" >>/etc/vimrc
	#fi
	echo "自动缩进，tab长度4。设置完成！"
}

sFunc(){
	read -p "请选择相应的操作[1-6]，清屏[c]，显示菜单[m]:" input
	case $input in
	1)
		internet
		;;
	2)
		yum_conf
		;;
	3)
		virtual_install
		;;
	4)
		cherrytree_install
		;;
	5)
		ntfs_install
		;;
	6)
		vim_profile
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
	sFunc
done

