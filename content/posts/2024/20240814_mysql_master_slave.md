---
author: "Hakuna"
title: Mysql主备部署(基于Binlog)
slug: sql_master_slave
description: ""
date: 2024-08-14 16:34:10
draft: false
ShowToc: true
TocOpen: true
tags:
  - Mysql
categories:
  - DevOps
---
### 部署环境情况

#### Mysql安装
```bash
# 192.168.2.10 主服务器，Ubuntu20
# 192.168.2.11 备服务器，Ubuntu18
# 主备服务器分别使用以下命令安装mysql
apt update
apt install mysql-server
# 初始化Msql，按提示操作，具体可以参考文末说明。
mysql_secure_installation

```

#### Msql升级
```bash
# 开始以为安装的mysql版本一致，结果Ubuntu20安装的为Mysql8，Ubuntu18安装的为Mysql5.6，后面配置同步导致字符集不一致出错，故添加Ubuntu18升级Mysql版本方法如下
# 下载Mysql的apt源
wget https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb
# 如果在Ubuntu18下运行此命令出现"https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb: Scheme missing.",是因为wget命令没有配置到系统变量无法直接使用，可以用下面命令执行
/usr/bin/wget https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb

# 安装源
dpkg -i mysql-apt-config_0.8.22-1_all.deb

# 在configuring mysql-apt-config中通过方向键和Enter选择MySQL Server & Cluster (Currently selected: mysql-8.0),然后选择Ok，在密码强度界面按自己意愿选择。安装时出现"*** mysqld.cnf (Y/I/N/O/D/Z) [default=N] ?"，可以输入Y保留当前配置文件。

# 升级Mysql
apt update
apt install mysql-server

# 最后可以登录Mysql查看版本
```

#### 非root用户登录Msql报错处理
```bash
# 附遇到的另一个问题，非root用户登录Mysql提示"Access denied for user '用户名'@'localhost'",主要是因为在Ubuntu上安装MySQL时，对于root用户，可以设置空密码。
# 通过以下命令修改数据库root密码，再退出数据库命令行，即可使用普通系统用户登录。
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';

# 此处修改密码时，如果在之前选择的是强密码，可能会报错密码强度不足，需要使用大小写字母+数字+符号形式的密码！

```

### 配置主从同步

#### 主库配置（192.168.2.10）

##### 停止Mysql服务
```bash
systemctl stop mysql
```
##### 修改Mysql配置
```bash
nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
在\[mysqld\]下添加
```bash
# 设置服务id，主从不能一致
server-id=1
# 开启binlog
log-bin=mysql-bin
# 设置需要同步的数据库
binlog-do-db=test1
```
##### 启动Mysql
```bash
systemctl start mysql
```
##### 登录数据库，创建主备复制专用账号
此处命令中的"192.168.2.11"为备库地址,如使用现有账号进行主备复制，则可以忽略创建步骤，"BY"后的密码可以自行指定。
```sql
CREATE USER 'sync_test'@'192.168.2.11' IDENTIFIED WITH mysql_native_password BY 'sync_test';
```
授予账号访问权限，sync_test为上一步创建账号,如上一步未创建，可替换为现有账号。
```sql
GRANT REPLICATION SLAVE ON *.* TO 'sync_test'@'192.168.2.11';
```
刷新权限
```sql
FLUSH PRIVILEGES;
```
记录日志文件名及位点(File和Position)
```sql
show master status;
```

#### 从库配置（192.168.2.11）

##### 停止Mysql服务
```bash
systemctl stop mysql
```
##### 修改Mysql配置
```bash
nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
在\[mysqld\]下添加
```bash
# 设置服务id，主从不能一致
server-id=2
# 开启binlog
log-bin=mysql-bin
# 设置需要同步的数据库
replicate_wild_do_table=test1.%
```
##### 启动Mysql
```bash
systemctl start mysql
```
##### 登录数据库，配置同步
停止同步
```sql
stop slave;
```
配置指向主库，其中master_host为主库地址，master_user、master_password为主备复制专用账号，master_log_file为主库查询到的日志文件名，master_log_pos为主库查询到的位点
```sql
CHANGE MASTER TO master_host='192.168.2.10', master_user='sync_test', master_password='sync_test', master_log_file='mysql-bin.000002',master_log_pos=157;
```
启动同步
```sql
start slave;
```
查看同步状态，如果Slave_IO_Running及Slave_SQL_Running均显示为YES，则同步成功，可以往主库插入一条数据看从库是否也同时插入了一条，若没有，再次使用以下命令查看是否有报错需要处理！
```sql
show slave status\G
```

### 配置互为主从
将以上主从颠倒再次配置一次即可。
注：Mysql配置文件只需添加相关配置，无需删除内容，防止之前配置的主从失效！





----------

```bash
mysql_secure_installation 交互说明

Enter current password for root (enter for none):<–初次运行直接回车

Set root password? [Y/n] <– 是否设置root用户密码，输入y并回车或直接回车
New password: <– 设置root用户的密码
Re-enter new password: <– 再输入一次你设置的密码

Remove anonymous users? [Y/n] <– 是否删除匿名用户,生产环境建议删除，所以直接回车

Disallow root login remotely? [Y/n] <–是否禁止root远程登录,根据自己的需求选择Y/n并回车,建议禁止

Remove test database and access to it? [Y/n] <– 是否删除test数据库,直接回车

Reload privilege tables now? [Y/n] <– 是否重新加载权限表，直接回车
```
