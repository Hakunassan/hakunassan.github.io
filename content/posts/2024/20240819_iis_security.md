---
author: "Hakuna"
title: IIS漏洞修复记录
slug: 
description: ""
summary: "修复记录汇总，不定时更新"
date: 2024-08-19 14:57:48
draft: false
ShowToc: true
TocOpen: true
tags:
  - IIS
categories:
  - DevOps
---
#### 技术信息泄露漏洞 (CVSSv3: 中危)
漏洞截图：![](/images/posts/2024/20240819_iis_security/20240819151447.png)
处理方式： 隐藏IIS版本号等标识信息  
**修改web.config会即时生效，谨慎操作生产环境！必须安装IIS URL重写模块，不然会导致IIS页面503，切记！！！**

- 隐藏Server信息  
下载对应版本[URL Rewirte](http://www.iis.net/downloads/microsoft/url-rewrite)进行安装
```config
<!--在web.config的system.webServer节点下添加以下内容-->
      <rewrite> 
        <outboundRules> 
          <rule name="REMOVE_RESPONSE_SERVER"> 
            <match serverVariable="RESPONSE_SERVER" pattern=".*" /> 
            <action type="Rewrite" /> 
          </rule> 
        </outboundRules> 
      </rewrite> 
```
- 隐藏x-powered-by信息
```config
<!--在web.config的system.webServer节点下添加以下内容，如果customHeaders节点已存在，直接在节点中添加即可-->
  <customHeaders>
    <remove name="X-Powered-By" />
  </customHeaders>
```

- 隐藏X-AspNet-Version信息 
下载[iis_stripheaders_module_1.0.5.msi](https://github.com/dionach/StripHeaders/releases/tag/v1.0.5)进行安装
```cmd
cd C:\Windows\System32\inetsrv
# 加载模块
appcmd.exe install module /name:StripHeadersModule /image:%windir%\system32\inetsrv\stripheaders.dll /add:true /lock:true
# 卸载模块
appcmd.exe uninstall module "StripHeadersModule"
```
操作成功后，X-AspNet-Version信息会自动隐藏