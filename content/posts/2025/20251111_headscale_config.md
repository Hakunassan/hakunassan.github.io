---
author: "Hakuna"
title: Headscale相关配置
slug: headscale_config
description: ""
summary: "搭建完Headscale服务端后，使用Tailscale连接的配置"
date: 2025-11-11 09:25:04
draft: false
ShowToc: true
TocOpen: true
tags:
  - Headscale
categories:
  - Devops
---

***!!!前提是headscale服务端已经搭建好，客户端上tailscale已经安装好!!!***

### 1.添加用户
```shell
# 服务端执行
sudo docker exec headscale headscale users create username
```
### 2.生成authkey
```shell
# 服务端执行
# 查询用户的id
sudo docker exec headscale headscale users list
# 根据id生成，假设id是1
sudo docker exec headscale headscale preauthkeys create --reusable -u 1
```
### 3.注册客户端
```shell
# 在客户端运行
tailscale up --login-server https://服务端地址 --authkey 生成的key
```
### 4.配置子路由
```shell
# 这台节点必须在你的局域网里，并且可以访问你想要连接的内网设备
# 比如一台 Linux 或 Windows 机器，IP 假设为 192.168.31.10，你的局域网是 192.168.31.0/24
# 先注册客户端
tailscale up --login-server https://服务端地址 --authkey 生成的key
# 广播子路由，服务端执行
sudo tailscale up --advertise-routes=192.168.31.0/24
# 查询节点id，服务端执行
sudo docker exec headscale headscale nodes list
# 服务端批准，此处节点id为2
sudo docker exec headscale headscale nodes approve-routes --identifier 2 --routes 192.168.31.0/24
```
### 5.测试网络