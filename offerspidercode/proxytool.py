import json
import random





def read_proxy_file():
    proxy_file = json.load(open("D:/TestFile/Spider python/day01/OfferSpiderTool/Tool/ipfile/proxypool.json", "r", encoding="utf-8"))
    return proxy_file

def get_proxy():
    proxy_datas = read_proxy_file()
    index = random.randint(0,len(proxy_datas)-1)
    return proxy_datas[index]



if __name__ == '__main__':
    proxy = get_proxy()
    print("获取的动态ip为",proxy)