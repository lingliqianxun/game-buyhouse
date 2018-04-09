#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import random
import threading
import os
import sys

import tkinter as tk  
from tkinter import ttk  
from tkinter import scrolledtext  
from tkinter import Menu  
from tkinter import Spinbox  
from tkinter import messagebox as mBox

from weather import Weather
from cargo import Cargo
from window import *
from data import Person
from version import GetVersion
from process import ProcessRunNum
 

#####数据#####

DEBUG = False

#全局变量
PROCESS_NAME = "buyhouse"
ICON_NAME = "ico.ico"
VERSION = 1.2
CHECK_URL = "https://github.com/lingliqianxun/game-buyhouse/blob/master/version.txt?raw=true"
DOWN_URL = "https://github.com/lingliqianxun/game-buyhouse/blob/master/dist/buyhouse.exe?raw=true"


#个人存档数据
person = Person()
person.GetData()

#####事件#####

#成就展示
def ArchiveShow():
    archive_get = []
    archive_less = []

    for a in person.archives:
        if a['code'] in person.archive_person:
            continue
        else:
            archive_less.append(a) 

    if(len(archive_less) == 0):
        return archive_get

    for a in archive_less:
        if a['code'] == 'million':
            if (person.money + person.cash + person.alimoney) >= 1000000:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'ten_million':
            if (person.money + person.cash + person.alimoney) >= 10000000:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'hundred_million':
            if (person.money + person.cash + person.alimoney) >= 100000000:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'million_cash':
            if person.cash >= 1000000:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'million_alimoney':
            if person.alimoney >= 1000000:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'one_house':
            if len(person.building_house) > 0:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'big_house':
            if ('豪华住宅' in person.building_house) | \
                ('湖景别墅' in person.building_house) | \
                ('泳池私宅' in person.building_house):
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'hundred_agency':
            if person.cargo_max >= 200:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'one_year':
            if person.week >= 52:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'three_year':
            if person.week >= 52*3:
                archive_get.append(a)
                person.archive_person.append(a['code'])
        elif a['code'] == 'hope_full':
            if person.hope == 100:
                archive_get.append(a)
                person.archive_person.append(a['code'])

    person.SaveData()
    for a in archive_get:
        mBox.showinfo('成就解锁提示', a['descript']+'！', parent=win)

#结束游戏
def GameOver(event):
    global person
    person = Person()
    person.SaveData()
    win.destroy()
    
#是否死亡
def IsDead():
    global person
    if person.health == 0:
        toplevel_dead = tk.Toplevel(win)
        toplevel_dead.title("游戏结束")
        toplevel_dead.iconbitmap(WindowResourcePath(ICON_NAME))
        #toplevel_dead.wm_overrideredirect(1)
        WindowSizeCenter(toplevel_dead, 250,100)
        toplevel_dead.columnconfigure(0, weight=1)
        toplevel_dead.columnconfigure(1, weight=1)

        text = "共生存%d周" % person.week
        ttk.Label(toplevel_dead, text=text, foreground='red', anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, padx=20, pady=10)
        button_leave = ttk.Button(toplevel_dead, text="退出游戏", width=10,
                                command=toplevel_dead.destroy)
        button_leave.grid(column=0, columnspan=2, row=1, padx=20, pady=10)
        toplevel_dead.bind('<Destroy>',GameOver)

        toplevel_dead.grab_set()
        toplevel_dead.focus()

#金钱格式化
def MoneyFormat(money):
    if int(money/100000000) > 0:
        money_text = "%d亿" % int(money/100000000)
    else:
        money_text = ""

    if int(money%100000000/10000) > 0:
        money_text += "%d万" % int(money%100000000/10000)
    else:
        money_text += ""

    money_text += "%d元" % int(money%10000)
    return money_text

#存款利息计算
def Interest():
    global person
    if person.cash > 0:
        person.cash += int(person.cash*person.cash_interest)
    if person.alimoney > 0:
        person.alimoney += int(person.alimoney*person.alimoney_interest)
    return 0

