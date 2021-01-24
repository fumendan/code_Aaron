package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
)

type Monitor struct {
	Name     string `json:"name"`
	Path     string `json:"path"`
	Matchreg string `json:"matchreg"`
	Label    int    `json:"label"`
}

type Config struct {
	RootPath string    `json:"rootpath"`
	Monitor  []Monitor `json:"monitor"`
}

func getdirinfo(mon Monitor) (map[string]int, map[string]int64) {
	//ilist := make(map[string][]string)
	ilist := make(map[string]int, 500)
	slist := make(map[string]int64, 500)
	filepath.Walk(mon.Path, func(path string, info os.FileInfo, err error) error {
		filenameRegex := regexp.MustCompile(mon.Matchreg)
		params := filenameRegex.FindStringSubmatch(path)
		if len(params) != 0 {
			//ilist[params[mon.Label[0]]] = append(ilist[params[mon.Label[0]]], params[mon.Label[1]])
			if _, ok := ilist[params[mon.Label]]; ok {
				ilist[params[mon.Label]] += 1
			} else {
				ilist[params[mon.Label]] = 1
			}
			slist[params[mon.Label]] += info.Size()
		}
		return nil
	})
	//for k, v := range ilist {
	//	fmt.Println(k, v)
	//}
	return ilist, slist
}

func getfilenum(rootpath string) (map[string]int, map[string]int64) {
	allsum := make(map[string]int, 100)
	allsize := make(map[string]int64, 100)
	filepath.Walk(rootpath, func(path string, info os.FileInfo, err error) error {
		if !info.IsDir() {
			allsum[filepath.Dir(path)] += 1
		}
		allsize[filepath.Dir(path)] += info.Size()
		return nil
	})
	//字节
	return allsum, allsize
}

func main() {
	//解析json配置文件
	conffile := "./config.json"
	confbrf, _ := ioutil.ReadFile(conffile)
	var cf Config
	err := json.Unmarshal(confbrf, &cf)
	if err != nil {
		fmt.Println(err)
	}
	//正则匹配
	if cf.RootPath != "" {
		allsum, allsize := getfilenum(cf.RootPath)
		for k, v := range allsum {
			fmt.Println("path:", k, "amount:", v, "size:", allsize[k]/1024, "KB")
		}
	} else {
		for _, item := range cf.Monitor {
			fmt.Println("Data Type：", item.Name)
			flist, slist := getdirinfo(item)
			for k, v := range flist {
				fmt.Println("filter:", k, "amount:", v, "size:", slist[k]/1024, "KB")
			}
		}
	}

}

