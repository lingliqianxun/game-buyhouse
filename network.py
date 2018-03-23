import urllib.request
import urllib.parse
from urllib.error import URLError,HTTPError


def Http(url, data=None):
    headers={}
    if data:
        data = urllib.parse.urlencode(data).encode('utf-8')

    request = urllib.request.Request(url=url, data=data, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except HTTPError as e:
        return e.code,e.msg
    except URLError:
        return -1,"无法连接"
           
    status = response.status
    results = response.read().decode('utf-8')
    return status,results

def HttpFile(url):
    headers={}
    request = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except URLError:
        return -1,"无法连接"
           
    status = 200
    results = response.read()
    return status,results


#测试用
def TestHttp():
    url = "http://www.baidu.com"
    data = {"user.oprid":11,"a":1}
    s,r = Http(url, data)
    print(s)
    print(r)
    while(1):
        pass
    
def TestHttpFile():
    url = "file:///C:/Users/admin/Desktop/python/game-buyhouse/version.txt"
    s,r = HttpFile(url)
    print(s)
    print(r)
    f=open('hellow.txt','bw')
    f.write(r)
    f.close()
    while(1):
        pass
    
#TestHttp()
#TestHttpFile()