#出租屋-货物出售-确定按钮-点击事件
def click_room_sell(toplevel_sell, num_sell, cargo_code, price_sell):
    try:
        num_sell = int(num_sell)
        if (num_sell < 0) | (num_sell > person.RoomCargosGetNum(cargo_code)):
            raise ValueError
    except ValueError:
        mBox.showwarning('卖出提示', '输入数额错误！', parent=toplevel_sell) 
        return

    for c in person.room_cargos:
        if c['code'] == cargo_code:
            c['num'] -= num_sell
            if(c['num'] == 0):
                person.room_cargos.remove(c)
        
    if(len(person.room_cargos) == 0):
        dic = {'code':'null', 'price_buy':'', 'num':''}
        person.room_cargos.append(dic)
            
    person.money += num_sell * price_sell
    person.cargo_cur -= num_sell
    
    toplevel_sell.destroy()
    FramPersonRefresh()
    FramRoomRefresh()

    mBox.showinfo('卖出提示', '卖出成功！', parent=win)
    ArchiveShow()

#出租屋-货物按钮-点击事件
def click_room_cargo(cargo_code):
    price_sell = person.MarketCargosGetPriceCur(cargo_code)
    if(price_sell == 0):
        mBox.showwarning('卖出提示', '市场不存在该货物！') 
        return
    
    toplevel_sell = tk.Toplevel(win)
    toplevel_sell.title("出售货物")
    toplevel_sell.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_sell, 250,120)
    toplevel_sell.columnconfigure(0, weight=1)
    toplevel_sell.columnconfigure(1, weight=1)
    
    ttk.Label(toplevel_sell, text="要卖几个？", anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    entry_num = ttk.Entry(toplevel_sell)
    entry_num.grid(column=0, columnspan=2, row=1)
    entry_num.insert(1,person.RoomCargosGetNum(cargo_code))
    button_yes = ttk.Button(toplevel_sell, text="确定", width=10,
                            command=lambda:click_room_sell(toplevel_sell,entry_num.get(),cargo_code,price_sell))
    button_yes.grid(column=0, columnspan=2, row=2, pady=10)

    toplevel_sell.grab_set()
    toplevel_sell.focus()
    
#市场-货物购买-确定按钮-点击事件
def click_market_buy(toplevel_buy, num_buy, cargo_code, price_cur):
    try:
        num_buy = int(num_buy)
        if num_buy <= 0:
            raise ValueError
    except ValueError:
        mBox.showwarning('购买提示', '输入数额错误！', parent=toplevel_buy) 
        return

    global person
    num_money_max = int(person.money/price_cur) 
    if(num_buy > num_money_max):
        mBox.showwarning('购买提示', '现金不足！', parent=toplevel_buy) 
        return
    num_cargo_max = person.cargo_max - person.cargo_cur
    if(num_buy > num_cargo_max):
        mBox.showwarning('购买提示', '库存不足！', parent=toplevel_buy) 
        return
     
    find = 0
    for c in person.room_cargos:
        if c['code'] == 'null':
            person.room_cargos.remove(c)
        elif c['code'] == cargo_code:
            c['price_buy'] = price_cur
            c['num'] += num_buy
            find = 1
        
    if find == 0:
        dic = {'code':cargo_code, 'price_buy':price_cur, 'num':num_buy}
        person.room_cargos.append(dic)
            
    person.money -= num_buy * price_cur
    person.cargo_cur += num_buy
    
    toplevel_buy.destroy()
    FramPersonRefresh()
    FramRoomRefresh()

    mBox.showinfo('购买提示', '购买成功！', parent=win)

#市场-货物按钮-点击事件
def click_market_cargo(cargo_code):
    price_cur = person.MarketCargosGetPriceCur(cargo_code)
    num_money_max = int(person.money/price_cur)   
    if(num_money_max == 0):
        mBox.showwarning('购买提示', '现金不足！') 
        return
    num_cargo_max = person.cargo_max - person.cargo_cur
    if(num_cargo_max <= 0):
        mBox.showwarning('购买提示', '库存不足！') 
        return
    if(num_money_max > num_cargo_max):
        num_max = num_cargo_max
    else:
        num_max = num_money_max
    
    toplevel_buy = tk.Toplevel(win)
    toplevel_buy.title("购买货物")
    toplevel_buy.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_buy, 250,120)
    toplevel_buy.columnconfigure(0, weight=1)
    toplevel_buy.columnconfigure(1, weight=1)
    
    ttk.Label(toplevel_buy, text="要买几个？", anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    entry_num = ttk.Entry(toplevel_buy, width=18)
    entry_num.grid(column=0, columnspan=2, row=1)
    entry_num.insert(1,num_max)
    button_yes = ttk.Button(toplevel_buy, text="确定",
                            command=lambda:click_market_buy(toplevel_buy,entry_num.get(),cargo_code,price_cur))
    button_yes.grid(column=0, columnspan=2, row=2, pady=10)

    toplevel_buy.grab_set()
    toplevel_buy.focus()
   
#操作-市场-点击事件 
def click_market1():
    global person
    #市场随机货物
    person.market_cargos.clear()
    Cargo().Random(person.market_cargos)
    
    #存款计算利息
    Interest()
    
    #天气随机
    person.week += 1
    person.weather = Weather().Random(person.weather)

    #健康
    person.health -= random.randrange(0,3)
    if person.health < 0:
        person.health = 0
    
    #面板刷新
    FramTopRefresh()
    FramPersonRefresh()
    FramMarketRefresh()
    ArchiveShow()
    IsDead()

#操作-医院-点击事件
def click_hospital():
    global person
    if (80 <= person.health) & (person.health <= 100):
        health_add = random.randrange(10,21)
    elif (60 <= person.health) & (person.health < 80):
        health_add = random.randrange(20,41)
    elif (person.health < 60):
        health_add = random.randrange(10,51)
    
    if person.health + health_add > 100:
        health_add = 100 - person.health
    person.health += health_add
    person.money -= 100
    FramPersonRefresh()

    text = "花费100元，恢复健康%d点" % health_add
    mBox.showwarning('恢复提示', text, parent=win) 

#操作-健身房-点击事件
def click_sport():
    global person
    if (80 <= person.health) & (person.health <= 100):
        health_add = random.randrange(5,11)
    elif (60 <= person.health) & (person.health < 80):
        health_add = random.randrange(3,7)
    elif (person.health < 60):
        health_add = random.randrange(0,4)
    
    if person.health + health_add > 100:
        health_add = 100 - person.health
    person.health += health_add
    person.money -= 10
    FramPersonRefresh()

    text = "花费10元，恢复健康%d点" % health_add
    mBox.showwarning('锻炼提示', text, parent=win) 

#操作-银行界面-存取款按钮-点击事件
def click_bank_button(toplevel_bank, num, action):
    try:
        num = int(num)
        if num <= 0:
            raise ValueError
    except ValueError:
        mBox.showwarning('购买提示', '输入数额错误！', parent=toplevel_bank) 
        return

    global person
    if(action == 0):
        if num > person.money:
            mBox.showwarning('购买提示', '现金不足！', parent=toplevel_bank) 
            return
        person.money -= num
        person.cash += num
    else:
        if num > person.cash:
            mBox.showwarning('购买提示', '存款不足！', parent=toplevel_bank) 
            return
        person.money += num
        person.cash -= num

    toplevel_bank.destroy()
    FramPersonRefresh()

    if(action == 0):
        mBox.showinfo('存取款提示', '存款成功！', parent=win)
    else:
        mBox.showinfo('存取款提示', '取款成功！', parent=win)
    ArchiveShow()
 
#操作-银行-点击事件   
def click_bank():
    toplevel_bank = tk.Toplevel(win)
    toplevel_bank.title("存取款操作")
    toplevel_bank.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_bank, 250,120)
    toplevel_bank.columnconfigure(0, weight=1)
    toplevel_bank.columnconfigure(1, weight=1)

    text = "要存取多少？（周%%%d利息）" % (person.cash_interest*100)
    ttk.Label(toplevel_bank, text=text, anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    entry_num = ttk.Entry(toplevel_bank)
    entry_num.grid(column=0, columnspan=2, row=1, sticky=tk.E+tk.W, padx=20)
    #entry_num.insert(1,num_max)
    button_in = ttk.Button(toplevel_bank, text="存款",
                            command=lambda:click_bank_button(toplevel_bank,entry_num.get(),0))
    button_in.grid(column=0, row=2, pady=10)
    button_out = ttk.Button(toplevel_bank, text="取款",
                            command=lambda:click_bank_button(toplevel_bank,entry_num.get(),1))
    button_out.grid(column=1, row=2, pady=10)

    toplevel_bank.grab_set()
    toplevel_bank.focus()

#操作-余X宝界面-存取款按钮-点击事件
def click_bank_button(toplevel_alipay, num, action):
    try:
        num = int(num)
        if num <= 0:
            raise ValueError
    except ValueError:
        mBox.showwarning('操作提示', '输入数额错误！', parent=toplevel_alipay) 
        return

    global person
    if(action == 0):
        if num > person.money:
            mBox.showwarning('操作提示', '现金不足！', parent=toplevel_alipay) 
            return
        person.money -= num
        person.alimoney += num
    else:
        if num > person.alimoney:
            mBox.showwarning('操作提示', '提现余额不足！', parent=toplevel_alipay) 
            return
        person.money += num
        person.alimoney -= num

    toplevel_alipay.destroy()
    FramPersonRefresh()

    if(action == 0):
        mBox.showinfo('存取款提示', '存入成功！', parent=win)
    else:
        mBox.showinfo('存取款提示', '提现成功！', parent=win)
    ArchiveShow()
 
#操作-余X宝-点击事件   
def click_alipay():
    toplevel_alipay = tk.Toplevel(win)
    toplevel_alipay.title("存取款操作")
    toplevel_alipay.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_alipay, 250,120)
    toplevel_alipay.columnconfigure(0, weight=1)
    toplevel_alipay.columnconfigure(1, weight=1)

    text = "要存取多少？（周%%%d利息）" % (person.alimoney_interest*100)
    ttk.Label(toplevel_alipay, text=text, anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    entry_num = ttk.Entry(toplevel_alipay)
    entry_num.grid(column=0, columnspan=2, row=1, sticky=tk.E+tk.W, padx=20)
    #entry_num.insert(1,num_max)
    button_in = ttk.Button(toplevel_alipay, text="存入",
                            command=lambda:click_bank_button(toplevel_alipay,entry_num.get(),0))
    button_in.grid(column=0, row=2, pady=10)
    button_out = ttk.Button(toplevel_alipay, text="提现",
                            command=lambda:click_bank_button(toplevel_alipay,entry_num.get(),1))
    button_out.grid(column=1, row=2, pady=10)

    toplevel_alipay.grab_set()
    toplevel_alipay.focus()

#操作-中介购买-确定按钮-点击事件
def click_agency_buy(toplevel_agency, num_buy):
    try:
        num_buy = int(num_buy)
        if num_buy <= 0:
            raise ValueError
    except ValueError:
        mBox.showwarning('操作提示', '输入数额错误！', parent=toplevel_agency) 
        return

    global person
    if(num_buy > int(person.money/10000)):
        mBox.showwarning('操作提示', '现金不足！', parent=toplevel_agency) 
        return
            
    person.money -= num_buy * 10000
    person.cargo_max += num_buy
    
    toplevel_agency.destroy()
    FramPersonRefresh()
    FramRoomRefresh()

    mBox.showinfo('操作提示', '购买成功！', parent=win)
    ArchiveShow()

#操作-中介-点击事件
def click_agency():
    toplevel_agency = tk.Toplevel(win)
    toplevel_agency.title("购买出租屋")
    toplevel_agency.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_agency, 250,120)
    toplevel_agency.columnconfigure(0, weight=1)
    toplevel_agency.columnconfigure(1, weight=1)
    
    ttk.Label(toplevel_agency, text="要买几个(1个/1万)？", width=20, anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    entry_num = ttk.Entry(toplevel_agency)
    entry_num.grid(column=0, columnspan=2, row=1, padx=20)
    #entry_num.insert(1,num_max)
    button_yes = ttk.Button(toplevel_agency, text="确定",
                            command=lambda:click_agency_buy(toplevel_agency,entry_num.get()))
    button_yes.grid(column=0, columnspan=2, row=2, pady=10)

    toplevel_agency.grab_set()
    toplevel_agency.focus()
 
#操作-售楼部面板-按钮-确定-点击事件   
def click_building_buy_yes(toplevel_building, toplevel_building_ask, name, price):
    global person
    person.building_house.append(name)
    person.money -= price*10000
    person.hope += 5
    if person.hope > 100:
        person.hope = 100
    
    toplevel_building_ask.destroy()
    toplevel_building.destroy()
    FramPersonRefresh()
    FramRoomRefresh()   

    mBox.showinfo('购买提示', '购买成功！')
    ArchiveShow()
 
#操作-售楼部面板-按钮-点击事件   
def click_building_buy(toplevel_building, name, price):
    global person
    if(person.money < price*10000):
        mBox.showwarning('购买提示', '现金不足！', parent=toplevel_building) 
        return

    toplevel_building_ask= tk.Toplevel(toplevel_building)
    toplevel_building_ask.title("购买提示")
    toplevel_building_ask.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_building_ask, 250,120)
    toplevel_building_ask.columnconfigure(0, weight=1)
    toplevel_building_ask.columnconfigure(1, weight=1)
    
    ttk.Label(toplevel_building_ask, text="确定购买吗？", anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, pady=10)
    button_yes = ttk.Button(toplevel_building_ask, text="确定",
                            command=lambda:click_building_buy_yes(toplevel_building, toplevel_building_ask, name, price))
    button_yes.grid(column=0, row=1, pady=10)
    button_no= ttk.Button(toplevel_building_ask, text="取消",
                            command=toplevel_building_ask.destroy)
    button_no.grid(column=1, row=1, pady=10)

    toplevel_building_ask.grab_set()
    toplevel_building_ask.focus()
    
