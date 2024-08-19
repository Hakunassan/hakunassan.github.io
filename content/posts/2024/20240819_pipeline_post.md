---
author: "Hakuna"
title: Pipeline添加无论成功失败都触发的操作
slug: 
description: ""
summary: "像系统装了还原卡一样！"
date: 2024-08-19 11:20:05
draft: false
ShowToc: true
TocOpen: true
tags:
  - Jenkins
categories:
  - DevOps
---
`通过添加always这个步骤，清理工作目录，防止下次构建时因为历史文件存在导致构建失败`
```groovy
pipeline { 
    agent any 
    stages { 
        stage('Build') { 
            ...
        } 
    } 
    
    post { 
        //添加总是要执行的步骤
        always { 
            //清空工作目录
            cleanWs() 
        } 
    } 
}
```