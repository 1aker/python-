# coding:utf-8
import gevent
from gevent import monkey;monkey.patch_all()
import requests
import queue
urls = []
filters = []
all = ''
queue = queue.Queue()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
f = open('testawvs.txt','r',encoding='utf-8')# 这里代表另一个电脑跑出的所有url防止两电脑采集到了相同的url

def test(url):
    try:
        global all
        #print('test:', url)
        res = requests.get(url='http://'+url,headers=headers,timeout=3)
        if res.status_code == 200 and len(res.text) > 5:
            print('http://' + url)
            all = all + url + '\n'
    except Exception as e:
        pass

for i in f.readlines():
    i = i.strip().replace('\r\n', '').replace('\n', '')
    if i not in urls:
        print(i)
        if len(i) > 27:
            i = i.split(' ')[0]
        urls.append(i)
        all = all + i + '\n'

'''
g_list = []
while urls != []:
    for i in range(1000):
        if urls !=[]:
            try:
                temp = urls[i]
                g = gevent.spawn(test, temp)
                g_list.append(g)
                urls.remove(temp)
            except:
                break
    gevent.joinall(g_list)

f.close()
'''
f = open('testawvs.txt', 'w+', encoding='utf-8')# 这里代表另一个电脑跑出的所有url防止两电脑采集到了相同的url
for i in all.split('\n'):
    f.write(i+'\n')
f.close()

# 将输出复制到目录txt就好
print('Successfully')