#操作-售楼部-点击事件
def click_building():
    toplevel_building = tk.Toplevel(win)
    toplevel_building .title("售楼部")
    toplevel_building.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_building, 320, 280)
    ttk.Label(toplevel_building, text="户型", width=10).grid(column=0, row=0, padx=20, pady=10)
    ttk.Label(toplevel_building, text="面积（m2）", width=12, anchor=tk.E).grid(column=1, row=0, pady=10)
    ttk.Label(toplevel_building, text="价格（万）", width=12, anchor=tk.E).grid(column=2, row=0, pady=10)

    for index,b in enumerate(person.buildings):
        if b['name'] in person.building_house:
            state = tk.DISABLED
        else:
            state = tk.NORMAL
        ttk.Button(toplevel_building, text=b['name'], state=state,width=10,command=lambda name=b['name'],price=b['price']:click_building_buy(toplevel_building,name,price)).grid(column=0, row=index+1, padx=20)
        ttk.Label(toplevel_building, text=b['m'], width=12, anchor=tk.E).grid(column=1, row=index+1)
        ttk.Label(toplevel_building, text=b['price'], width=12, anchor=tk.E).grid(column=2, row=index+1)

    #toplevel_building.wm_attributes('-topmost',1)
    toplevel_building.grab_set()
    toplevel_building.focus()
 
