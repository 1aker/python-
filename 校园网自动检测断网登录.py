#coding:utf-8
import requests
import re
import time
import os
import subprocess
import sys


while True:
    res = os.popen('ping www.baidu.com -l 1 -n 1')
    res = subprocess.Popen ('ping www.baidu.com -l 1 -n 1', shell=True, stdout=subprocess.PIPE)
    sys.stdout.flush()
    temp = res.stdout.read()
    #print(temp)
    if re.findall('= \d\dms',temp) != []:
        print('Having connected')
        time.sleep(5)
    else:
        while True:
            try:
                user = '5120151943'
                passwd = '117564'
                headers = {
                    'Host': 'portal.swust.edu.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3315.4 Safari/537.36'
                }
                session = requests.session()
                res = session.get(url='http://portal.swust.edu.cn',headers=headers)

                # print(res)
                # print(res.cookies.get_dict())
                # print(res.headers)

                url = re.findall(r"href='(.*?)'</script>", res.text)[0]
                res = session.get(url=url, headers=headers)
                proxies = {'http':'http://127.0.0.1:8080'}
                headers = {
                    'Host': 'portal.swust.edu.cn',
                    'Proxy-Connection': 'keep-alive',
                    'Origin': 'http://portal.swust.edu.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3315.4 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': '*/*',
                    'Referer': '%s' % url,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9'
                }
                cookies = {
                    'EPORTAL_COOKIE_OPERATORPWD':'',
                    'EPORTAL_COOKIE_SERVER_NAME':'%E6%A0%A1%E5%9B%AD%E7%BD%91',
                    'EPORTAL_AUTO_LAND':'',
                    'EPORTAL_COOKIE_SERVER':'swust',
                    'EPORTAL_COOKIE_PASSWORD':'%s' % passwd,
                    'EPORTAL_COOKIE_DOMAIN':'false',
                    'EPORTAL_COOKIE_USERNAME':'%s' % user,
                    'EPORTAL_USER_GROUP':'root',
                    'JSESSIONID':'E0185A7F11739BC650E22F1C9E3F2014'

                }

                data = {
                    'userId':'%s' % user,
                    'password':'%s' % passwd,
                    'service':'swust',
                    'queryString':'%s' % url.replace('http://portal.swust.edu.cn/eportal/index.jsp?',''),
                    'operatorPwd':'',
                    'operatorUserId':'',
                    'validcode':''
                }

                res = session.post(url='http://portal.swust.edu.cn/eportal/InterFace.do?method=login',cookies=cookies,headers=headers,data=data)

                headers_get = {
                'Host': 'portal.swust.edu.cn',
                'Proxy-Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3315.4 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://portal.swust.edu.cn/eportal/index.jsp?wlanuserip=064a017ace30493f28a9092a454bd761&wlanacname=041fbe0577187ffe56d9d5222e67a8a1&ssid=&nasip=0a5271c1a59d0122af12918c228e9c41&snmpagentip=&mac=ccf56b459be2198f624c88d5d4f20a7f&t=wireless-v2&url=f908f599425d7ed7e805a331fa69312208298d74f4136d6c8dc6cc88f6c335dba51a61c922bf6587&apmac=&nasid=041fbe0577187ffe56d9d5222e67a8a1&vid=4004e5a2fc9d4440&port=0cf37389a6e5ddc7&nasportid=6c6b3ad8d8b22015d2ea1ed80640c9e6b59ae3577c6cdc82bb40c60b6269b682',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9'
                }
                res = session.get(url='http://portal.swust.edu.cn/eportal/success.jsp?userIndex=30613532373163316135396430313232616631323931386332323865396334315f31302e31302e342e3139345f35313230313430343932&keepaliveInterval=0',cookies=cookies,headers=headers_get)
                print('[+] Reconnected')
                time.sleep(20)
                break
            except Exception as e:
                break
