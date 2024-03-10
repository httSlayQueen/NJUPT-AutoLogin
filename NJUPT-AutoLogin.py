import subprocess as sp
import httpx, os, re, json

#定义登录时需要用的变量
USERNAME = ""      #用户名
PASSWD = ""    #密码
SEL = 0     #0-校园网；1-中国电信；2-中国移动

#运营商代号，不要修改
ISP = ["", "@njxy", "@cmcc"]

class LoginBot():
    """
    处理登录事件的类
    """
    #各个地址
    URLs = {
        "init": "https://p.njupt.edu.cn/a79.htm",                       #登录页面
        "check": "",                                                    #登录状态查询页面
        "login": "https://p.njupt.edu.cn:802/eportal/portal/login",    #登录信息发送地址
    }
    #网页参数
    params = {
        "callback": "dr1003",
        "login_method": "1",
        "user_account": ",0,",
        "user_password": "",
        "wlan_user_ip": "",
        "wlan_user_ipv6": "",
        "wlan_user_mac": "000000000000",
        "wlan_ac_ip": "",
        "wlan_ac_name": "",
    }
    #请求头
    header = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        "Connection": "keep-alive",
        "Host": "p.njupt.edu.cn:802",
    }

    def __init__(self):
        with httpx.Client(headers=self.header) as client:
            try:
                #获得页面信息
                r = client.get(url=self.URLs["init"], timeout=1)
            except:
                print("无法访问登录地址，请检查是否连接到校园网！")
            else:
                self.params["wlan_user_ip"] = re.search(R"v46ip='(.+)'", r.text).group(1)   #获取客户端IP
                self.params["user_account"] = self.params["user_account"] + USERNAME + ISP[SEL] #写入账户
                self.params["user_password"] = PASSWD   #写入密码
                #计算十进制IP，用于查询登录状态
                ip_list = list(map(int, self.params["wlan_user_ip"].split(".")))
                ip_dec = str(ip_list[0] << 24 | ip_list[1] << 16 | ip_list[2] << 8 | ip_list[3] >> 0)
                self.URLs["check"] = f"https://p.njupt.edu.cn:802/eportal/portal/online_list?callback=dr1002&user_account=&user_password=&wlan_user_mac=000000000000&wlan_user_ip={ip_dec}&curr_user_ip={ip_dec}"
                print("登录信息初始化成功！")

    def Login(self):
        #查询登录状态
        r = httpx.get(self.URLs["check"])
        res = json.loads(re.search(R"\((.*?)\);", r.text).group(1))

        if int(res["result"]) == 0:
            self.__OnLogin()
        elif int(res["result"]) == 1:
            print("已登录到校园网，请不要重复登录！")
        else:
            os.system("pause")
            os._exit(1)

    def __OnLogin(self):
        #启用HTTP/2.0
        with httpx.Client(headers=self.header, http2=False) as client:
            try:
                #尝试登录
                r = client.get(url=self.URLs["login"], params=self.params, headers=self.header)
            except:
                print("登录失败！")
            else:
                #打印结果
                res = json.loads(re.search(R"\((.*?)\);", r.text).group(1))
                if int(res["result"]) == 1:
                    print("登录成功！{0}".format(res["msg"]))
                else:
                    print("登录失败！{0}".format(res["msg"]))


def checkNet():
    """
    判断网络是否链接
    """
    ret = sp.run(R"ping 1.2.4.8 -n 2", shell=True, stdout=sp.PIPE, stdin=sp.PIPE,stderr=sp.PIPE)
    return True if ret.returncode==0 else False


if __name__ == '__main__':
    if checkNet():
        print("已连接到互联网，尽情冲浪！")
    else:
        bot = LoginBot()
        bot.Login()

    os.system("pause")
    os._exit(0)