#操作-彩票-下注点击开奖事件 
def click_lottery_open(toplevel_lottery, num, var, label_result):
    try:
        num = int(num)
        if num <= 0:
            raise ValueError
    except ValueError:
        mBox.showwarning('操作提示', '输入数额错误！', parent=toplevel_lottery) 
        return

    global person
    if(num > int(person.money)):
        mBox.showwarning('操作提示', '现金不足！', parent=toplevel_lottery) 
        return

    person.money -= num
    FramPersonRefresh()

    toplevel_run = tk.Toplevel(toplevel_lottery)
    toplevel_run.title("开奖提示")
    toplevel_run.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_run, 220, 120)
    
    ttk.Label(toplevel_run, text="开奖中，请稍等...", width=25, anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, padx=20, pady=40)
    toplevel_run.update()
    time.sleep(1)
    toplevel_run.destroy()

    prize = random.randrange(1,11)
    add_money = 0
    #1~5
    if(var==1):
        if (0 <= prize) | (prize <= 5):
            add_money = num*2
    #6~10
    elif(var==2):
        if (6 <= prize) | (prize <= 10):
            add_money = num*2
    #6
    elif(var==3):
        if (6 == prize):
            add_money = num*10
    #单
    elif(var==4):
        if (prize%2==1):
            add_money = num*2
    #双
    elif(var==5):
        if (prize%2==0):
            add_money = num*2
     
    person.money += add_money
    FramPersonRefresh()
    label_result.config(text="上期开奖结果：%d"%prize)
    if add_money > 0:
        mBox.showwarning('中奖提示', '恭喜获得%d元！'%add_money, parent=toplevel_lottery) 
    else:
        mBox.showwarning('中奖提示', '未中奖~', parent=toplevel_lottery) 
    ArchiveShow()
    
   
