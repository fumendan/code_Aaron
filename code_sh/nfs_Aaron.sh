#!/bin/bash
#author：aaron
#version：1.0
#function：配置NFS服务
#

#交互界面
interface(){
    echo "=================================================="
    echo "----------NFS服务配置/由Aaron开发----------"
    echo "-----1、配置NFS服务端"
    echo "-----2、配置NFS客户端"
    echo "=================================================="
    read -p "-----请输入您要增加的配置选项：" SC
}

#服务端配置
server(){
    echo "==========安装相应的软件包=========="
    yum -y install nfs-utils rpcbind
    echo "写入/etc/exports文件一行内容：" 
    read line
    echo "正在写入共享配置文件。。。"
    echo $line >> /etc/exports && echo "写入配置文件成功"
    echo "正在启动服务。。。"
    systemctl restart nfs && echo "服务重启成功"
    echo "NFS服务端配置完成"
}

#客户端配置
client(){
    echo "==========安装相应的软件包=========="
    yum -y install nfs-utils rpcbind
    echo "=================================================="
    read -p "输入服务端的IP：" serverIP
    showmount -e $serverIP
    read -p "输入挂载点(据对路径):" mP
    read -p "输入服务器分享的目录(包含IP)：" mS
    echo "正在挂载。。。"
    mount $mS $mP
    echo "挂载成功！"
}

menu(){
interface
case $SC in
1)
    server
;;
2)
    client
;;
esac
}

#程序开始执行处
menu
