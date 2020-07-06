import urllib.request

import useragenttool


def parse_proxy_url(temp_url):


    # （1）随机隐藏身份信息；
    headers = useragenttool.get_headers()
    # （2）发送请求；
    request = urllib.request.Request(temp_url, headers=headers)
    # （3）获取响应； -->*保存一份html源码到本地，分析数据
    response = urllib.request.urlopen(request)
    html_result = response.read().decode("utf-8")
    # print(html_result)
    file = open("../../test/2.html", 'w', encoding="utf-8")
    file.write(html_result)
    return html_result

def main():
    http_url = "https://www.xicidaili.com/nn/"
    parse_proxy_url(http_url)

if __name__ == '__main__':
    main()