#操作-彩票-点击事件
def click_lottery():
    toplevel_lottery = tk.Toplevel(win)
    toplevel_lottery .title("时时彩票")
    toplevel_lottery.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_lottery, 420, 220)

    ttk.Label(toplevel_lottery, text="随机1~10号数字，猜中直返倍率，请下注数额~").grid(column=0, columnspan=3, row=0, padx=20, pady=10)
    ttk.Label(toplevel_lottery, text="范围(双倍)").grid(column=0, row=1, padx=20, pady=10)
    ttk.Label(toplevel_lottery, text="特殊(十倍)").grid(column=1, row=1, padx=20, pady=10)
    ttk.Label(toplevel_lottery, text="单双(双倍)").grid(column=2, row=1, padx=20, pady=10)

    def radio_click():
        pass
    radio_var = tk.IntVar()
    tk.Radiobutton(toplevel_lottery, text='1~5', variable=radio_var, value=1, command=radio_click).grid(column=0, row=2, sticky=tk.W, padx=20)
    r=tk.Radiobutton(toplevel_lottery, text='6', variable=radio_var, value=3, command=radio_click)
    r.grid(column=1, row=2, sticky=tk.W+tk.E, padx=20)
    r.select()
    tk.Radiobutton(toplevel_lottery, text='单', variable=radio_var, value=4, command=radio_click).grid(column=2, row=2, sticky=tk.W, padx=20)
    tk.Radiobutton(toplevel_lottery, text='6~10', variable=radio_var, value=2, command=radio_click).grid(column=0, row=3, sticky=tk.W, padx=20)
    tk.Radiobutton(toplevel_lottery, text='双', variable=radio_var, value=5, command=radio_click).grid(column=2, row=3, sticky=tk.W, padx=20)

    ttk.Label(toplevel_lottery, text="押注数(元)").grid(column=0, row=4, padx=20, pady=10)
    entry_num = ttk.Entry(toplevel_lottery)
    entry_num.grid(column=1, row=4, padx=20)
    #entry_num.insert(1,num_max)
    button_open = ttk.Button(toplevel_lottery, text="下注",
                            command=lambda:click_lottery_open(toplevel_lottery,entry_num.get(), radio_var.get(), label_result))
    button_open.grid(column=2, row=4, pady=10)
    label_result = ttk.Label(toplevel_lottery, text="")
    label_result.grid(column=0, columnspan=3, row=5, padx=20, pady=10)

    toplevel_lottery.grab_set()
    toplevel_lottery.focus()

