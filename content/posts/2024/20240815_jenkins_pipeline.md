---
author: "Hakuna"
title: 记一次Jenkins配置pipeline任务流程
slug: 
description: ""
date: 2024-08-15 13:38:13
draft: false
ShowToc: true
TocOpen: true
tags:
  - Jenkins
categories:
  - DevOps
---
## Jenkins实现代码自动化测试、构建、上传
* 源代码为Java开发，构建成品为jar包及对应sources包

### 新建流水线任务（Pipeline）

    新建任务->流水线

### 编写流水线脚本

#### 指定脚本中需要使用的工具
* 需要在部署Jenkins的机器中安装，本脚本中使用的是maven和jdk。

```shell
tools {
		//前面为工具名，后面为Jenkins中配置的具体名称，可以在系统管理->全局工具配置中查看
        maven "maven_3.8.4"
        jdk "jdk11"
      }
```

#### 拉取git源代码

```shell
// Git pull 为自定义名称，可以自己配置
stage('Git pull'){
            steps{
                //此处branch即指定分支，credentialsId为git凭据id，可以在系统管理->Manage Credentials中配置后得到。
                git branch: 'dev', credentialsId: '2caf8590-ce9d-4317-a6a4-7153b872eb58',url:  'https://你的项目.git'
			}
            
        }
```

#### 使用Junit进行单元测试
* 需要先在Jenkins中安装Junit插件，以及pom文件修改（详情见文末）

```shell
// Junit 为自定义名称，可以自己配置
stage('Junit'){
			steps{
			    //执行测试命令
				sh "mvn clean test"
				
			}
			post{
				success{
					//获取测试结果文件
					junit 'target/surefire-reports/*.xml'
				}
			}
		}
```

#### 使用Jacoco进行代码覆盖率测试
* 需要先在Jenkins中安装Jacoco插件，以及拷贝[jacocoagent.jar]到自定义目录、pom文件修改（详情见文末）

```shell
stage('Jacoco'){
            steps{
				//调用jacocoagent.jar进行测试，其中jacocoagent.jar包路径需自行修改
                sh "mvn clean deploy -U -DargLine=-javaagent:/home/jacocoagent.jar -Dmaven.test.failure.ignore=true -Dmaven.test.skip=false"
				//读取生成的测试文件
                jacoco()
            }
        }
```

#### 项目构建

```shell
stage('Build') {
            steps {
				//此处打包代码需咨询开发自行修改
                sh "mvn package -DskipTests"
                sh "mvn dependency:copy-dependencies -DoutputDirectory=target/lib"
                sh "mvn source:jar"
            }
            post {
                success {
					//构建成功归档
                    archiveArtifacts 'target/*.jar' 
                }
            }
        }
```

#### 项目文件上传
* 先在Jenkins中安装NexusArtifactUploader插件

##### 环境变量配置

```shell
environment {
		//你的nexus版本
        NEXUS_VERSION = "nexus2"
		//你的nexus协议(http/https)
        NEXUS_PROTOCOL = "http"
        NEXUS_URL = "你的nexus地址"
        NEXUS_REPOSITORY = "你的REPOSITORY名称"
		//你的nexus凭据id，配置方法参考git凭据
        NEXUS_CREDENTIAL_ID = "373c4e8a-83db-4025-933e-a29b052e088c"
    }
```

##### Jar包上传脚本
```shell
stage('Upload nexus'){
			steps {
                script {
					//读取项目根目录pom.xml文件
                    pom = readMavenPom file: "pom.xml";
                        nexusArtifactUploader(
                            nexusVersion: NEXUS_VERSION,
                            protocol: NEXUS_PROTOCOL,
                            nexusUrl: NEXUS_URL,
                            groupId: pom.groupId,
                            version: pom.version,
                            repository: NEXUS_REPOSITORY,
                            credentialsId: NEXUS_CREDENTIAL_ID,
							//此处提交了两个jar包，另一个为source jar包
                            artifacts: [
                                [artifactId: pom.artifactId,
                                classifier: '',
								//默认不用修改，除非开发配置不在此路径
                                file: "target/${pom.artifactId}-${pom.version}.${pom.packaging}",
                                type: pom.packaging],
                                [artifactId: pom.artifactId,
								//如需提交source jar包，需要此处指定'sources'
                                classifier: 'sources',
                                file: "target/${pom.artifactId}-${pom.version}-sources.${pom.packaging}",
                                type: pom.packaging]
                                ])
                }
            }
		}
```

