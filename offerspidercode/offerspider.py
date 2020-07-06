import requests
import useragenttool
import proxytool
import lxml.html
import time
import random
import os
import xlwt

class Offerspider(object):
    def __init__(self):
        """初始化"""
        self.offer_index_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        self.offer_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        self.list = []
    def get_offer_pages(self):
        """动态获取页面数，int"""
        request = requests.get(self.offer_index_url,
                     headers=useragenttool.get_headers(),
                     proxies=proxytool.get_proxy())
        # 获取网页源码
        response = request.content.decode("gbk")
        # 解析数据
        metree = lxml.html.etree
        page_parser = metree.HTML(response)
        # print(response)
        # 提取内容页数
        pages_content = page_parser.xpath("//div[@class='dw_page']//span[@class='td']/text()")[0]
        offer_pages = int(pages_content[1:4])
        return offer_pages

    def get_offer_url_list(self,numbers):
        """拼接所有页面URL"""
        url_list = []
        for page_index in range(1,numbers+1):
            temp_url = self.offer_url.format(page_index)
            url_list.append(temp_url)
        return url_list

    def parse_offer_url(self,temp_url):
        """爬取整个页面内容"""
        offer_response = requests.get(temp_url,
                                      headers=useragenttool.get_headers(),
                                      proxies=proxytool.get_proxy())
        offer_html_content = offer_response.content.decode("gbk","ignore")
        return offer_html_content

    def catch_work_info(self,offer_name_url):
        """通过职位名称链接提取工作职责"""
        offer_content = self.parse_offer_url(offer_name_url)
        #解析数据
        metree = lxml.html.etree
        offer_parser = metree.HTML(offer_content)
        work_info = "".join(offer_parser.xpath("//div[@class='bmsg job_msg inbox']//text()")).strip().replace(" ","")
        # print(work_info)
        return work_info

    def catch_company_info(self,company_url):
        """通过公司链接提取公司简介"""
        company_content = self.parse_offer_url(company_url)
        # 解析数据
        metree = lxml.html.etree
        company_parser = metree.HTML(company_content)
        company_info = "".join(company_parser.xpath("//div[@class='con_txt']/text()")).strip().replace(" ", "")
        # print(company_info)
        return company_info

    def catch_offer_html(self,html_content):
        """提取单个页面的职位名，职位名称链接，公司名，公司链接，工作地点，薪资，发布时间，工作职责，公司简介"""
        # 解析数据

        metree = lxml.html.etree
        html_parser = metree.HTML(html_content)
        #提取数据
        offer = html_parser.xpath("//div[@class='el']")[4:]
        # print(offer)
        for element in offer:
            # 提取职位名
            element_list = []
            offer_name = element.xpath("./p/span/a/@title")[0]
            element_list.append(offer_name)
            # print(item)
            # print(offer_name)
            #提取职位名称链接
            offer_name_url = element.xpath("./p/span/a/@href")[0]
            # print(offer_name_url)
            element_list.append(offer_name_url)
            #公司名
            company_mame = element.xpath("./span[@class='t2']/a/text()")[0]
            element_list.append(company_mame)
            # print(company_mame)
            #公司链接
            company_url = element.xpath("./span[@class='t2']/a/@href")[0]
            element_list.append(company_url)
            # print(company_url)
            #工作地点
            workplace = element.xpath("./span[@class='t3']/text()")[0]
            element_list.append(workplace)
            #薪资
            salary = element.xpath("./span[@class='t4']/text()")
            if salary ==[]:
                salary =['4-5千/月']
            salary = salary[0]
            salary_result = 8000
            if "千/月" in salary:
                salary_result = int(float(salary.split("-")[0])*1000)
            elif "万/月" in salary:
                salary_result = int(float(salary.split("-")[0])*10000)
            element_list.append(salary_result)
            # print(salary)
            #发布时间
            pushtime = element.xpath("./span[@class='t5']/text()")[0]
            element_list.append(pushtime)
            # 工作职责
            work_info = self.catch_work_info(offer_name_url)
            element_list.append(work_info)
            # 公司简介
            company_info = self.catch_company_info(company_url)
            element_list.append(company_info)
            self.list.append(element_list)
        # print(self.list)
        # print(len(self.list))
        return self.list

    def sava_offer_page_data(self):
        """保存所有数据内容到EXCEL中"""
        offer_path = "./offerdata"
        if not os.path.exists(offer_path):
            os.mkdir(offer_path)
        #获得Book工作薄
        book = xlwt.Workbook(encoding="utf-8")
        #创建一个表格标题
        offer_sheet = book.add_sheet("python招聘信息")
        #写入数据
        row_index = 0
        #表头
        header = ['职位名','职位名称链接','公司名','公司链接','工作地点','薪资','发布时间','工作职责','公司简介']
        while row_index<len(self.list):
            col_index = 0
            while col_index<len(self.list[row_index]):
                if row_index == 0:
                    offer_sheet.write(row_index,col_index,header[col_index])
                else:
                    offer_sheet.write(row_index,col_index,self.list[row_index][col_index])
                col_index +=1
            row_index +=1
        book.save(offer_path+"/招聘python岗位信息表.xls")


    def run(self):
        # 动态获取页面数
        # page_total = self.get_offer_pages()
        page_total = 5
        # 拼接URL列表内容
        offer_url_datas = self.get_offer_url_list(page_total)

        i = 0
        for http_url in offer_url_datas:
            i +=1
            # print(http_url)
            offer_url_datas = self.parse_offer_url(http_url)
            # print("输出内容",offer_url_datas)
            self.catch_offer_html(offer_url_datas)
            self.sava_offer_page_data()

            # 限制处理
            wait_time = random.randint(0,10)
            print("动态限制访问频率，%ds继续爬取数据..."%wait_time)
            time.sleep(wait_time)
            print("第%d页爬取成功！---------"%i)
        print("所有数据保存成功")



def main():
    url_page = Offerspider()
    url_page.run()

if __name__ == '__main__':
    main()