#操作-成就-点击事件
def click_archive():
    toplevel_archive = tk.Toplevel(win)
    toplevel_archive.title("已获成就")
    toplevel_archive.iconbitmap(WindowResourcePath(ICON_NAME))
    WindowSizeCenter(toplevel_archive, 250, 250)
    toplevel_archive.columnconfigure(0, weight=1)
    toplevel_archive.columnconfigure(1, weight=1)

    text = '空'
    if len(person.archive_person) > 0:
        text = '成就列表'
    ttk.Label(toplevel_archive, text=text, anchor=tk.CENTER).grid(column=0, row=0, columnspan=2, padx=20, pady=10)

    for index,a in enumerate(person.archive_person):
        ttk.Label(toplevel_archive, text=index+1, width=4, anchor=tk.E).grid(column=0, row=index+1, padx=20)
        ttk.Label(toplevel_archive, text=person.ArchiveGetDescript(a), width=20, anchor=tk.E).grid(column=1, row=index+1)

    toplevel_archive.grab_set()
    toplevel_archive.focus()

#操作-关于-点击事件
def click_about():
    text = "版本：" + str(VERSION) + "\n制作：By 绫里千寻"
    mBox.showinfo('关于本软件', text)
    
#操作-重新开始-点击事件
def click_restart():
    global person
    person = Person()
    FramTopRefresh()
    FramPersonRefresh()
    FramRoomRefresh()
    FramMarketRefresh()

    mBox.showinfo('重新开始游戏', '重置成功！')

