---
author: "Hakuna"
title: 简单爬个小说
slug: spider_novel
description: ""
summary: "一怒之下一怒爬下了"
date: 2024-08-15 13:42:53
draft: false
ShowToc: true
TocOpen: true
tags:
  - Python
categories:
  - Interest
---
## 目标：爬取古龙书屋的小说
`代码实现：下载每个页面的txt，合并成一整本小说`

### 根据网页URL，获取小说页面的链接组成
```markdown
https://m.gulongsw.com/xs_968/938982.html
其中：
    https://m.gulongsw.com 为主站URL
    /xs_968 为小说目录
    /938982.html 为小说章节页面
```

### 使用BeautifulSoup模块解析小说页面

#### 获取下一章链接
```html
<div class="pager"><a href="/xs_968/936604.html">上一章</a> <a href="/xs_968/">目 录</a> <a href="/xs_968/939514.html">下一章</a> <a id="mark">存书签</a> </div>
```
编写对应python代码
```python
def next_page(soup):
    pager = soup.find(name='div', attrs={'class': 'pager'})
    for a in pager.findAll(name='a'):
        if a.string == '下一章':
            return str(a['href'])
```

#### 获取小说正文内容
```html
<div class="content">中的p标签
```
编写对应python代码
```python
def download_page(soup):
    head = '【' + str(soup.h1.string) + '】' + '\n'  # 章节名
    paragraph.append(head)
    content_text = soup.find(name='div', attrs={'class': 'content'})
    for i in content_text.findAll(name='p'):
        paragraph.append(str(i.string) + '\n')
    paragraph.append('\n\n\n\n')
```

### 避免站点封禁IP，使用代理池
```python
def UserAgent_random():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 '
        'Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
        'Safari/537.36']
 
    UserAgent = {'User-Agent': random.choice(user_agent_list)}
    return UserAgent
```

### 保存所有章节至TXT文档
```python
with open('novel.txt', 'a', encoding='utf-8') as f:
            for p in paragraph:
                f.write(p)
            f.close()
```
----------

### 完整代码
```python
import random
import requests
import time
from bs4 import BeautifulSoup
 
 
def UserAgent_random():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 '
        'Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
        'Safari/537.36']
 
    UserAgent = {'User-Agent': random.choice(user_agent_list)}
    return UserAgent
 
 
def next_page(soup):
    pager = soup.find(name='div', attrs={'class': 'pager'})
    for a in pager.findAll(name='a'):
        if a.string == '下一章':
            return str(a['href'])
 
 
def download_page(soup):
    head = '【' + str(soup.h1.string) + '】' + '\n'  # 章节名
    paragraph.append(head)
    content_text = soup.find(name='div', attrs={'class': 'content'})
    for i in content_text.findAll(name='p'):
        paragraph.append(str(i.string) + '\n')
    paragraph.append('\n\n\n\n')

if __name__ == '__main__':
    url = 'https://m.gulongsw.com'
    url_r = '/xs_968/938982.html'
    # final_url = '/xs_968/1008623.html'
 
    from requests.adapters import HTTPAdapter
 
     
    while url_r != '/xs_968/':
        paragraph = []
        UserAgent = UserAgent_random()
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            real_html = s.get(url + url_r, headers=UserAgent, timeout=5).text
        except requests.exceptions.RequestException as e:
            print(e)
        soup = BeautifulSoup(real_html, 'html.parser')
        download_page(soup)
        url_r = next_page(soup)
        with open('novel.txt', 'a', encoding='utf-8') as f:
            for p in paragraph:
                f.write(p)
            f.close()
```