#!/usr/bin/env bash
#author:Aaron
#version:1.0
#
#function:在系统内添加python3
#
#2018-02-01 创建脚本版本0.1
#2018-04-13 更新,版本升级到1.0
#
menu(){
	echo "=================================================="
	echo "--------Python3安装/由Aaron开放--------"
	echo "---1、编译安装python3"
	echo "---2、安装ipython(命令ipython3)"
	echo "---3、安装python3虚拟环境"
	echo "---4、Vim编辑环境优化"
	echo "--------------------------------------------------"
	echo "-----c清屏、m菜单、q退出"
	echo "=================================================="
}

#编译安装Python3
python_install(){
	local reval
	yum install -y openssl-devel zlib-devel readline-devel sqlite-devel
	#从官网上下载python3的包，放在/opt下面
	if [ ! -f /opt/Python-3.6.4.tar.xz ];then
		wget -c https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz -O /opt/Python-3.6.4.tar.xz 
	fi
	#解压
	rm -fr /opt/Python-3.6.4
	tar xf /opt/Python-3.6.4.tar.xz -C /opt/ && echo "解压成功" && rm -fr /opt/Python-3.6.4.tar.xz
	#编译安装
	cd /opt/Python-3.6.4
	./configure --prefix=/usr/local/python3.6 && make && make install && echo "安装成功" || echo "安装失败"
	cd - &>/dev/null && rm -fr /opt/Python-3.6.4 
	#创建软链接
	#ln -s /usr/local/python3.6/bin/python3 /usr/bin/python3
	#ln -s /usr/local/python3.6/bin/pip3 /usr/bin/pip3
	echo 'export PATH=$PATH:/usr/local/python3.6/bin' >> /etc/profile.d/python3.sh && source /etc/profile.d/python3.sh
}

#安装ipython
ipython_install(){
	pip3 install ipython
	#ln -s /usr/local/python3.6/bin/ipython3 /usr/bin/ipython3
}

#安装python3虚拟环境
virtenv_install(){
	python3_path='/etc/profile.d/python3.sh'
	pip3 install virtualenv
	pip3 install virtualenvwrapper
	echo 'export VIRTUALENVWRAPPER_PYTHON="/usr/local/python3.6/bin/python3"' >>$python3_path
	echo 'export WORKON_HOME=$HOME/.virtualenvs' >>$python3_path
	echo 'source /usr/local/python3.6/bin/virtualenvwrapper.sh' >>$python3_path
	source $python3_path
}

#Vim编辑环境优化
vim_profile(){
	local reval
    grep "set ai" /etc/vimrc &>/dev/null
    reval=$?
    if [ reval != 0 ];then
        echo "set ai" >>/etc/vimrc
    fi
    grep "set sw=4" /etc/vimrc &>/dev/null
    reval=$?
    if [ reval != 0 ];then
        echo "set sw=4" >>/etc/vimrc
    fi
    grep "set ts=4" /etc/vimrc &> /dev/null
    reval=$?
    if [ $reval != 0 ];then
    	echo "set ts=4" >>/etc/vimrc
    fi
    grep "set si" /etc/vimrc &>/dev/null
    reval=$?
    if [ reval != 0 ];then
        echo "set si" >>/etc/vimrc
    fi
    grep "set ci" /etc/vimrc &>/dev/null
    reval=$?
    if [ reval != 0 ];then
        echo "set ci" >>/etc/vimrc
    fi
    echo "自动缩进，tab长度4。设置完成！"
}

select_fun(){
	local input
	read -p "请选择相应的操作[1-5]，清屏[c]、显示菜单[m]:" input
	case $input in
	1)
		python_install
		;;
	2)
		ipython_install
		;;
	3)
		virtenv_install
		;;
	4)
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
while :
do
	select_fun
done
