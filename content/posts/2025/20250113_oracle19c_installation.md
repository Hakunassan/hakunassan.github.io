---
author: "Hakuna"
title: Oracle19c单机版静默部署及升级
slug: oracle19c_installation
description: ""
summary: "Linux下安装oracle19c，并且升级补丁集到19.12.0.0.0"
date: 2025-01-13 16:32:46
draft: false
ShowToc: true
TocOpen: true
tags:
  - Oracle
categories:
  - Devops
---

***！！！服务器最好使用Redhat/Centos，如果一定要用Ubuntu的话，可能会有很多缺少库的问题需要处理，相当棘手！！！***

> 需要使用到的安装包：
> ----19c安装包：LINUX.X64_193000_db_home.zip
> ----opatch更新包：p6880880_190000_Linux-x86-64.zip
> ----19.12补丁集：p32904851_190000_Linux-x86-64.zip

### 一、系统基础配置
#### 1、创建用户和用户组
```shell
# 创建oinstall和dba用户组
groupadd oinstall
groupadd dba

# 创建Oracle用户
useradd -g oinstall -G dba oracle

# 设置Oracle用户密码
passwd oracle

# 查看用户
id oracle

注意：这里查出来的uid必须是oracle，gid必须是oinstall，组必须是dba
```
#### 2、修改系统配置文件
```shell
cat >>/etc/sysctl.conf<<'EOF'
fs.aio-max-nr=1048576
fs.file-max=6815744
kernel.shmall=524288
kernel.shmmax=2147483647
kernel.sem=250 32000 100 128
kernel.shmmni=4096
kernel.panic_on_oops=1
net.core.rmem_default=262144
net.core.rmem_max=4194304
net.core.wmem_default=262144
net.core.wmem_max=1048576
net.ipv4.conf.all.rp_filter=2
net.ipv4.conf.default.rp_filter=2
fs.aio-max-nr=1048576
net.ipv4.ip_local_port_range=9000 65500
EOF

sysctl -p



cat >>/etc/security/limits.conf<<'EOF'
oracle soft nproc 2047
oracle hard nproc 16384
oracle soft nofile 1024
oracle hard nofile 65536
oracle soft stack 10240
oracle hard stack 10240
EOF


cat >>/etc/pam.d/login<<'EOF'
session    required     /lib64/security/pam_limits.so
session    required     pam_limits.so
EOF



cat >>/etc/profile<<'EOF'
if [ $USER = "oracle" ]; then
    if [ $SHELL = "/bin/ksh" ]; then
        ulimit -p 16384 ulimit -n 65536
    else
        ulimit -u 16384 -n 65536
    fi
fi
EOF


source /etc/profile
```
#### 3、 创建数据库目录
```shell
mkdir -p /data/server/oracle
chown -R oracle:oinstall /data/server/oracle
chmod -R 775 /data/server/oracle
```
#### 4、配置Oracle用户
```shell
su - oracle
vim ~/.bash_profile
export ORACLE_BASE=/data/server/oracle
export ORACLE_SID=orcl

source ~/.bash_profile
```
### 二、安装部署及配置
#### 1、上传安装包
```shell
mkdir -p /data/file/oracle
chown -R oracle:oinstall /data/file/oracle
chmod -R 775 /data/file/oracle

上传安装包到 /data/file/oracle 目录下
```
#### 2、解压文件
```shell
su - oracle
cd /data/file/oracle/
unzip LINUX.X64_193000_db_home.zip
```
#### 3、编辑文件内容
```shell
# 切换oracle用户
su - oracle
cd /data/file/oracle/install/response/
mv db_install.rsp  db_install.rsp.bak

cat>db_install.rsp<<'EOF'
oracle.install.responseFileVersion=/oracle/install/rspfmt_dbinstall_response_schema_v19.0.0
# 响应文件版本号

oracle.install.option=INSTALL_DB_SWONLY
# 安装选项为仅安装数据库软件

UNIX_GROUP_NAME=oinstall
# UNIX 组名为 oinstall

INVENTORY_LOCATION=/data/server/oracle/oraInventory
# Oracle 软件 Inventory（库存）位置

ORACLE_HOME=/data/file/oracle
# Oracle 软件安装目录

ORACLE_BASE=/data/server/oracle
# Oracle 软件基础目录

oracle.install.db.InstallEdition=EE
# 安装的 Oracle 版本为 Enterprise Edition

oracle.install.db.OSDBA_GROUP=dba
# OSDBA 组名为 dba

oracle.install.db.OSOPER_GROUP=oinstall
# OSOPER 组名为 oinstall

oracle.install.db.OSBACKUPDBA_GROUP=oinstall
# OSBACKUPDBA 组名为 oinstall

oracle.install.db.OSDGDBA_GROUP=oinstall
# OSDGDBA 组名为 oinstall

oracle.install.db.OSKMDBA_GROUP=oinstall
# OSKMDBA 组名为 oinstall

oracle.install.db.OSRACDBA_GROUP=oinstall
# OSRACDBA 组名为 oinstall

oracle.install.db.rootconfig.executeRootScript=false
# 执行 root 脚本为 false

oracle.install.db.rootconfig.configMethod=
# 配置方法为空

oracle.install.db.rootconfig.sudoPath=
# sudo 路径为空

oracle.install.db.rootconfig.sudoUserName=
# sudo 用户名为空

oracle.install.db.CLUSTER_NODES=
# 集群节点为空

oracle.install.db.config.starterdb.type=GENERAL_PURPOSE
# Starter 数据库类型为 GENERAL_PURPOSE

oracle.install.db.config.starterdb.globalDBName=ocrl
# Starter 数据库全局名称为 ocrl

oracle.install.db.config.starterdb.SID=ocrl
# Starter 数据库 SID 为 ocrl

oracle.install.db.ConfigureAsContainerDB=
# 配置为 Container Database 为空

oracle.install.db.config.PDBName=
# PDB 名称为空

oracle.install.db.config.starterdb.characterSet=
# 字符集为空

oracle.install.db.config.starterdb.memoryOption=
# 内存选项为空

oracle.install.db.config.starterdb.memoryLimit=81920
# 内存限制为81920

oracle.install.db.config.starterdb.installExampleSchemas=
# 安装示例模式为空

oracle.install.db.config.starterdb.password.ALL=oracle
# 所有密码为oracle

oracle.install.db.config.starterdb.password.SYS=
# SYS 密码为空

oracle.install.db.config.starterdb.password.SYSTEM=
# SYSTEM 密码为空

oracle.install.db.config.starterdb.password.DBSNMP=
# DBSNMP 密码为空

oracle.install.db.config.starterdb.password.PDBADMIN=
# PDBADMIN 密码为空

oracle.install.db.config.starterdb.managementOption=
# 管理选项为空

oracle.install.db.config.starterdb.omsHost=
# omsHost 为空

oracle.install.db.config.starterdb.omsPort=
# omsPort 为空

oracle.install.db.config.starterdb.emAdminUser=
# emAdminUser 为空

oracle.install.db.config.starterdb.emAdminPassword=
# emAdminPassword 为空

oracle.install.db.config.starterdb.enableRecovery=
# 启用恢复为空

oracle.install.db.config.starterdb.storageType=
# 存储类型为空

oracle.install.db.config.starterdb.fileSystemStorage.dataLocation=
# 文件系统存储数据位置为空

oracle.install.db.config.starterdb.fileSystemStorage.recoveryLocation=
# 文件系统存储恢复位置为空

oracle.install.db.config.asm.diskGroup=
# ASM 磁盘组为空

oracle.install.db.config.asm.ASMSNMPPassword=
# ASM SNMP 密码为空
EOF
```
#### 4、开始安装
```shell
# 安装依赖
yum install libnsl

# 伪装为Redhat系统，Oracle默认不支持centos和kylin
export CV_ASSUME_DISTID=RHEL7.6

执行db_install.rsp文件

cd /data/file/oracle
./runInstaller -silent -responseFile  /data/file/oracle/install/response/db_install.rsp
```
安装成功截图：
![](/images/posts/2024/20240827_binlog_restore/image.png)
```shell
#切换到root用户执行
/data/server/oracle/oraInventory/orainstRoot.sh
/data/file/oracle/root.sh
```
执行成功截图：
![](/images/posts/2024/20240827_binlog_restore/image2.png)

