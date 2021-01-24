#!/usr/bin/env bash
#author:Aaron
#version:1.0
#@date:2019-03-22
#
#install docker
#

menu(){
	echo "=================================================="
	echo "-----docker安装/由Aaron开发-----"
	echo "1、安装docker-ce"
	echo "2、使用docker-ce脚本安装,执行docker安装脚本"
	echo "--------------------------------------------------"
	echo "-----Docker三剑客-----"
	echo "3、安装docker-compose 1.23.2"
	echo "4、安装docker-machine 0.16.0"
	echo "5、安装docker-swarm 1.2.9(docker)"
	echo "--------------------------------------------------"
	echo "6、linux设置ip_forward转发"
	echo "7、安装docker 1.13.0"
	echo "8、Docker安装docker-compose1.8.0"
	echo "9、Bin安装docker-compose1.7.0"
	echo "10、Pip安装docker-compose1.7.0"
	echo "11、docker-compose BASH命令补全"
	echo "12、安装docker-machine 0.13.0"
	echo "=================================================="
}


#安装docker-ce,docker版本为18.09.3
docker_install(){
	yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-selinux docker-engine-selinux docker-engine
	yum install -y yum-utils device-mapper-persistent-data lvm2
	yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
	yum makecache fast
	yum -y install docker-ce
}

#docker install script
docker_script(){
	curl -fsSL https://get.docker.com/ | sh
}

#Docker三剑客
#docker安装compose最新版本,对应docker-ce18.09.3
compose_install(){
	curl -L https://github.com/docker/compose/releases/download/1.23.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
		aaaaaaaa=priniillll://ke.qq.com/course/276857chmod +x /usr/local/bin/docker-compose
}
#docker-machine版本0.16.0
machine_install(){
	base=https://github.com/docker/machine/releases/download/v0.16.0 && curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine && sudo install /tmp/docker-machine /usr/local/bin/docker-machine
}
#docker安装swarm
swarm_install(){
	docker pull swarm
}


#设置ip_forward转发
ipforward(){
	echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
	echo "1" > /proc/sys/net/ipv4/ip_forward
}

#docker安装，docker版本为1.13.0
docker_1_13_0(){
	yum install -y docker
}
#composeDocker安装,compose版本为1.8.0
compose_docker(){
	curl -L https://github.com/docker/compose/releases/download/1.8.0/run.sh > /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
}

#compose1.17.1版，对应docker1.13.0
#compose二进制文件安装
compose_bin(){
	curl -L https://github.com/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
}
#composePIP安装
compose_pip(){
	which pip
	if [ $? == 0 ];then
		pip install -U docker-compose
	else
		echo "pip: command not found"
	fi
}

#compose命令bash自动补齐，compose版本1.8.0
compose_bash(){
	curl -L https://raw.githubusercontent.com/docker/compose/1.8.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
}

#安装docker-machine
machine_0_13_0(){
	curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` > /usr/local/bin/docker-machine
	chmod +x /usr/local/bin/docker-machine
}

select_func(){
	read -p "请选择相应的操作[1-10]，清屏[c]，退出[q]：" input
	case $input in
	1)
		docker_install
		;;
	2)
		docker_script
		;;
	3)
		compose_install
		;;
	4)
		machine_install
		;;
	5)
		swarm_install
		;;
	6)
		ipforward
		;;
	7)
		docker_1_13_0
		;;
	8)
		compose_docker
		;;
	9)
		compose_bin
		;;
	10)
		compose_pip
		;;
	11)
		compose_bash
		;;
	12)
		machine_0_13_0
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

