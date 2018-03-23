import os, sys
import base64


def Encry(data):
    data_encry = base64.b64encode(data.encode('utf-8')).decode('utf-8')
    data_change = data_encry[-8:] + data_encry[8:-8] + data_encry[:8]
    return data_encry

def Decry(data):
    #data_change = data[-8:] + data[8:-8] + data[:8]
    data_decry = base64.b64decode(data.encode('utf-8')).decode('utf-8')
    return data_decry


#测试用
def Test():
    #f1=open('data.txt','r',encoding='ISO-8859-1')
    f1=open('data.txt','r',encoding='utf-8')
    c=f1.read()
    print(c)
    print(Encry(c))
    print(Decry(Encry(c)))
    f1.close()

    while(1):
        os.getcwd()
#Test()
