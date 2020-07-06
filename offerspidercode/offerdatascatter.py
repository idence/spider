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
    #读取所有数据内容
    offer_salary = read_offer_data_excel()
    # print(offer_salary)
    #绘制薪资分布图
    pyplot.figure(figsize=(18,8),dpi=80)
    x = [i for i in range(1,offer_salary.size+1)]
    #绘制
    pyplot.scatter(x,offer_salary,label="薪资值")
    # 添加标题
    pyplot.title("某招聘网python岗位薪资分布图")
    # x/y
    pyplot.xlabel("岗位个数")
    pyplot.ylabel("薪资")
    # 处理中文乱码
    pyplot.rcParams["font.sans-serif"] = ["SimHei"]
    #x刻度 每隔十个数则绘制刻度值
    x_tick = [i for i in range(0,offer_salary.size+1,10)]
    pyplot.xticks(x_tick,x_tick,rotation=45)
    #最大最小值
    pyplot.xlim(0,250)
    # y刻度
    y_tick = [i for i in range(0,41000,2500)]
    pyplot.yticks(y_tick)
    pyplot.ylim(0,40000)
    #网格
    pyplot.grid(alpha=0.1)

    # 绘制均值线
    aver = numpy.mean(offer_salary)
    print("平均薪资",aver)
    aver_list = [aver for i in x]
    pyplot.plot(x,aver_list,'g',linewidth=3,label="平均薪资")
    # 绘制均值数值
    pyplot.text(0,aver+200,"均薪："+str(aver),color="green")
    #绘制图例
    pyplot.legend(loc=0)

    #显示
    pyplot.show()



if __name__ == '__main__':
    main()