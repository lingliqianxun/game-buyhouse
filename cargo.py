import random

class Cargo:
    data = [
        {'name':'转基因大豆', 'code':'beans', 'min':6, 'max':50},
        {'name':'防毒面具', 'code':'mask', 'min':40, 'max':480},
        {'name':'奶粉', 'code':'milk', 'min':100, 'max':500},
        {'name':'黄金', 'code':'gold', 'min':220, 'max':1880},
        {'name':'手机', 'code':'phone', 'min':999, 'max':8800},
        {'name':'电脑', 'code':'computer', 'min':2300, 'max':12000},
        {'name':'摩托车', 'code':'moterbike', 'min':4800, 'max':22000},
        {'name':'汽车', 'code':'car', 'min':20000, 'max':120000},
    ]
    
    def GetName(self, code):
        for d in self.data:
            if(d['code']==code):
                return d['name']
        return ''

    def Random(self, cargos):
        for d in random.sample(self.data, 5):
            price_cur = random.randrange(d['min'], d['max'])
            dic = {'code':d['code'], 'price_cur':price_cur}
            cargos.append(dic)
