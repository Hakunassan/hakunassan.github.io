---
author: "Hakuna"
title: Linux中离线安装Docker
slug: installDocker_inLinux
description: ""
summary: "国产Linux中也能拿下！"
date: 2024-08-16 14:06:08
draft: false
ShowToc: true
TocOpen: true
tags:
  - Docker
categories:
  - DevOps
---
## 下载离线安装包
[docker-20.10.9.tgz](https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz)

## 解压压缩包
```shell
tar -xzvf docker-20.10.9.tgz
```

## 将解压后的文件拷贝至/usr/bin/目录下
```shell
cd docker
cp * /usr/bin/
```

## 编写docker.service文件
```shell
vi /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target
 
[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s
 
[Install]
WantedBy=multi-user.target
```

## 添加开机自启
```shell
systemctl enable docker
```

## 迁移docker文件目录，配置docker
```shell
sudo cp -r /var/lib/docker /data/docker
sudo nano /etc/docker/daemon.json
{
  "log-driver":"json-file",
  "log-opts": {"max-size":"500m", "max-file":"3"},
	"data-root": "/data/docker",
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "https://hub-mirror.c.163.com"]
}
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 配置docker-compose，将docker-compose文件复制至/usr/bin/下
```shell
cp docker-compose-linux-x86_64 /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
docker-compose -v
```