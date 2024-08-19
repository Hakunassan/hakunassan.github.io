---
author: "Hakuna"
title: pipeline并行构建
slug: 
description: ""
summary: "用并行构建，享畅快人生（注意机器性能，别把jenkins整宕了）"
date: 2024-08-19 11:24:30
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
        //添加并行构建stage
        stage('Parallel Steps') {
            parallel {
              //此处添加需要并行构建的多个stage
              stage('Build Backend') { 
                  ...
              } 
              stage('Build Front') { 
                  ...
              } 
              stage('Build android-app') { 
                  ...
              } 
              stage('Build ios-app') { 
                  ...
              } 
            }
        }
    } 
}
```