import ssl
import json
import requests
import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
class Awvs():
    def __init__(self):
        # 禁用安全请求警告
        requests.packages.urllib3.disable_warnings (InsecureRequestWarning)
        # localhost:3443全部替换为awvs所在的服务器及端口
        username = '*****@qq.com'
        pw = 'd4e1da01c3dccb90ff55977d0c998a15f193de849df8aeeec67b7b8537815d68'
        # sha256加密后的密码，通过burp抓包可获取,也可以使用(http://tool.oschina.net/encrypt?type=2)把密码进行加密之后填入，请区分大小写、中英文字符。
        # 以上内容为配置内容，然后把要添加的url列表保存成testawvs.txt文件，放在该脚本下运行该脚本。
        # url_login = "https://localhost:3443/api/v1/me/login"
        send_headers_login = {
            'Host': 'localhost:3443',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8'
        }
        data_login = '{"email":"' + username + '","password":"' + pw + '","remember_me":false}'
        response_login = requests.post (url="https://localhost:3443/api/v1/me/login", headers=send_headers_login,
                                        data=data_login, verify=False)
        xauth = response_login.headers['X-Auth']
        COOOOOOOOkie = response_login.headers['Set-Cookie']
        print("当前验证信息如下\r\n cookie : {}  \r\n X-Auth : {}  ".format (COOOOOOOOkie, xauth))
        send_headers2 = {
            'Host': 'localhost:3443',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Auth': xauth,
            'Cookie': COOOOOOOOkie
        }
        # 以上代码实现登录（获取cookie）和校验值
        self.xauth = xauth
        self.COOOOOOOOkie = COOOOOOOOkie
        self.send_headers2 = send_headers2

    def add_exec_scan(self,target):
        print('function start')
        url = "https://localhost:3443/api/v1/targets"
        try:
            target_url = 'http://' + target.replace ('http://', '').replace ('', '').strip ()
            data = '{"description":"222","address":"' + target_url + '","criticality":"10"}'
            response = requests.post(url=url, headers=self.send_headers2, data=data, verify=False)
            target_id = json.loads(response.text)['target_id']  # 获取添加后的任务ID
            # 以上代码实现批量添加
            url_scan = "https://localhost:3443/api/v1/scans"
            headers_scan = {
                'Host': 'localhost:3443',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json;charset=utf-8',
                'X-Auth': self.xauth,
                'Cookie': self.COOOOOOOOkie,
            }
            requests.patch(url='https://localhost:3443/api/v1/targets/%s/configuration' % str (target_id),
                            headers=headers_scan, data={"scan_speed": "sequential"}, verify=False)
            data_scan = '{"target_id":' + '\"' + target_id + '\"' + ',"profile_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"66666666666666666666666666666666"}'
            response_scan = requests.post (url=url_scan, headers=headers_scan, data=data_scan, verify=False)
            print(response_scan.text + "添加成功！")
        # 以上代码实现批量加入扫描
        except Exception as e:
            print(e)

    def count(self):
        response_count = requests.get(url='https://localhost:3443/api/v1/notifications/count',headers=self.send_headers2,verify=False)
        print("当前存在%r个通知！" % json.loads(response_count.text)['count'])
        print("-" * 50)
        print("已存在以下任务")
        response_info = requests.get(url='https://localhost:3443/api/v1/scans',headers=self.send_headers2,verify=False)
        all_info = json.loads(response_info.text)
        num = 0
        for website in all_info.get("scans"):
            num += 1
            print(website.get("target").get("address") + " \r\n target_id:" + website.get("scan_id"))
        print("共%r个扫描任务" % num)

    def del_scan(self):
        response_info = requests.get(url='https://localhost:3443/api/v1/scans',headers=self.send_headers2,verify=False)
        all_info = json.loads(response_info.text)
        counter = 0
        for website in all_info.get("scans"):
            url_scan_del = "https://localhost:3443/api/v1/scans/" + str(website.get("scan_id"))
            req_del = urllib.Request(url_scan_del, headers=self.send_headers2)
            req_del.get_method = lambda: 'DELETE'
            response_del = urllib2.urlopen(req_del)
            counter = counter + 1
            print("已经删除第%r个!" % counter)

    def del_targets(self):
        url_info = "https://localhost:3443/api/v1/targets"
        req_info = urllib2.Request(url_info, headers=self.send_headers2)
        response_info = urllib2.urlopen(req_info)
        all_info = json.loads(response_info.read())
        for website in all_info.get("targets"):
            if (website.get("description")) == "222":
                url_scan_del = "https://localhost:3443/api/v1/targets/" + str(website.get ("target_id"))
                req_del = urllib2.Request(url_scan_del, headers=self.send_headers2)
                req_del.get_method = lambda: 'DELETE'
                response_del = urllib2.urlopen(req_del)
                print("ok!")
    def notice(self):
        print("**" * 20)
        print("1、添加扫描任务并执行请输入1，然后回车\r\n2、删除所有使用该脚本添加的任务请输入2，然后回车\r\n3、删除所有任务请输入3，然后回车\r\n4、查看已存在任务请输入4，然后回车\r\n")
        choice = str (input(">"))
        #self.add_exec_scan()
        if choice == "1":
            f = open('testawvs.txt','r')
            for i in f:
                self.add_exec_scan(i)
            f.close()
            self.count()
        elif choice == "2":
            self.del_targets()
            self.count()
        elif choice == "3":
            self.del_scan()
            self.count ()
        elif choice == "4":
            self.count ()
        else:
            print("请重新运行并请输入1、2、3、4选择。")

awvs = Awvs()
awvs.notice()
