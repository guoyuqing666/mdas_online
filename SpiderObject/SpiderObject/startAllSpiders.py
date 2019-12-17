from scrapy import cmdline
import os

# cmdline.execute("scrapy crawlall".split())
# cmdline.execute("scrapy crawl dzh -o dzh.csv".split())

from tkinter import *
import time

from tkinter import *


def callback():
    var.set('程序正在运行，请稍等...')
    #cmdline.execute("scrapy crawlall".split())
    #cmdline.execute("scrapy crawl dzh -o dzh.csv".split())
    #cmdline.execute("scrapy crawl detail".split())

    #os.system("scrapy crawlall -s CLOSESPIDER_TIMEOUT=120")
    #os.system("scrapy crawl dzh -o dzh.csv")
    os.system("scrapy crawl detail")

root = Tk()

frame1 = Frame(root)  # Frame    框架控件；在屏幕上显示一个矩形区域，多用来作为容器
frame2 = Frame(root)

todayDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
var = StringVar()  # 设置字符串
var.set("今天的日期是:"+todayDate+"\n 要开始并行运行所有爬虫吗？")

textLabel = Label(frame1,
                  textvariable=var,
                  justify=LEFT)

textLabel.pack(side=LEFT)

theButton = Button(frame2, text="爬取全部内容", command=callback)  # 定义一个按钮
theButton.pack()

frame1.pack(padx=10, pady=10)  # 定义位置
frame2.pack(padx=50, pady=50)

mainloop()