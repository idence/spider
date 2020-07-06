import lxml.html
import lxml
import json
import catchproxyspider

def catch_proxy_value_list(html_content):
    """提取数据内容"""
    proxy_list = []
    # (1)解析器对象； --用于解析html代码
    metree = lxml.html.etree
    proxy_parse = metree.HTML(html_content)
    # （2）获得所有的tr列表；
    tr_list = proxy_parse.xpath("//table[@id='ip_list']/tr")[1:]
    # print(tr_list)
    # print(len(tr_list))
    # （3）遍历tr列表，tr单个元素；
    for tr_element in tr_list:
        ip_item = {}
        # （4）提取数据内容；
        ip = tr_element.xpath("./td[2]/text()")[0]
        # print(ip)
        agreement = tr_element.xpath("./td[6]/text()")[0]
        # print(agreement)
        proxy_item = {agreement:agreement.lower()+ "://" + ip}
        # print(proxy_item)
        proxy_list.append(proxy_item)
    # print(proxy_list)
    return proxy_list

def save_proxy_file(ip_path,datas):
    """保存所有的IP代理数据到json文件中"""
    json.dump(datas,
              open(ip_path+"/proxydata.json",'w',encoding="utf-8"),
              ensure_ascii=False,
              indent=2
    )
    print("所有数据已保存成功！")

def main():
    # file = open("../../test/1.html", encoding="utf-8")
    # file_content = file.read()
    # print(file_content)
    http_url = "https://www.xicidaili.com/nn/"
    content = catchproxyspider.parse_proxy_url(http_url)
    datas = catch_proxy_value_list(content)
    # file.close()
    ip_path = "../../test"
    save_proxy_file(ip_path,datas)

if __name__ == '__main__':
    main()
