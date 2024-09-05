---
author: "Hakuna"
title: 内网证书服务器搭建（mkcert）
slug: localnetwork_https
description: "内网实现https"
summary: ""
date: 2024-09-05 15:45:06
draft: false
ShowToc: true
TocOpen: true
tags:
  - mkcert
  - python
categories:
  - DevOps
---
> 使用mkcert工具实现，github地址：https://github.com/FiloSottile/mkcert

### 安装mkcert工具
以Ubuntu系统为例
先到github下载对应版本的release：`mkcert-v1.4.4-linux-amd64`
将mkcert上传至服务器
```shell
# 授予可执行权限
chmod +x mkcert-v1.4.4-linux-amd64
# 将mkcert移动至系统目录
mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert
# 可能需要安装依赖
sudo apt install libnss3-tools
# 使用命令验证mkcert可以正常运行，此命令输出结果为默认根证书生成路径
mkcert -CAROOT
```

### 生成根证书
```shell
# 根证书默认生成路径为 ~/.local/share/mkcert
mkcert -install
```

### 根据内网IP地址生成ssl证书
```shell
# 生成ip地址为192.168.10.2的证书
mkcert 192.168.10.2
# 当前目录下会生成两个文件：192.168.10.2-key.pem，192.168.10.2.pem
```

### 使用python+flask搭建接口服务器
主要提供两个接口：
- 下载根证书：http://<服务器ip>:5000/download-root-cert
- 通过ip获取ssl证书：http://<服务器ip>:5000/get-cert?ip=192.168.1.1（用实际的 IP 地址替换）
```python
from flask import Flask, send_file, request, jsonify
import os
import subprocess
import tempfile

app = Flask(__name__)

# 根证书路径
ROOT_CA_CERT = os.path.expanduser('./rootCA.pem')
# 提前使用mkcert生成本服务器的ssl证书
LOCAL_CERT_PATH = '192.168.10.2.pem'
LOCAL_KEY_PATH = '192.168.10.2-key.pem'

# 临时目录用于存储生成的证书
CERT_DIR = tempfile.mkdtemp()

@app.route('/download-root-cert', methods=['GET'])
def download_root_cert():
    """下载根证书"""
    if not os.path.exists(ROOT_CA_CERT):
        return jsonify({'error': 'Root CA certificate not found'}), 404
    
    return send_file(ROOT_CA_CERT, as_attachment=True)

@app.route('/get-cert', methods=['GET'])
def get_cert():
    """根据内网 IP 地址请求证书及私钥"""
    ip_address = request.args.get('ip')
    if not ip_address:
        return jsonify({'error': 'IP address is required'}), 400

    # 生成证书文件和私钥文件的路径
    cert_path = os.path.join(CERT_DIR, f'{ip_address}.pem')
    key_path = os.path.join(CERT_DIR, f'{ip_address}-key.pem')

    try:
        # 使用 mkcert 生成证书和私钥
        subprocess.run(
          ['mkcert', '-key-file', key_path, '-cert-file', cert_path, ip_address], 
          check=True)

        # 创建一个包含证书和私钥的压缩包
        zip_path = os.path.join(CERT_DIR, f'{ip_address}.zip')
        subprocess.run(['zip', '-j', zip_path, cert_path, key_path], check=True)

        # 发送压缩包文件
        response = send_file(zip_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error generating certificate: {e}'}), 500

    finally:
        # 删除生成的证书和私钥文件
        if os.path.exists(cert_path):
            os.remove(cert_path)
        if os.path.exists(key_path):
            os.remove(key_path)
        if os.path.exists(zip_path):
            os.remove(zip_path)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=(LOCAL_CERT_PATH, LOCAL_KEY_PATH))

```

### mkcert证书有效期修改
> 使用官方的mkcert默认只会生成两年加三个月的证书，可以通过修改官方的代码，然后重新打包来修改证书的有效期
```go
// 修改文件为cert.go
···
	// Certificates last for 2 years and 3 months, which is always less than
	// 825 days, the limit that macOS/iOS apply to all certificates,
	// including custom roots. See https://support.apple.com/en-us/HT210176.
	expiration := time.Now().AddDate(2, 3, 0)
···
```
将此文件中的`AddDate(2, 3, 0)`修改为想要的年月即可，其中`2`代表两年，`3`代表三月。