#####面板#####
win = tk.Tk()       
win.title("买房记v%s" % VERSION)  
win.iconbitmap(WindowResourcePath(ICON_NAME))
#win.resizable(0,0)
WindowSizeCenter(win,660,500)

#顶部信息面板
def FramTopRefresh():
    label_weather.configure(text=person.weather)
    label_week.configure(text=str(person.week)+"/周")
    
fram_top = ttk.LabelFrame(win, text='', width=615, height=50)
fram_top.grid_propagate(0)
fram_top.grid(column=0, columnspan=3, row=0, sticky='WN', padx=20, pady=4)
ttk.Label(fram_top, text="天气：", width=6, anchor=tk.E).grid(column=0, row=0, sticky='E')
label_weather = ttk.Label(fram_top, width=8)
label_weather.grid(column=1, row=0, sticky='E')
label_week = ttk.Label(fram_top, width=60, anchor=tk.E)
label_week.grid(column=2, row=0, sticky='E')
FramTopRefresh()

#个人信息面板
def FramPersonRefresh():
    label_money.configure(text=MoneyFormat(person.money))
    label_cash.configure(text=MoneyFormat(person.cash))
    label_alimoney.configure(text=MoneyFormat(person.alimoney))

    label_health.configure(text=person.health)
    label_hope.configure(text=person.hope)
    person.SaveData()
    
fram_person = ttk.LabelFrame(win, text='个人信息', width=195, height=290)
fram_person.grid_propagate(0)
fram_person.grid(column=0, row=1, sticky='WN', padx=20, pady=10)
ttk.Label(fram_person, text="现  金：", width=8, anchor=tk.E).grid(column=0, row=0, sticky='E')
label_money = ttk.Label(fram_person, width=17, anchor=tk.E)
label_money.grid(column=1, row=0, sticky='E')
ttk.Label(fram_person, text="存  款：").grid(column=0, row=1, sticky='E')
label_cash = ttk.Label(fram_person)
label_cash.grid(column=1, row=1, sticky='E')
ttk.Label(fram_person, text="余X宝：").grid(column=0, row=2, sticky='E')
label_alimoney = ttk.Label(fram_person)
label_alimoney.grid(column=1, row=2, sticky='E')
ttk.Label(fram_person, text="健  康：").grid(column=0, row=3, sticky='E')
label_health = ttk.Label(fram_person)
label_health.grid(column=1, row=3, sticky='E')
ttk.Label(fram_person, text="声  望：").grid(column=0, row=4, sticky='E')
label_hope = ttk.Label(fram_person)
label_hope.grid(column=1, row=4, sticky='E')
FramPersonRefresh()

#出租屋面板
def FramRoomRefresh():
    room_str='出租屋'+'('+str(person.cargo_cur)+'/'+str(person.cargo_max)+')'
    fram_room.configure(text=room_str)
    
    #先清空
    for child in fram_room.winfo_children():
        if (child.cget('text')!='货物') & (child.cget('text')!='买入价') & (child.cget('text')!='数量'):
            child.destroy()
    for index,c in enumerate(person.room_cargos):
        if c['code'] == 'null':
            ttk.Label(fram_room, text="空",anchor=tk.W).grid(column=0, row=index+1,sticky='W')
            break
        ttk.Button(fram_room, text=Cargo().GetName(c['code']),width=12, command=lambda code=c['code']: click_room_cargo(code)).grid(column=0, row=index+1)
        ttk.Label(fram_room, text=c['price_buy'],width=8,anchor=tk.E).grid(column=1, row=index+1, sticky='E')
        ttk.Label(fram_room, text=c['num'],width=8,anchor=tk.E).grid(column=2, row=index+1, sticky='E')

fram_room = ttk.LabelFrame(win, width=220, height=290)
fram_room.grid_propagate(0)
fram_room.grid(column=1, row=1, sticky='WN', padx=0, pady=10)
ttk.Label(fram_room, text="货物", width=12).grid(column=0, row=0)
ttk.Label(fram_room, text="买入价", width=8, anchor=tk.E).grid(column=1, row=0)
ttk.Label(fram_room, text="数量", width=8, anchor=tk.E).grid(column=2, row=0)
#s = ttk.Style().configure('A.TButton', anchor=tk.W)
#ttk.Button(style='A.TButton')
FramRoomRefresh()

