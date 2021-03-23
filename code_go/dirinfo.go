package main

import (
	"io/ioutil"
	"os"
	"time"
	"flag"
	"fmt"
)

/*
按修改时间过滤
basepath		string			文件路径
filelist		[]string		文件名
coltimerange	int64			分钟，分钟以内正值，分钟之前负值
*/
func FileModTime(basepath string, filelist []string, coltimerange int64) (getFilelist []string) {
	PthSep := string(os.PathSeparator)
	if coltimerange == 0 {
		return filelist
	}
	for _, v := range filelist {
		f, err := os.Open(basepath + PthSep + v)
		if err != nil {
			break
		}
		fi, err := f.Stat()
		if err != nil {
			break
		}
		if coltimerange > 0 && time.Now().Unix()-fi.ModTime().Unix() < coltimerange*60 {
			getFilelist = append(getFilelist, v)
		} else if coltimerange < 0 && time.Now().Unix()-fi.ModTime().Unix() > coltimerange*-60 {
			getFilelist = append(getFilelist, v)
		}
	}
	return
}

/*
递归便利目录下所有常规文件
basepath		string			目录路径
subpath			string			子目录
filelist		[]string		文件路径，相对路径。subpath+/+filelist
err				error			目录读取失败返回error
*/
func GetAllFiles(basepath, subpath string) (filelist []string, err error) {
	PthSep := string(os.PathSeparator)
	dir, err := ioutil.ReadDir(basepath + PthSep + subpath)
	if err != nil {
		return nil, err
	}
	for _, file := range dir {
		if file.IsDir() {
			subfile, _ := GetAllFiles(basepath, subpath+PthSep+file.Name())
			filelist = append(filelist, subfile...)
		} else {
			filelist = append(filelist, subpath+PthSep+file.Name())
		}
	}
	return filelist, nil
}

func main(){
	path:=flag.String("path","./","dir path")
	time:=flag.Int64("time",0,"search time")
	flag.Parse()
	filelist,_:=GetAllFiles(*path,"")
	allfile:=FileModTime("./",filelist,*time)
	fmt.Println(allfile)
}

