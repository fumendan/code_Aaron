#!/usr/bin/env bash
# author:Aaron
#
# 2020-08-30更新 添加脚本使用说明
# 2020-07-07更新 缩减代码
# 2020-07-02更新 优化查询速度
#
#
# 显示单个目录下文件的信息
# bash datashowinfo.sh /opt/ 2020-08-30
#
# 批量显示目录下的文件信息
# bash datashowinfo.sh file 2020-08-30
# 
# cat file
# /opt/a
# /opt/b
# /opt/c
#
# 例如显示文件信息
# 当前目录：/opt/
# 17:00:00---18:00:00     359     6.93M
# 文件数量和：359 文件大小和：6.93M       平均每个文件大小：19.76K
#
#

timesp=("00:00:00" "01:00:00" "02:00:00" "03:00:00" "04:00:00" "05:00:00" "06:00:00" "07:00:00" "08:00:00" "09:00:00" "10:00:00" "11:00:00" "12:00:00" "13:00:00" "14:00:00" "15:00:00" "16:00:00" "17:00:00" "18:00:00" "19:00:00" "20:00:00" "21:00:00" "22:00:00" "23:00:00")
#tday=`date +%F`


showinfo(){
# line 数据路径
#
	line=$1
	#判断目录是否存在
	if [ ! -d $line ];then
		echo ===== $line ===== Diretory does not exist
		exit
	fi
	#查询某天文件夹内指定文件大小等信息，line文件夹路径，cl文件数量，sum文件大小和
	info=`find $line -type f \( -newermt "$tday 00:00:00" -a -not -newermt "$tday 23:59:59" \) -printf "%s\t%p\n" | awk -v line="$line" 'BEGIN{cl=0}{sum+=$1;cl+=1};END{if(sum!=0)print line,cl,sum}'`
	aline=`echo $info | awk '{print $1}'`
	if [ "$aline" != '' ];then
		echo 当前目录：$aline
		for(( i=0;i<${#timesp[@]};i++ ))
		do
			starttime=$tday' '${timesp[i]}
			stoptime=$tday' '${timesp[$((i+1))]:-"23:59:59"}
			#查询每小时内文件数量和大小，cl文件数量，sum文件大小
			sinfo=`find $aline -type f \( -newermt "$starttime" -a -not -newermt "$stoptime" \) -printf "%s\t%p\n" | awk 'BEGIN{cl=0}{sum+=$1;cl+=1};END{if(sum!=0)printf ("%d %.2fM\n",cl,sum/1024/1024)}'`
			count=`echo $sinfo | awk '{print $1}'`
			fsize=`echo $sinfo | awk '{print $2}'`
			#显示格式
			if [ "$fsize" != '' ];then
				# 开始时间----停止时间 文件数量 文件大小和(Mb)
				echo -e "${timesp[i]}---${timesp[$((i+1))]:-"23:59:59"}\t$count\t$fsize"
			fi
		done
		allc=`echo $info | awk '{print $2}'`
		alls=`echo $info | awk '{print $3}'`
		ave=`awk 'BEGIN{printf "%.2f\n",('$alls'/'$allc')}'`
		am=`awk 'BEGIN{printf "%.2f\n",('$alls'/'1024'/'1024')}'`
		ak=`awk 'BEGIN{printf "%.2f\n",('$ave'/'1024')}'`
		echo -e "文件数量和：$allc\t文件大小和：${am}M\t平均每个文件大小：${ak}K"
	else
		#line文件夹内没有指定时间范围内的文件
		echo ===== $line
	fi
}

# 限制输入两个参数
if [ $# -eq 2 ];then
	dirfile=$1
	tday=$2
	#判断第一个参数是文件，否则是路径
	if [ -f $dirfile ];then
		for line in `cat ${dirfile}` #遍历文件内的文件路径
		do
			showinfo $line
		done
	elif [ -d $dirfile ];then
		showinfo $dirfile
	fi
else
	echo "Usage: $0 examplefile|dirpath time"
fi
