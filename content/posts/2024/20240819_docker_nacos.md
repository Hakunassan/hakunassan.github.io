---
author: "Hakuna"
title: Docker部署Nacos
slug: docker_nacos
description: ""
summary: "抛开烦恼，轻松部署"
date: 2024-08-19 14:37:22
draft: false
ShowToc: true
TocOpen: true
tags:
  - Docker
categories:
  - DevOps
---
### x86环境
#### Docker安装nacos并使用默认的Derby数据库
- 拉取Docker镜像
```shell
docker pull nacos/nacos-server
```
- 创建本地的映射文件custom.properties
```shell
mkdir -p /root/nacos/init.d /root/nacos/logs
touch /root/nacos/init.d/custom.properties
# 在custom.properties中写入以下配置
management.endpoints.web.exposure.include=*
```
- 创建容器并启动
```shell
# docker run启动
docker run -d -p 8848:8848 -e MODE=standalone -e PREFER_HOST_MODE=hostname -v /root/nacos/init.d/custom.properties:/home/nacos/init.d/custom.properties -v /root/nacos/logs:/home/nacos/logs --restart always --name nacos nacos/nacos-server
# docker-compose启动
# 首先配置docker-compose文件 standalone-derby.yaml
version: "2"
services:
  nacos:
    image: nacos/nacos-server:latest
    container_name: nacos
    environment:
    - MODE=standalone
    volumes:
    - /root/nacos/logs:/home/nacos/logs
    -  /root/nacos/init.d/custom.properties:/home/nacos/init.d/custom.properties
    ports:
    - "8848:8848"
#启动
docker-compose -f standalone-derby.yaml up
#关闭
docker-compose -f standalone-derby.yaml stop
#移除
docker-compose -f standalone-derby.yaml rm
#关闭并移除
docker-compose -f standalone-derby.yaml down
```
- 访问http://localhost:8848/nacos/ 默认账号密码nacos/nacos
#### Docker安装nacos并使用Mysql数据库
- 拉取Docker镜像
```shell
docker pull nacos/nacos-server
```
- 创建本地的映射文件custom.properties
```shell
mkdir -p /root/nacos/init.d /root/nacos/logs
touch /root/nacos/init.d/custom.properties
# 在custom.properties中写入以下配置
management.endpoints.web.exposure.include=*
```
- 创建数据库nacos_config
```sql
create database nacos_config;
```
- 使用sql脚本恢复数据库，恢复脚本参考https://github.com/alibaba/nacos/blob/master/config/src/main/resources/META-INF/nacos-db.sql
[【附件】nacos-db.zip](/media/attachment/2023/12/nacos-db.zip)
- 启动容器(注意修改mysql相关配置)
```shell
docker run -d -p 8848:8848 -e MODE=standalone -e PREFER_HOST_MODE=hostname -e SPRING_DATASOURCE_PLATFORM=mysql -e MYSQL_SERVICE_HOST=127.0.0.1 -e MYSQL_SERVICE_PORT=3306 -e MYSQL_SERVICE_DB_NAME=nacos_config -e MYSQL_SERVICE_USER=root -e MYSQL_SERVICE_PASSWORD=root -e MYSQL_DATABASE_NUM=1 -v /root/nacos/init.d/custom.properties:/home/nacos/init.d/custom.properties -v /root/nacos/logs:/home/nacos/logs --restart always --name nacos nacos/nacos-server
```
- 访问http://localhost:8848/nacos/ 默认账号密码nacos/nacos

### arm环境
#### Docker运行nacos并使用默认的Derby数据库
- 创建Dockerfile
```text
FROM arm64v8/centos:7
MAINTAINER Nissan
ADD jdk-18.0.2.1_linux-aarch64_bin.tar.gz /jdk/
COPY fonts/* /usr/share/fonts/chinese/
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime  && yum install dejavu-sans-fonts mkfontscale fontconfig -y && yum clean all && cd /usr/share/fonts/chinese && mkfontscale && mkfontdir && fc-cache -fv && mkdir -p /data/engine
ENV JAVA_HOME=/jdk/jdk-18.0.2.1
ENV CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV PATH=$JAVA_HOME/bin:$PATH
ENV LANG en_US.UTF-8
COPY ./nacos /root/nacos
WORKDIR /root/nacos
EXPOSE 8848
ENV MODE=standalone
ENV SPRING_DATASOURCE_PLATFORM=derby
ENTRYPOINT ["java","-Dnacos.standalone=true","-jar","target/nacos-server.jar"]
#ENTRYPOINT ["yum","update"]
```
1. jdk-18.0.2.1_linux-aarch64_bin.tar.gz需要到java官网下载
https://download.oracle.com/java/18/archive/jdk-18.0.2.1_linux-aarch64_bin.tar.gz
2. fonts字体包可以直接从windows系统获取：C:\Windows\Fonts
3. nacos包为arm架构包，可以从github获取
https://github.com/alibaba/nacos
- 打包镜像
```shell
docker build -t nacos_arm .
```
- 上传镜像部署，映射出8848、9848、9849端口即可