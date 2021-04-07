#!/usr/bin/env bash
#author:Aaron
#version:1.0
#
#
hostname=`hostname`
ip=`ifconfig | grep 'inet ' | awk '{print $2}'`
corenum=``