#### 清空工作区
* 构建完成后清空（可选）

```shell
stage('Clean workspace') {
	steps{
			deleteDir()
		 }
	}
}
```

---

### 完整流水线代码（Pipeline script）

```shell
pipeline {
    agent any
	
	environment {
        NEXUS_VERSION = "nexus2"
        NEXUS_PROTOCOL = "http"
        NEXUS_URL = "***"
        NEXUS_REPOSITORY = "***"
        NEXUS_CREDENTIAL_ID = "373c4e8a-83db-4025-933e-a29b052e088c"
    }
	
    tools {
        maven "maven_3.8.4"
        jdk "jdk11"
    }

    stages {
        stage('Git pull'){
            steps{
                
                git branch: 'dev', credentialsId: '2caf8590-ce9d-4317-a6a4-7153b872eb58',url:  'https://***.git'
            }
            
        }

		stage('Junit'){
			steps{
				sh "mvn clean test"
			}
			post{
				success{
					junit 'target/surefire-reports/*.xml'
				}
			}
		}
		
        stage('Jacoco'){
            steps{
                sh "mvn clean deploy -U -DargLine=-javaagent:/home/jacocoagent.jar -Dmaven.test.failure.ignore=true -Dmaven.test.skip=false"
                jacoco()
            }
        }
        stage('Build') {
            steps {
                sh "mvn package -DskipTests"
                sh "mvn dependency:copy-dependencies -DoutputDirectory=target/lib"
                sh "mvn source:jar"
            }
            post {
                success {
                    archiveArtifacts 'target/*.jar'
                }
            }
        }
		       

		stage('Upload nexus'){
			steps {
                script {
                    pom = readMavenPom file: "pom.xml";
                        nexusArtifactUploader(
                            nexusVersion: NEXUS_VERSION,
                            protocol: NEXUS_PROTOCOL,
                            nexusUrl: NEXUS_URL,
                            groupId: pom.groupId,
                            version: pom.version,
                            repository: NEXUS_REPOSITORY,
                            credentialsId: NEXUS_CREDENTIAL_ID,
                            artifacts: [
                                [artifactId: pom.artifactId,
                                classifier: '',
                                file: "target/${pom.artifactId}-${pom.version}.${pom.packaging}",
                                type: pom.packaging],
                                [artifactId: pom.artifactId,
                                classifier: 'sources',
                                file: "target/${pom.artifactId}-${pom.version}-sources.${pom.packaging}",
                                type: pom.packaging]
                                ])
                }
            }
		}
		

		stage('Clean workspace') {
			steps{
					deleteDir()
				 }
			}
		}
        
    

}

```




---
#### 关于Junit单元测试，开发人员需修改pom.xml，增加如下片段，同事根据增加片段中的内容命名测试类
```xml
<plugin>
		<groupId>org.apache.maven.plugins</groupId>
		<artifactId>maven-surefire-plugin</artifactId>
		<configuration>
				<!--表示执行任何子目录下所有命名以Test结尾的java类 -->
				<includes>
						<include>**/*Testor.java</include>
				</includes>
				<!--表示不执行任何子目录下所有命名以Test开头的java类 -->
				<excludes>
						<exclude>**/Test.java</exclude>
				</excludes>
		</configuration>
</plugin>
```

#### 关于Jacoco代码覆盖率测试，开发人员需修改pom.xml，增加如下片段
```xml
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-deploy-plugin</artifactId>
	<version>2.8.2</version>
	<configuration>
		<skip>true</skip>
	</configuration>
</plugin>
```