#### 5、配置oracle用户
```shell
su - oracle

vim .bash_profile
export ORACLE_HOME=/data/file/oracle
export ORACLE_BASE=/data/server/oracle
export ORACLE_SID=orcl
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib
export PATH=$PATH:$ORACLE_HOME/bin
export LANG="zh_CN.UTF-8"
export NLS_LANG="SIMPLIFIED CHINESE_CHINA.AL32UTF8"
export NLS_DATE_FORMAT='yyyy-mm-dd hh24:mi:ss'

source .bash_profile
```
#### 6、配置监听
```shell
netca /silent /responsefile  /data/file/oracle/assistants/netca/netca.rsp
```
#### 7、启动监听
```shell
lsnrctl start
```
#### 8、修改静默建库文件
```shell
cd  /data/file/oracle/assistants/dbca/

cp dbca.rsp  dbca.rsp.bak

cat >dbca.rsp<<'EOF'
responseFileVersion=/oracle/assistants/rspfmt_dbca_response_schema_v19.0.0
# 响应文件版本号
gdbName=orcl
# 数据库全局名称为空
sid=orcl
# 数据库 SID 为orcl
databaseConfigType=SI
# 数据库配置类型为空
RACOneNodeServiceName=
# RAC One Node 服务名称为空
policyManaged=
# 策略管理为空
createServerPool=
# 创建服务器池为空
serverPoolName=
# 服务器池名称为空
cardinality=
# 配置数量为空
force=
# 强制为空
pqPoolName=
# pqPoolName 为空
pqCardinality=
# pqCardinality 为空
createAsContainerDatabase=true
# 创建为 Container Database 为空
numberOfPDBs=1
# PDB 数量为空
pdbName=orclpdb
# PDB 名称为空
useLocalUndoForPDBs=
# 为 PDB 使用本地撤消为空
pdbAdminPassword=
# PDB 管理员密码为空
nodelist=
# 节点列表为空
templateName=/data/file/oracle/assistants/dbca/templates/General_Purpose.dbc
# 模板名称为空
sysPassword=
# SYS 密码为空
systemPassword=
# SYSTEM 密码为空
oracleHomeUserPassword=
# Oracle Home 用户密码为空
emConfiguration=
# EM 配置为空
emExpressPort=5500
# EM Express 端口为 5500
runCVUChecks=
# 运行 CVU 检查为空
dbsnmpPassword=
# DBSNMP 密码为空
omsHost=
# omsHost 为空
omsPort=0
# omsPort 为空
emUser=
# EM 用户为空
emPassword=
# EM 密码为空
dvConfiguration=
# DV 配置为空
dvUserName=
# DV 用户名为空
dvUserPassword=
# DV 用户密码为空
dvAccountManagerName=
# DV 账户管理员名称为空
dvAccountManagerPassword=
# DV 账户管理员密码为空
olsConfiguration=
# OLS 配置为空
datafileJarLocation=
# 数据文件 JAR 位置为空
datafileDestination=
# 数据文件目标位置为空
recoveryAreaDestination=
# 恢复区域目标位置为空
storageType=
# 存储类型为空
diskGroupName=
# 磁盘组名称为空
asmsnmpPassword=
# ASMSNMP 密码为空
recoveryGroupName=
# 恢复组名称为空
characterSet=AL32UTF8
# 字符集为空
nationalCharacterSet=
# 国家字符集为空
registerWithDirService=
# 注册到目录服务为空
dirServiceUserName=
# 目录服务用户名为空
dirServicePassword=
# 目录服务密码为空
walletPassword=
# 钱包密码为空
listeners=LISTENER
# 监听器为空
variablesFile=
# 变量文件为空
variables=
# 变量为空
initParams=
# 初始化参数为空
sampleSchema=
# 示例模式为空
memoryPercentage=40
# 内存百分比为空
databaseType=
# 数据库类型为空
automaticMemoryManagement=false
# 自动内存管理为空
totalMemory=0
# 总内存为空
EOF



执行静默建库操作
dbca -silent -createDatabase  -responseFile  /data/file/oracle/assistants/dbca/dbca.rsp
```
![](/images/posts/2024/20240827_binlog_restore/image3.png)
![](/images/posts/2024/20240827_binlog_restore/image4.png)
#### 9、数据库启停及监听启停命令
```shell
# 启动数据库实例
su - oracle
[oracle@centos ~]$ sqlplus / as sysdba

SQL*Plus: Release 19.0.0.0.0 - Production on 星期六 3月 16 20:44:57 2024
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

已连接到空闲例程。

SQL> startup
ORACLE 例程已经启动。

Total System Global Area  905968496 bytes
Fixed Size            9141104 bytes
Variable Size          239075328 bytes
Database Buffers      650117120 bytes
Redo Buffers            7634944 bytes
数据库装载完毕。
数据库已经打开。
SQL> exit
从 Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0 断开

# 启动数据库监听
[oracle@centos ~]$ lsnrctl  start

LSNRCTL for Linux: Version 19.0.0.0.0 - Production on 16-3月 -2024 20:45:38

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

启动/data/file/oracle/bin/tnslsnr: 请稍候...

TNSLSNR for Linux: Version 19.0.0.0.0 - Production
系统参数文件为/data/file/oracle/network/admin/listener.ora
写入/data/server/oracle/diag/tnslsnr/oracle-1/listener/alert/log.xml的日志信息
监听: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=192.168.100.50)(PORT=1521)))
监听: (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))

正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.100.50)(PORT=1521)))
LISTENER 的 STATUS
------------------------
别名                      LISTENER
版本                      TNSLSNR for Linux: Version 19.0.0.0.0 - Production
启动日期                  16-3月 -2024 20:45:38
正常运行时间              0 天 0 小时 0 分 0 秒
跟踪级别                  off
安全性                    ON: Local OS Authentication
SNMP                      OFF
监听程序参数文件          /data/file/oracle/network/admin/listener.ora
监听程序日志文件          /data/server/oracle/diag/tnslsnr/oracle-1/listener/alert/log.xml
监听端点概要...
  (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=192.168.100.50)(PORT=1521)))
  (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
监听程序不支持服务
命令执行成功

# 关闭实例
[oracle@centos ~]$ sqlplus / as sysdba

SQL*Plus: Release 19.0.0.0.0 - Production on 星期六 3月 16 20:40:11 2024
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.


连接到: 
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。

# 关闭监听
[oracle@centos ~]$ lsnrctl stop

LSNRCTL for Linux: Version 19.0.0.0.0 - Production on 16-3月 -2024 20:42:28

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

正在连接到 (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.100.50)(PORT=1521)))
命令执行成功
```
### 三、补丁库升级
#### 1、升级检查
```shell
# 确认数据库版本号及列出已应用补丁
[oracle@centos ~]$ sqlplus -v

SQL*Plus: Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

[oracle@centos ~]$ cd $ORACLE_HOME
[oracle@centos oracle]$ cd OPatch/
[oracle@centos OPatch]$ ./opatch lspatches

29585399;OCW RELEASE UPDATE 19.3.0.0.0 (29585399)
29517242;Database Release Update : 19.3.0.0.190416 (29517242)

# 确认Opatch版本
[oracle@centos ~]$ $ORACLE_HOME/OPatch/opatch version

OPatch Version: 12.2.0.1.17
OPatch succeeded.
```
#### 2、升级Opatch
```shell
# 上传opatch更新包到/opt下
[root@centos ~]# cd /opt
[root@centos opt]# chown oracle:oinstall p6880880_190000_Linux-x86-64.zip
[root@centos opt]# chmod 755 p6880880_190000_Linux-x86-64.zip
[root@centos opt]# su - oralce
[oracle@centos ~]$ cd $ORACLE_HOME
[oracle@centos oracle]$ mv OPatch/ OPatchbak
[oracle@centos oracle]$ unzip /opt/p6880880_190000_Linux-x86-64.zip -d $ORACLE_HOME
[oracle@centos oracle]$ $ORACLE_HOME/OPatch/opatch version

OPatch Version: 12.2.0.1.36
OPatch succeeded.

# 验证Oracle Inventory
[oracle@centos ~]$ $ORACLE_HOME/OPatch/opatch lsinventory -detail -oh $ORACLE_HOME
```
#### 3、检查补丁冲突
```shell
# 上传19.12补丁集到/opt下
[root@centos ~]# cd /opt
[root@centos opt]# unzip p32904851_190000_Linux-x86-64.zip
[root@centos opt]# chown -R oracle:oinstall 32904851
[root@centos opt]# chmod -R 755 32904851
[root@centos ~]# su - oracle
[oracle@centos ~]$ cd /opt/32904851/
[oracle@centos 32904851]$ $ORACLE_HOME/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
```
#### 4、自动补丁安装
```shell
# 关闭数据库监听
[oracle@centos ~]$ lsnrctl stop
# 关闭数据库
[oracle@centos ~]$ sqlplus / as sysdba

SQL*Plus: Release 19.0.0.0.0 - Production on 星期六 3月 16 20:40:11 2024
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.


连接到: 
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

SQL> shutdown immediate
数据库已经关闭。
已经卸载数据库。
ORACLE 例程已经关闭。
[oracle@centos ~]$ cd /opt/32904851/
[oracle@centos 32904851]$ $ORACLE_HOME/OPatch/opatch apply

```
#### 5、检查补丁
```shell
# 检查输出是否正确
[oracle@centos ~]$ $ORACLE_HOME/OPatch/opatch lspatches

32904851;Database Release Update : 19.12.0.0.210720 (32904851)
29585399;OCW RELEASE UPDATE 19.3.0.0.0 (29585399)
OPatch succeeded.

[oracle@centos ~]$ sqlplus -version

SQL*Plus: Release 19.0.0.0.0 - Production
Version 19.12.0.0.0
```