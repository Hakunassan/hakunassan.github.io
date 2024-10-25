---
author: "Hakuna"
title: OpenGaussDB单机部署实践
slug: opengaussdb_installation
description: ""
summary: "按照官方教程来，还是会有坎坎坷坷"
date: 2024-10-24 15:01:22
draft: false
ShowToc: true
TocOpen: true
tags:
  - OpenGauss
categories:
  - DevOps
---
> 参考官方部署文档：https://docs-opengauss.osinfra.cn/zh/docs/6.0.0/docs/InstallationGuide/%E4%B8%80%E7%AB%99%E5%BC%8F%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97.html
> 
> 下载地址：https://opengauss.org/zh/download/

### 前提条件（官方）
- 所有服务器操作系统和网络均正常运行。
- 用户必须有数据库包解压路径、安装路径的读、写和执行操作权限，并且安装路径必须为空。
- 用户对下载的openGauss压缩包有执行权限。
- 如果使用中文界面来安装，需要检查当前本地字符集是否支持中文(如:zh_CN.UTF-8)

### 前提条件（个人补充）
- 官方没有说需要python，且需要3.10及以下的版本，3.11不支持。
- 不要使用root用户目录进行安装，否则后面无法给新建用户授予目录权限。
- 需要提前安装linux基础开发编辑包等依赖
- 本文使用的安装包为：**openGauss_6.0.0 企业版**
- 本文安装环境为：**单机版无CM**

### 安装基础依赖包
```shell
# 如果后续安装还有缺少依赖的情况，那就继续安装，此处只列出本次实践部署机器缺少的包
sudo yum groupinstall "Development Tools" -y && \ 
sudo yum install gcc zlib-devel bzip2-devel ncurses-devel -y && \
sudo yum install libffi-devel readline-devel openssl-devel sqlite-devel -y
```

### 安装Python3.10
```shell
# 卸载3.11版本或者安装python版本管理工具（推荐此方案，因为后面还会缺少python3.7的lib包）
# 此处演示使用pyenv管理工具的方案

# pyenv安装需要使用git
yum install git
# 安装pyenv
curl https://pyenv.run | bash
# 设置环境变量
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
# 安装执行版本Python
pyenv install 3.10.4
# 使用pyenv设置全局Python版本
pyenv global 3.11.4
```

### 根据官网步骤，执行预安装
```shell
# 注意修改tar包名
tar -zxvf openGauss-All-6.0.0-openEuler20.03-aarch64.tar -C targetDir
cd targetDir
tar -zxvf openGauss-OM-6.0.0-openEuler20.03-aarch64.tar.gz -C omDir
# 添加一步,复制server包到omDir下
cp openGauss-Server* omDir/
cd omDir/script
# 添加一步，安装Python3.7，拷贝lib包到/usr/lib或/usr/lib64（根据实际情况来）
# lib包名为libpython3.7m.so.1.0
pyenv install 3.7
cp ~/.pyenv/versions/3.7.17/lib/libpython3.7m.so.1.0 /usr/lib64/
# 此处根据文字提示选择安装需求，完成预安装
./gs_preinstall -U omm -G dbgroup --one-stop-install

```

### 根据官网步骤，安装
```shell
su - omm
# 此处xml文件路径为上一步预安装时打印出来的路径
gs_install -X /opt/software/openGauss/cluster_config.xml
```

### 验证
```shell
su - omm
# 执行如下命令检查数据库状态是否正常，“cluster_state ”显示“Normal”表示数据库可正常使用
gs_om -t status
# 数据库安装完成后，默认生成名称为postgres的数据库。第一次连接数据库时可以连接到此数据库
# 端口号为预安装时指定的，默认为15000
gsql -d postgres -p 15000
# 连接成功后，系统显示类似如下信息表示数据库连接成功。
gsql ((openGauss x.x.x build 290d125f) compiled at 2021-03-08 02:59:43 commit 2143 last mr 131
Non-SSL connection (SSL connection is recommended when requiring high-security)
Type "help" for help.
```

### 配置远程连接
```shell
# 参照postgresql修改postgresql.conf、pg_hba.conf
# 重启数据库
gs_om -t restart
```