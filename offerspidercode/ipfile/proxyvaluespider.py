import json
import requests
import useragenttool

def read_proxy_file_by_json():
    file = open("../../test/proxydata.json",'r',encoding="utf-8")
    content = json.load(file)
    return content



def main():
    proxy_ip_datas = read_proxy_file_by_json()
    sohu_url = "https://www.sohu.com/"
    #有用的ip
    value_proxy_list = []
    # print("结果：",proxy_ip_datas)
    #遍历，分析通信是否正常
    for proxy in proxy_ip_datas:
        # print(proxy)
        try:
            #处理ip
            proxy_response = requests.get(sohu_url, headers = useragenttool.get_headers(), proxies = proxy)
            # proxy_response.status_code
            if proxy_response.status_code == 200:
                value_proxy_list.append(proxy)
                #保存
                json.dump(value_proxy_list,
                          open("./proxypool.json","w",encoding="utf-8"),
                          ensure_ascii= False,
                          indent= 2)
                print("正在添加到ip代理池中的ip代理值为：",proxy)
        except Exception:
            print("该ip代理异常，ip代理值为",proxy)




if __name__ == '__main__':
    main()