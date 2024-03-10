# NJUPT-AutoLogin

由于2023年暑假南邮更新了校园网认证系统，把原来的POST方式改成了GET，还引入了HTTPS，以前的登录脚本需要大改，于是有了这个项目。

【测试环境】
- OS: Windows10
- Python 3.8.10 (Anaconda3)
- httpx 0.24.1

## ❤准备工作

本项目使用了Python第三方库`httpx`，用来支持HTTP/2的请求。使用以下控制台命令下载：

```
pip install httpx
```
```
pip install httpx[http2]
```

注：`requests`库不支持HTTP/2，所以用的`httpx`，但是我看到其他人的项目用`requests`库也行？

然后把源码下载到电脑里

## ➡修改代码

用记事本或其他文本编辑器打开源码，在`USERNAME`和`PASSWD`后面的双引号中间填写对应信息，并修改`SEL`后面的数字选择运营商，如下方代码块所示。
```python
#定义登录时需要用的变量
USERNAME = "BXXXXXXXX"      #用户名
PASSWD = "💅💅💅💅💅💅"    #密码
SEL = 1     #0-校园网；1-中国电信；2-中国移动
```

## 🧱cmd.exe，启动！

在与源码同一目录下，新建一个文本文档，将后缀改成`.bat`，复制下面的代码并保存，你也可以自行修改😘：

```
@ECHO OFF
chcp 65001
title NJUPT校园网登录
python ./NJUPT-AutoLogin.py
pause
EXIT
```
