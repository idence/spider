import pandas
from matplotlib import pyplot
import numpy


def read_offer_data_excel():
    """从Excel表格中获取数据内容"""
    data_results = pandas.read_excel("./offerdata/招聘python岗位信息表.xls")
    # print("所有数据内容",data_results)
    salary = data_results["薪资"]
    return salary


def main():
    # 读取所有数据内容
    offer_salary = read_offer_data_excel()
    # print(offer_salary)
    count_5k = 0
    count_8k = 0
    count_14k = 0
    count_m14k = 0
    index = 0
    while index<offer_salary.size:
        if offer_salary[index] < 5000:
            count_5k += 1
        elif offer_salary[index] <8000:
            count_8k += 1
        elif offer_salary[index] <14000:
            count_14k += 1
        else:
            count_m14k += 1
        index +=1
    # print(count_5k)
    # 绘制薪资占比图
    pyplot.rcParams["font.sans-serif"] = ["SimHei"]
    data = [count_5k,count_8k,count_14k,count_m14k]
    labels = ["5k以下","5-8k","8-14k","14k以上"]
    explores = [0,0,0,0.05]
    pyplot.pie(data,labels=labels,autopct="%2.2f%%",explode=explores)
    pyplot.title("python岗位薪资占比分布")
    pyplot.legend(loc="upper left")

    # 显示
    pyplot.show()


if __name__ == '__main__':
    main()