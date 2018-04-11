# -*- coding:utf-8 -*-
import re
import sys
import requests
import time
import os
from lxml import etree
from xlwt import *
import numpy as np
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')

"""cookies = {
    "__jda=122270672.372601625.1508901534.1508912320.1508915999.4
	"unpl=V2_ZzNtbRZRFBF1CENRKRheB2IEEQgRURAQIV1CBngRCVEzAkJVclRCFXMURlVnGlgUZwcZXkFcQBNFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJARVVS1ZDFnMPQlVLKV8FVwMTbUBRQBJ0CEFXfylsAlczIllFVUMcdDhHZHopHlE7BxpdR1FLWHcORVN6GVsGYzMTbUE%3d
	"__jdc=122270672
	"__jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|36980127650_0_e7f51144c033462db7b4ed5c29dee0a9|1508916147690
	"__jdu=372601625
	"qr_t=c
	"alc=AspBriwKOVVtHLa46F/Otw==_t=tWDDrYVzFDELFmXkx8xQVeXiNDYOM3iyhBAI/bSAYV0=
	"TrackID=1UnHaNsWpe9LdGIT7vMp1yQsCI2b4r_aFx-XQ6ec0hJcSm1dqUjbfMStN9Udo0TOtf0rDTJgEtlZZPxMk66Nz33sf2Fi6hbMgYnHj9NXuemfCi43fCeyM5c6KpQHRiuu7
	"pinId=1MiwrqzMKfHDs_aMNtMWZQ
	"pin=18810922035_p
	"thor=6D39AD3A6C86DF5BBFC4578B96E0792AFE781556CA6B23349064880ED3FFB4B5F5309F1B5FD35FFE8C997E69ED49669F8D147C00C7343C4B64E566D4DCCDD07A4C66C04A49E51999C4007E6AFA770BEA6FDB73551287A91BB67A654E6D21CCBBAC6F74FD6BAE9D88A0AF3C41B41B3E461E722B94E9BB190DD2227A2B48BE56BCBF0DB733377EB3452B1851DEE375DCA0
	"ol=1
	"_tp=q7EZn%2BUo8bONh1L2ntpmbA%3D%3D
	"_pst=18810922035_p
	"ceshi3.com=000
	"ipLoc-djd=53283-53309-0-0
	"3AB9D23F7A4B3C9B=VB26BPRZ4RBJP4LFKDH4C2CHLA4ZAZV5JSHACWXVTEWNWJO4YH23VRVO76KF6377WUB6GHP4FWN73X634VLOK5EZSQ
	"__jdb=122270672.7.372601625|4.1508915999
	"CCC_SE=ADC_bDQRiJdPNp0ljZ1HB%2fivbJN72QayfHnj4VIn4c33ok%2bJ4xeD9YfNuOAeiA4HT5gqxT0pALi6LfwNBD64nzJ1A2LsL7jjoW7b6QNeViwacjZi6UkXOaqtLMbB4403S3asv2ClCAjbZ7LG2ehF9qTRJsfmI7xomo2G11anxKVXDmEnw0YuygAt%2f9qsy5vpVeSgOZDm6xwNg4xAC958ofFQGO92elkX5uIb9varSPqBHEC6sz4ZO29Oip1kmjPIOKfhBmlV%2bFDbznKrLZbSsK4y%2bfHokW2IThdxf5YkjFtY3fMtNgcxkOUfc8tjZdaNxnrpZVn265DcGLUW9J9eU7lEoj%2f3LZK239%2fGuZ%2b0Ps7R%2flx9yAHj3AP5wnMdmyJOYArRUmxrueGeZYHWRaJyUXY6x27oFe9PzijpvE1zaEJwqSxn0L%2bPtcznKyWBAtEoQDKO6vO1uawqVvnlWlnunROEHev590c1QBycH8jpr9cu4yNdYUW3CZkIK2%2bBDksK3O9%2b"}
"""
class JD:
    cookie = {'TrackID': '1_VWwvLYiy1FUr7wSr6HHmHhadG8d1-Qv-TVaw8JwcFG4EksqyLyx1SO7O06_Y_XUCyQMksp3RVb2ezA',
              '__jda': '122270672.1507607632.1423495705.1479785414.1479794553.92',
              '__jdb': '122270672.1.1507607632|92.1479794553',
              '__jdc': '122270672',
              '__jdu': '1507607632',
              '__jdv': '122270672|direct|-|none|-|1478747025001',
              'areaId': '1',
              'cn': '0',
              'ipLoc-djd': '1-72-2799-0',
              'ipLocation': '%u5317%u4EAC',
              'mx': '0_X',
              'rkv': 'V0800',
              'user-key': '216123d5-4ed3-47b0-9289-12345',
              'xtest': '4657.553.d9798cdf31c02d86b8b81cc119d94836.b7a782741f667201b54880c925faec4b'}

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Connection': 'close',
        'Referer': 'https://www.jd.com/'
    }

    def __init__(self):
        self.file1 = Workbook(encoding = 'utf-8')
        self.table1 = self.file1.add_sheet("%s.xls" % "联想 IdeaPad 110-15")
        self.productIdSet = set()
        self.word_count = 1

    def getProductId(self):

        url = 'https://search.jd.com/Search?keyword=%E8%81%94%E6%83%B3%20IdeaPad%20110-15&enc=utf-8'
        request = requests.session()
        request.keep_alive = False
        html = request.get(url, cookies=JD.cookie, headers=JD.header).content
        selector = etree.HTML(html)
        print 'Get homepage successfully!'

        productIds = selector.xpath('//li[@class="gl-item"]/@data-sku')
        for i in productIds:
            i = int(i)
            print i
            self.productIdSet.add(i)
    """def getComment(self,productId):
        table_line = 0 
        url = 'https://item.jd.com/%d.html'% productId
        request = requests.session()
        request.keep_alive = False
        html = request.get(url, cookies=JD.cookie, headers=JD.header).content
        print html
        selector = etree.HTML(html)
        info = selector.xpath('//div[@class="comment-percent"]')
        print info"""
    def getComment(self,productId):
        data = {
            'productId': str(productId),
            'score': '0',
            'sortType': '5',
            'page': '0',
            'pageSize': '10',
            'isShadowSku': '0'
        }
        s = os.getcwd()
        s = s + "\\" + str(productId) +".txt"
        print s,type(s)
        newfile = file(s , 'w')
        url = 'https://club.jd.com/comment/productPageComments.action'
        for pagenum in range(100):
            data['page'] = pagenum
            response = requests.get(url, data, cookies=JD.cookie, headers=JD.header).content
            #html = str(reponse).encode('gbk')
            time.sleep(1)
            newfile.write(response)
            print pagenum
        newfile.close()

    def cleanData(self, productId):
        s = os.getcwd()
        s = s + "\\" + str(productId) + ".txt"
        html = open(s, 'r').read()
        userClient = re.findall(r',"usefulVoteCount".*?,"userClientShow":(.*?),', html) #用户购买商品时使用的媒介，手机客户端还是电脑端
        userLevel = re.findall(r'"referenceImage".*?,"userLevelName":(.*?),', html)     #用户等级
        productColor = re.findall(r'"creationTime".*?,"productColor":(.*?),', html)     #产品型号
        productSize = re.findall(r'"creationTime".*?,"productSize":(.*?),', html)
        recommend = re.findall(r'"creationTime".*?,"recommend":(.*?),', html)           #是否推荐
        nickname = re.findall(r'"creationTime".*?,"nickname":(.*?),', html)             #用户名
        userProvince = re.findall(r'"referenceImage".*?,"userProvince":(.*?),', html)   #用户所在地
        usefulVoteCount = re.findall(r'"referenceImage".*?,"usefulVoteCount":(.*?),', html)  # 使用正则提取days字段信息
        days = re.findall(r'"usefulVoteCount".*?,"days":(.*?)}', html)                  #时间
        score = re.findall(r'"referenceImage".*?,"score":(.*?),', html)                 #使用正则提取score字段信息

        isMobile = re.findall(r'"usefulVoteCount".*?,"isMobile":(.*?),', html)          #是否为手机端客户
        mobile = []
        for m in isMobile:
            n = m.replace('}', '')
            mobile.append(n)            #再次清洗mobile数据

        creationTime1 = re.findall(r'"creationTime":(.*?),"referenceName', html)        #创建评论的时间
        creationTime = []
        for d in creationTime1:
            date = d[1:20]
            creationTime.append(date)    #再次清洗时间数据

        content = re.findall(r'"guid".*?,"content":(.*?),', html)                       #评论内容
        content_1 = []
        for i in content:
            if not "img" in i:
                content_1.append(i)      #排除掉所有包含图片的评论信息，已达到评论去重的目的。

        """table = pd.DataFrame(
            {'creationTime': creationTime, 'nickname': nickname, 'productColor': productColor,
             'productSize': productSize, 'recommend': recommend, 'mobile': mobile, 'userClient': userClient,
             'userLevel': userLevel, 'userProvince': userProvince, 'usefulVoteCount': usefulVoteCount,
             'content_1': content_1, 'days': days, 'score': score})"""
        print "creationTime ", len(creationTime)
        print "nickname ", len(nickname)
        print "productClolor ", len(productColor)
        print 'productSize ',  len(productSize)
        print 'recommend ', len(recommend)
        print 'mobile ', len(mobile)
        print 'userClient ',  len(userClient)
        table = pd.DataFrame(
            {'creationTime': creationTime, 'nickname': nickname, 'productColor': productColor,
             'productSize': productSize, 'recommend': recommend, 'mobile': mobile, 'userClient': userClient,
             'userLevel': userLevel, 'userProvince': userProvince, 'usefulVoteCount': usefulVoteCount,
             })
        # 将creationTime字段更改为时间格式
        table['creationTime'] = pd.to_datetime(table['creationTime'])
        # 设置creationTime字段为索引列
        table = table.set_index('creationTime')
        # 设置days字段为数值格式
        table['days'] = table['days'].astype(np.int64)
        table.to_csv('jd_table.csv')

        print userClient, userLevel

    def start(self):
        #try:
            #JD.getProductId(self)
            #JD.getComment(self,10582094283)
            JD.cleanData(self, 10582094283)
        #except Exception, e:
        #   print "Error1: ", e


if __name__ =="__main__":
    JD().start()
