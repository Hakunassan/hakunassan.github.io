---
author: "Hakuna"
title: Shadowsocks的PAC模式问题
slug: shadowsocks_solution
description: ""
summary: "解决shadowsocks开启PAC模式后无法访问内网问题"
date: 2024-11-28 11:39:14
draft: false
ShowToc: true
TocOpen: true
tags:
  - Vpn
categories:
  - Shadowsocks
---
- 起因：内网vpn与shadowsocks同时开启后，无法访问到内网，但是保持同时只有一个vpn在线又影响效率
自行修改pac.txt文件无果后，开始各种搜索，找到以下两种方案：
1.修改user-rule.txt，添加相关配置
> user-rule.txt 说明
> 一行只能有一条代理规则
> 注释使用 ! ，例如 !test
> 添加@@开头表示不走代理，否则就走代理
> 要让user-rule生效，需要更新本地的PAC
```txt
@@||内网域名
@@||内网ip
```
2.根据官方issue修改配置
  退出SS，使用Windows自带的记事本打开 Shadowsocks.exe 所在目录下的 gui-config.json 文件，然后将文件中的  "geositePreferDirect": false, 修改为 "geositePreferDirect": true, 保存退出后删除同目录下的 pac.txt 文件，再启动SS并更新PAC。
  配置截图：![](/images/posts/2024/20241128_shadowsocks_solution/shadowsocks.png)