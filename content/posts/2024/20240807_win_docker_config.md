---
author: "Hakuna"
title: Win10中WSL2 docker存储位置迁移
slug: 
description: 防止C盘大爆炸！
summary: "系统盘还顶得住嘛？"
date: 2024-08-08 11:17:47
draft: false
ShowToc: true
TocOpen: true
tags:
  - Docker
categories:
  - Solution
---
在windows10中安装完Docker后，想要修改Docker镜像及容器的存储位置，但是点开设置发现是这样的
![](/images/posts/2024/20240807_win_docker_config/2910378857.jpg)
这是由于docker使用了基于wsl2的方式安装。
可以通过以下方式迁移docker

```cmd
# 进入CMD,查询docker运行状态
wsl -l -v --all
```

返回结果如下图所示的话，需要先关闭docker；如果两个状态都是stopped的话，可以继续下一步操作
![](/images/posts/2024/20240807_win_docker_config/885509585.jpg)

```cmd
# 导出docker及docker-data,'D:\Docker\'为导出存储路径，可以自行修改，执行完后可以在此路径下看到导出文件
wsl --export docker-desktop D:\Docker\docker-desktop.tar
wsl --export docker-desktop-data D:\Docker\docker-desktop-data.tar

# 导出完成之后，注销现有的wsl系统
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data

# 执行后会有正在注销的提示，使用下面命令查看是否都注销成功
wsl -l -v --all

# 导入docker及docker-data,'D:\docker\docker-desktop'及'D:\docker\docker-desktop-data'为导入路径,tar包路径为之前导出的路径
wsl --import docker-desktop D:\docker\docker-desktop D:\Docker\docker-desktop.tar --version 2
wsl --import docker-desktop-data D:\docker\docker-desktop-data D:\Docker\docker-desktop-data.tar --version 2

# 导入执行完成之后，使用下面命令查看是否都导入成功
wsl -l -v --all

# 启动docker即可使用
```