#市场面板
def FramMarketRefresh():
    #先清空
    for child in fram_market.winfo_children():
        if (child.cget('text')!='货物') & (child.cget('text')!='价格'):
            child.destroy()
    for index,c in enumerate(person.market_cargos):
        if c['code'] == 'null':
            ttk.Label(fram_market, text="空",anchor=tk.W).grid(column=0, row=index+1,sticky='W')
            break
        ttk.Button(fram_market, text=Cargo().GetName(c['code']),width=12, command=lambda code=c['code']: click_market_cargo(code)).grid(column=0, row=index+1)
        ttk.Label(fram_market, text=c['price_cur'],width=8,anchor=tk.E).grid(column=1, row=index+1, sticky='E')

fram_market = ttk.LabelFrame(win, text='市场', width=160, height=290)
fram_market.grid_propagate(0)
fram_market.grid(column=2, row=1, sticky='WN', padx=20, pady=10)
ttk.Label(fram_market, text="货物", width=12).grid(column=0, row=0)
ttk.Label(fram_market, text="价格", width=8, anchor=tk.E).grid(column=1, row=0)
FramMarketRefresh()

#操作面板        
fram_option = ttk.LabelFrame(win, text='操作', width=615, height=110)
fram_option.grid_propagate(0)
fram_option.grid(column=0, row=2, columnspan=3, sticky='WN', padx=20, pady=10)
button_market1 = ttk.Button(fram_option,text="二手市场",width=10, command=lambda:click_market1())
button_market1.grid(column=0, row=0)
button_market2 = ttk.Button(fram_option,text="市场",width=10, command=lambda:click_market1())
button_market2.grid(column=1, row=0)
button_market3 = ttk.Button(fram_option,text="农贸市场",width=10, command=lambda:click_market1())
button_market3.grid(column=2, row=0)
button_about = ttk.Button(fram_option,text="关于",width=10, command=lambda:click_about())
button_about.grid(column=3, row=0)

button_hospital = ttk.Button(fram_option,text="医院",width=10, command=lambda:click_hospital())
button_hospital.grid(column=0, row=1)
button_sport = ttk.Button(fram_option,text="健身房",width=10, command=lambda:click_sport())
button_sport.grid(column=1, row=1)
button_bank = ttk.Button(fram_option,text="银行",width=10, command=lambda:click_bank())
button_bank.grid(column=2, row=1)
button_alipay = ttk.Button(fram_option,text="余X宝",width=10, command=lambda:click_alipay())
button_alipay.grid(column=3, row=1)

button_agency = ttk.Button(fram_option,text="中介",width=10, command=lambda:click_agency())
button_agency.grid(column=0, row=2)
button_building = ttk.Button(fram_option,text="售楼部",width=10, command=lambda:click_building())
button_building.grid(column=1, row=2)
button_lottery = ttk.Button(fram_option,text="彩票",width=10, command=lambda:click_lottery())
button_lottery.grid(column=2, row=2)
button_archive = ttk.Button(fram_option,text="成就",width=10, command=lambda:click_archive())
button_archive.grid(column=3, row=2)

button_restart = ttk.Button(fram_option,text="重新开始",width=10, command=lambda:click_restart())
button_restart.grid(column=4, rowspan=3, sticky=tk.N+tk.S, row=0)


#查询版本
threading.Thread(target=GetVersion, args=(win,PROCESS_NAME,ICON_NAME,VERSION,CHECK_URL,DOWN_URL)).start()
win.mainloop()

##判断进程是否存在
##存在Bug：先运行，后改名字再运行
#if (ProcessRunNum(PROCESS_NAME) == 0) & (DEBUG == False):
#    win.destroy()
#    win = tk.Tk()
#    win.withdraw()
#    mBox.showwarning('运行提示', '请不要更改程序名称 buyhouse.exe', parent=win) 
#elif ProcessRunNum(PROCESS_NAME) > 2:
#    win.destroy()
#    win = tk.Tk()
#    win.withdraw()
#    mBox.showwarning('运行提示', '已有程序在运行!', parent=win) 
#else:
#    #查询版本
#    threading.Thread(target=GetVersion, args=(win,PROCESS_NAME,ICON_NAME,VERSION,CHECK_URL,DOWN_URL)).start()
#    win.mainloop()