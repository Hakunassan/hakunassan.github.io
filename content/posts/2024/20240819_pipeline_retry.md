---
author: "Hakuna"
title: Pipeline添加重试构建操作
slug: pipeline_retry
description: ""
summary: "多试试，万一成了呢"
date: 2024-08-19 11:17:05
draft: false
ShowToc: true
TocOpen: true
tags:
  - Jenkins
categories:
  - DevOps
---

```groovy
pipeline { 
    agent any 
    stages { 
        stage('Build') { 
            steps { 
                //重试构建三次，通过修改‘3’来修改需要重试的次数
                retry(3) { 
                  //此处编辑需要重试构建的步骤
                  sh 'make' 
                } 
            } 
        } 
    } 
}
```