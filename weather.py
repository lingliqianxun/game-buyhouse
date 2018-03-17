import random
import time

class Weather:
    data = [
        {'name':'晴天','child':[
            {'name':'晴天','rate':500},
            {'name':'多云','rate':200},
            {'name':'阴天','rate':100},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':88},
            {'name':'雨加雪','rate':1},
            {'name':'小雪','rate':1},
        ]},
        {'name':'多云','child':[
            {'name':'晴天','rate':300},
            {'name':'多云','rate':300},
            {'name':'阴天','rate':200},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':88},
            {'name':'雨加雪','rate':1},
            {'name':'小雪','rate':1},
        ]},
        {'name':'阴天','child':[
            {'name':'晴天','rate':200},
            {'name':'多云','rate':200},
            {'name':'阴天','rate':200},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':200},
            {'name':'小雨','rate':170},
            {'name':'雨加雪','rate':10},
            {'name':'小雪','rate':10},
        ]},
        {'name':'雾','child':[
            {'name':'晴天','rate':300},
            {'name':'多云','rate':300},
            {'name':'阴天','rate':200},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':88},
            {'name':'雨加雪','rate':1},
            {'name':'小雪','rate':1},
        ]},
        {'name':'雷阵雨','child':[
            {'name':'晴天','rate':100},
            {'name':'多云','rate':150},
            {'name':'阴天','rate':150},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':200},
            {'name':'小雨','rate':270},
            {'name':'中雨','rate':100},
            {'name':'雨加雪','rate':10},
            {'name':'小雪','rate':10},
        ]},
        {'name':'小雨','child':[
            {'name':'晴天','rate':100},
            {'name':'多云','rate':100},
            {'name':'阴天','rate':200},
            {'name':'雾','rate':10},
            {'name':'雷阵雨','rate':200},
            {'name':'小雨','rate':170},
            {'name':'中雨','rate':200},
            {'name':'雨加雪','rate':10},
            {'name':'小雪','rate':10},
        ]},
        {'name':'中雨','child':[
            {'name':'晴天','rate':100},
            {'name':'多云','rate':100},
            {'name':'阴天','rate':100},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':100},
            {'name':'中雨','rate':200},
            {'name':'大雨','rate':200},
            {'name':'暴雨','rate':100},
        ]},
        {'name':'大雨','child':[
            {'name':'晴天','rate':50},
            {'name':'多云','rate':50},
            {'name':'阴天','rate':100},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':100},
            {'name':'中雨','rate':200},
            {'name':'大雨','rate':200},
            {'name':'暴雨','rate':200},
        ]},
        {'name':'暴雨','child':[
            {'name':'晴天','rate':50},
            {'name':'多云','rate':50},
            {'name':'阴天','rate':100},
            {'name':'雷阵雨','rate':100},
            {'name':'小雨','rate':100},
            {'name':'中雨','rate':200},
            {'name':'大雨','rate':200},
            {'name':'暴雨','rate':200},
        ]},
        {'name':'雨加雪','child':[
            {'name':'晴天','rate':100},
            {'name':'多云','rate':100},
            {'name':'阴天','rate':100},
            {'name':'小雨','rate':200},
            {'name':'雨加雪','rate':200},
            {'name':'小雪','rate':200},
            {'name':'中雪','rate':100},
        ]},
        {'name':'小雪','child':[
            {'name':'晴天','rate':100},
            {'name':'多云','rate':100},
            {'name':'阴天','rate':100},
            {'name':'小雨','rate':50},
            {'name':'雨加雪','rate':100},
            {'name':'小雪','rate':250},
            {'name':'中雪','rate':300},
        ]},
        {'name':'中雪','child':[
            {'name':'晴天','rate':50},
            {'name':'多云','rate':50},
            {'name':'阴天','rate':50},
            {'name':'小雪','rate':250},
            {'name':'中雪','rate':300},
            {'name':'大雪','rate':200},
            {'name':'暴雪','rate':100}, 
        ]},
        {'name':'大雪','child':[
            {'name':'晴天','rate':50},
            {'name':'多云','rate':50},
            {'name':'阴天','rate':50},
            {'name':'小雪','rate':150},
            {'name':'中雪','rate':300},
            {'name':'大雪','rate':300},
            {'name':'暴雪','rate':100}, 
        ]},
        {'name':'暴雪','child':[
            {'name':'晴天','rate':50},
            {'name':'多云','rate':50},
            {'name':'阴天','rate':50},
            {'name':'小雪','rate':150},
            {'name':'中雪','rate':200},
            {'name':'大雪','rate':300},
            {'name':'暴雪','rate':200}, 
        ]},
    ]

    def GetChild(self, name):
        for d in self.data:
            if d['name'] == name:
                return d['child']
        return None
            
    #随机天气
    def Random(self, name):
        weather_all = []
        for c in self.GetChild(name):
            for i in range(0,c['rate']):
                weather_all.append(c['name'])
        return random.sample(weather_all,1)[0]


def Test():
    w = Weather().Random('晴天')
    while(1):
        w = Weather().Random(w)
        print(w)
        time.sleep(1)
#测试用
#Test()
