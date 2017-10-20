import sys
from threading import Thread

import requests
import time
from lxml import etree
from xlwt import *

reload(sys)
sys.setdefaultencoding('utf-8')
WORKER_THREADS = 40
class weibo:
    cookie = {
        "Cookie": "T_WM=8dba2202a4d8675d36216a1c51ac94c1; SUB=_2A2504HY5DeRhGeNI7lIQ8ybIyDiIHXVUKxpxrDV6PUJbkdANLWbEkW1VkmE6c_P96fXrp1k9bP1OmVPsvA..; SUHB=0tKqglCfBqyxbX; SCF=AvfmKxlLor-F3CTrV9z66VkHzvUB0qtOOVgMpl2U36EWMwaUGPMmutDjZo4MEdOgfAkppVodujf_rraiuV1UNy8.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh_pqDwC2e_DnpobOaoaIe25JpX5oz75NHD95QfSo-7eKeRSheXWs4Dqcjdi--fi-88iKn4i--fiKnEiKnfi--fiKysi-zR; H5:PWA:UID=1; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4163402215727714%26luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; H5_INDEX=3; H5_INDEX_TITLE=%E5%AE%89%E5%82%85%E5%8F%B8; SSOLoginState=1508116073"
        }

    def __init__(self, user_id, filter_value):
        self.user_id = user_id
        self.filter_value = filter_value
        self.file1 = Workbook(encoding = 'utf-8')
        self.table1 = self.file1.add_sheet("%d.xls" % user_id)
        self.file2 = Workbook(encoding = 'utf-8')
        self.table2 = self.file2.add_sheet("%d_comment.xls" % user_id)
        self.urlComment_set = set()
        self.word_count = 1
        self.pageNum = 0

    def web_init(self):
        url = 'https://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter_value)
        request = requests.session()
        request.keep_alive = False
        html = request.get(url, cookies=weibo.cookie).content
        print 'Get homepage successfully!'
        selector = etree.HTML(html)
        # get total number of pages
        pageNum = selector.xpath('//input[@name="mp"]')[0].attrib['value']
        pageNum = int(pageNum)
        # --------------------!CAREFUL!-------------------
        page_start = 1
        page_end = pageNum
        pageNum = page_end - page_start + 1
        # --------------------!CAREFUL!-------------------
        self.pageNum = pageNum
        print 'Total number of pages = ', pageNum
        sys.stdout.flush()

    def words(self):
        sleep_between_pages = 1
        steps = 5
        one_step = self.pageNum / steps
        page_start = 1
        page_end = self.pageNum
        for step in range(0, steps):  # [0,steps-1]
            if step < steps - 1:
                i = step * one_step + page_start
                j = (step + 1) * one_step + page_start
            else:  # (step = steps - 1)
                i = step * one_step + page_start
                j = page_end + 1

            for page in range(i, j):
                # get lxml (I don't know why, probably to translate <br>, emojis, &amp; etc.)
                # and store all the texts and comments
                try:
                    url_page = 'https://weibo.cn/u/%d?filter=1&page=%d' % (self.user_id, page)
                    print url_page
                    #requests.adapters.DEFAULT_RETRIES = 5
                    request = requests.session()
                    request.keep_alive = False
                    html = request.get(url_page, cookies=weibo.cookie).content
                    # get text
                    selector = etree.HTML(html)
                    info = selector.xpath('//div[@class="tip2"]')
                    for each_info in info:
                        main_info = each_info.xpath('string(.)')
                        # table1.write(0, 3, main_info)
                        print "main_info finished"

                    # find all the <span> tags with class "ctt"
                    content = selector.xpath('//span[@class="ctt"]')  # content of weibo
                    content_time = selector.xpath('//span[@class="ct"]')
                    current_page_word = 0
                    for each in content:
                        text = each.xpath('string(.)')
                        time_str = content_time[current_page_word].xpath('string(.)')
                        print time_str
                        if self.word_count >= 3:
                            self.table1.write(self.word_count, 0, self.word_count - 2)
                            self.table1.write(self.word_count, 1, time_str)
                            self.table1.write(self.word_count, 2, text)
                        else:
                            self.table1.write(0, self.word_count, text)
                        current_page_word += 1
                        self.word_count += 1
                    print self.word_count
                    print page, 'text OK'

                    # RegExp to find all comment links in this page

                    comm_link = selector.xpath('//a[@class="cc"]/@href')
                    for each in comm_link:
                        each = each.split('&')[0]
                        self.urlComment_set.add(each)
                        # -------------------------------------------------------------------------------------------#
                except Exception, e:
                    print "Error1: ", e
                    print page, 'ERROR'

                print page, 'Sleep'
                time.sleep(sleep_between_pages)
            self.file1.save("%d.xls" % self.user_id)


    def comment(self):
        all_comment = 0
        try:
            for each_url in self.urlComment_set:
                print each_url
                #requests.adapters.DEFAULT_RETRIES = 5
                request = requests.session()
                request.keep_alive = False
                html_content = request.get(each_url, cookies=weibo.cookie).content
                selector_com_1 = etree.HTML(html_content)
                comment_page = selector_com_1.xpath('//input[@name="mp"]')[0].attrib['value']
                print "total page of comment " + comment_page

                comment_page = int(comment_page)
                comment_num = 0
                for i in range(1, comment_page + 1):
                    comm_url = each_url + '&page=%d' % i
                    print comm_url
                    request = requests.session()
                    request.keep_alive = False
                    html_comment = request.get(comm_url, cookies=weibo.cookie).content
                    selector_comment = etree.HTML(html_comment)
                    comm = selector_comment.xpath('//span[@class="ctt"]')
                    comm_time = selector_comment.xpath('//span[@class="ct"]')
                    current_page_comm = 0

                    for each_comm in comm:
                        each_comm = each_comm.xpath('string(.)')
                        comm_time_str = comm_time[current_page_comm].xpath('string(.)')
                        print comm_time_str
                        self.table2.write(all_comment, 0, all_comment)
                        self.table2.write(all_comment, 1, comm_time_str)
                        self.table2.write(all_comment, 2, each_comm)
                        print each_comm
                        current_page_comm =current_page_comm + 1
                        comment_num = comment_num + 1
                        all_comment = all_comment + 1
                    time.sleep(3)

        except Exception, e:
            print "Error2: ", e
        self.file2.save("%d_comment.xls" % self.user_id)

    def start(self):
        try:
            weibo.web_init(self)
            weibo.words(self)
            for i in range(WORKER_THREADS):
                t = Thread(target=weibo.comment(self))
                t.daemon = True
                t.start()
            print "end"
            print '==========================================================================='
        except Exception, e:
            print "Error3: ", e


wb = weibo(user_id = 2183473425, filter_value = 1)
wb.start()
