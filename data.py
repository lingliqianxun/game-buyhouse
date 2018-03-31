from encry import *
from process import PROCESS_NAME

#####数据#####

class Person():
    #全局数据
    cash_interest = 0.01
    alimoney_interest = 0.05
    week = 0
    weather = '晴天'

    #个人数据
    money = 3000
    cash = 0
    alimoney = 0
    health = 100
    hope = 80
    cargo_cur = 0
    cargo_max = 100

    #出租屋货物数据
    room_cargos = [
        {'code':'null', 'price_buy':'', 'num':''},
    ]

    def RoomCargosGetNum(self, code):
        for c in self.room_cargos:
            if(c['code'] == code):
                return c['num']
        return 0
        
    def RoomCargosSetNum(self, code, num):
        for c in self.room_cargos:
            if(c['code'] == code):
                c['num'] = num
        return 0
        

    #市场货物数据
    market_cargos = [
        {'code':'null', 'price_cur':''},
    ]

    def MarketCargosGetPriceCur(self, code):
        for c in self.market_cargos:
            if(c['code'] == code):
                return c['price_cur']
        return 0
        
    #售楼部房屋数据
    buildings  = [
        {'name':'单身公寓','m':30,'price':40},
        {'name':'二手旧房','m':80,'price':120},
        {'name':'高档小区','m':108,'price':180},
        {'name':'豪华住宅','m':180,'price':300},
        {'name':'湖景别墅','m':320,'price':600},
        {'name':'泳池私宅','m':450,'price':1200},
        {'name':'一栋小区','m':1512,'price':2500},
        {'name':'一个楼盘','m':24192,'price':4000},
    ]
    building_house = []

    #成就数据
    archive_person = []
    archives = [
        {'code':'million', 'descript':'成为百万富翁'},
        {'code':'ten_million', 'descript':'成为千万富翁'},
        {'code':'hundred_million', 'descript':'成为亿万富翁'},
        {'code':'million_cash', 'descript':'银行存款100万'},
        {'code':'million_alimoney', 'descript':'余X宝存款100万'},
        {'code':'one_house', 'descript':'拥有一所房屋'},
        {'code':'big_house', 'descript':'拥有一所豪宅'},
        {'code':'hundred_agency', 'descript':'购买租房100个'},
        {'code':'one_year', 'descript':'度过1年(52周)'},
        {'code':'three_year', 'descript':'度过3年(156周)'},
        {'code':'hope_full', 'descript':'声望出名'},
    ]

    def ArchiveGetDescript(self, code):
        for a in self.archives:
            if a['code'] == code:
                return a['descript']
        return ''

    def GetData(self):
        file_name = PROCESS_NAME + ".data"
        try:
            file = open(file_name,'r',encoding='utf-8') 
        except:
            return
        conts_encry = file.read()
        conts = Decry(conts_encry)
        if conts:
            data = eval(conts)
            self.week = data['week']
            self.weather = data['weather']
            self.money = data['money']
            self.cash = data['cash']
            self.alimoney = data['alimoney']
            self.health = data['health']
            self.hope = data['hope']
            self.cargo_cur = data['cargo_min']
            self.cargo_max = data['cargo_max']
            self.room_cargos = data['room_cargos']
            self.market_cargos = data['market_cargos']
            self.building_house = data['building_house']
            self.archive_person = data['archive_person']

        file.close()

    def SaveData(self):
        file_name = PROCESS_NAME + ".data"
        file = open(file_name,'w',encoding='utf-8') 
        data = {}
        data['week'] = self.week 
        data['weather'] = self.weather
        data['money'] = self.money
        data['cash'] = self.cash
        data['alimoney'] = self.alimoney
        data['health'] = self.health
        data['hope'] = self.hope
        data['cargo_min'] = self.cargo_cur
        data['cargo_max'] = self.cargo_max
        data['room_cargos'] = self.room_cargos
        data['market_cargos'] = self.market_cargos
        data['building_house'] = self.building_house
        data['archive_person'] = self.archive_person

        conts = str(data)
        conts_encry = Encry(conts)
        file.write(conts_encry)
        file.close()


