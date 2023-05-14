import requests

requests.packages.urllib3.disable_warnings()

from lxml import etree

from datetime import datetime, timedelta

from threading import Thread

import csv

from math import ceil

import os

import re

from time import sleep

from random import randint

#这里还有个user-agent和Cookie，里面的数据需要换成自己的，我帮你找在哪里
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Cookie': '''SINAGLOBAL=4250019372509.81.1643690508685; ALF=1677760612; SCF=AuDijIALd6BtLiIjY9Hv_QKnKT40eNSMx4qa4ReyaqmX2f5wz4UGtcITrq24ZzSyXSnAQMY1-KA4vb5dQ9HJvlo.; SUB=_2A25PJEAoDeRhGeBK61MW-C3KwzWIHXVs52BgrDV8PUJbkNAKLRX5kW1NR-GaOmnj9j84Fvh1skaG7lzSqFAZkWHa; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZQoeED-AfigYnRCRfUBOo5NHD95QcSh5pS0n0Son4Ws4Dqcj.i--fi-zNi-8Fi--fi-2EiKL8i--fi-88iKL8i--Xi-i2iK.0; XSRF-TOKEN=47DLsU0C70cDP4Mec20bcytu; _s_tentry=weibo.com; Apache=5076152925347.95.1647425375820; ULV=1647425375924:7:5:1:5076152925347.95.1647425375820:1646470709426; WBPSESS=QthxJZxbtrFOjmf8V9vUmYNjnmRp9ZlDk_7L2i4bTK7reGLjj0GJnDmo1ZL8dWe3zVW0AYJQU1YirTa8oiXFpIJiOWE-Vz45Mdabit_ztqDbVfRTDB76eZ1i2xSTbfe4n-8AcZAXkKJ9-L6OeL8KNg=='''
}

class WeiboCommentScrapy(Thread):

    def __init__(self,wid):
        global headers
        Thread.__init__(self)
        self.headers = headers
        self.result_headers = [
            '评论者主页',
            '评论内容',
        ]
        if not os.path.exists('comment'):
            os.mkdir('comment')
        self.wid = wid
        self.start()


    def get_one_comment_struct(self,comment):
        # xpath 中下标从 1 开始
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content)==0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content)==0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':')+1:]
        else:
            content = content[0]




        return [content]

    def write_to_csv(self,result,isHeader=False):
        with open('comment/' + self.wid + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if isHeader == True:
                writer.writerows([self.result_headers])
            writer.writerows(result)
            print('已成功将{}条评论写入{}中'.format(len(result),'comment/' + self.wid + '.csv'))

    def run(self):
        res = requests.get('https://weibo.cn/comment/{}'.format(self.wid),headers=self.headers,verify=False)
        commentNum = re.findall("评论\[.*?\]",res.text)[0]
        commentNum = int(commentNum[3:len(commentNum)-1])
        #        print(commentNum)
        pageNum = ceil(commentNum/10)
        #        print(pageNum)
        for page in range(pageNum):

            result = []

            res = requests.get('https://weibo.cn/comment/{}?page={}'.format(self.wid,page+1), headers=self.headers,verify=False)

            html = etree.HTML(res.text.encode('utf-8'))

            comments = html.xpath("/html/body/div[starts-with(@id,'C')]")

            print('第{}/{}页'.format(page+1,pageNum))

            for i in range(len(comments)):
                result.append(self.get_one_comment_struct(comments[i]))
                print(self.get_one_comment_struct(comments[i]))


            if page==0:
                self.write_to_csv(result,isHeader=True)
            else:
                self.write_to_csv(result,isHeader=False)
            sleep(1)


if __name__ =="__main__":
    #宝宝，把下面这个wid换成想要爬取的评论页面的对应数据
    #这里我想爬取https://weibo.com/1974576991/Lk1DR1BF2
    #就填入Lk1DR1BF2
    WeiboCommentScrapy(wid='Lk1DR1BF2')
    #这个程序会漏掉一部分，不过大部分数据都能够爬取

