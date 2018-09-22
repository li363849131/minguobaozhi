#coding:utf-8
import urllib2
import urllib
from HTMLParser import HTMLParser
import Queue,threading
import time
import os,sys
import re
import codecs
import random

print "lijie"
#url1= "http://bz.nlcpress.com/library/publish/default/PaperSearch.jsp?paperName=&pubDate=&keyword=%E7%BA%A2%E5%8D%81%E5%AD%97&content=&topic=&author=&layoutNum=&layoutName=&column=&paperStartDate=&paperEndDate=&searchScope=6&curPageNum="
#url2 = "&paperScope=&search=0&searchorder=3&paperVolume=&searchfield=-1&searchtype=2&searchsynonym=2&searchmatch=1&pagesize=50&fileType=-1&contentfilter=-1"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

headers = { 'Host':'bz.nlcpress.com',
                    'Connection':'keep-alive',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                    'Referer': 'http://bz.nlcpress.com/library/publish/default/paperDocView_pic.jsp?docID=2374108&docLibID=30&dydocID=null&dydocLibID=null&keyword=%25E7%25BA%25A2%25E5%258D%2581%25E5%25AD%2597&searchmatch=1&searchsynonym=2&userID=91',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9'
}
data = None



keyword_input = u"红十字"
lisfilename = "crossredlist.txt"
findexSavefilename = "currentindex.txt"

#1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
browser = webdriver.Chrome(executable_path ="D:\code\laopo\RecentPaperRedCross\chromedriver")

#2.通过浏览器向服务器发送URL请求
#browser.get(url1+"1"+url2)
browser.get("http://bz.nlcpress.com/library/publish/default/Login.jsp")

sleep(1)

#3.刷新浏览器
browser.refresh()
#4.设置浏览器的大小
browser.set_window_size(800,600)

#sleep(1)


#dr.find_element_by_id("kw")
#driver.find_element_by_name("account").send_keys('123456789')
 
element=browser.find_element_by_id("UserCode")
element.send_keys("minguobaozhi")

element=browser.find_element_by_id("UserPassword")
element.send_keys("nlcpress")
element.send_keys(Keys.RETURN)

#element=browser.find_element_by_link_text("登录")
#element.click()
sleep(1)


browser.find_element_by_class_name("inp_srh").send_keys(keyword_input)
browser.find_element_by_class_name("inp_srh").send_keys(Keys.RETURN)

browser.switch_to.window(browser.window_handles[-1])
sleep(1)

e1 = browser.find_element_by_xpath("//div/div/div[@class='search-oper']")
e2 = e1.find_elements_by_tag_name("p")[0]
#change pagesize to 50
e3 = e2.find_elements_by_tag_name("span")[2].click()

#sort by year
y1 = browser.find_element_by_class_name("cur-date-order")
y1.click()

#raise "123"

#print re.findall(r"right-oper right", browser.page_source)
#browser.refresh()
#sleep(1)
#e2 = e1.find_element_by_class_name(u"right-oper right")

#find total paper number
totalpapernumber = re.findall(ur"\u5171([\d]{1,8})\u7bc7", browser.page_source)
totalpapernumber = int(totalpapernumber[0])
print "total paper number :", totalpapernumber

#find the list page num
totalpagenum = totalpapernumber/50 if totalpapernumber%50 ==0 else totalpapernumber/50+1
print "total page number :", totalpagenum
#print totalpagenum

total_index = 1

if os.path.exists(lisfilename) == False:
    fguo = codecs.open(lisfilename,'w+','utf-8')
    fguo.close()

findexSave_index = 1
if os.path.exists(findexSavefilename) == True:
    findexSave = open(findexSavefilename)
    findexSave_data = findexSave.read()
    findexSave_index = int(findexSave_data)
    findexSave.close()
else:
    findexSave = open(findexSavefilename,"w")
    findexSave.write("1")
    findexSave_index = 1
    findexSave.close()

#print findexSave_index
#raise "123"

for i in range(1, totalpagenum+1):
#for i in range(1, 2):
    #t1 = browser.find_elements_by_class_name("newsList02 clearfix")
    #find all tr, that is one records.
    t1 = browser.find_elements_by_xpath("//div[@class='clearfix']/div/div[@class='newsList02 clearfix']")
    recordsNum = len(t1)
    print "page%d have %d records"%(i, len(t1))

    for j in range(recordsNum):
        # get value of findexSave_index
        findexSave = open(findexSavefilename)
        findexSave_data = findexSave.read()
        findexSave_index = int(findexSave_data)
        findexSave.close()

        print "current_page : ", i
        if total_index >= findexSave_index:
            t2 = t1[j].find_elements_by_tag_name("li")
            #get record title
            t3 = t2[0].find_element_by_tag_name("p")
            recordsTitle = t3.text
            print "total index : %08d"%total_index
            print "recordsTitle : "+recordsTitle

            fguo = codecs.open(lisfilename,'a+','utf-8')        
            fguo.write("total index : %08d"%total_index+"\n")
            fguo.write("recordsTitle : "+recordsTitle+"\n")

            paperName = t2[1].find_elements_by_tag_name("a")[0].text
            paperData = t2[1].find_elements_by_tag_name("a")[1].text
            paperVersion = t2[1].find_elements_by_tag_name("a")[2].text

            fguo.write("    paperName : "+paperName+"\n")
            fguo.write("    paperData : "+paperData+"\n")
            fguo.write("    paperVersion : "+paperVersion+"\n")
            fguo.write("    image file : "+"%08d.png"%total_index+"\n")
            fguo.write("\n")
            fguo.close()

            print paperName, paperData, paperVersion
            print ''

            #open the record
            t4 = t2[0].find_element_by_tag_name("a")
            t4.click()
            #change to new explore
            browser.switch_to.window(browser.window_handles[-1])
            sleep(1)
            #save the image
            largeImage = browser.find_element_by_id("largeImage")
            srclink =  largeImage.get_attribute('src')
            reflink = browser.current_url

            #print srclink
            #print reflink

            headers["Referer"] = reflink
            #print headers

            req = urllib2.Request(srclink, data, headers)
            try_get_image_times = 10
            
            while(try_get_image_times > 0):
                try:
                    print "current getting image file "+"data\%08d.png"%total_index
                    response = urllib2.urlopen(req)
                    imagedata = response.read()
                    try_get_image_times = 0
                except:
                    print "network error, sleep 20 seconds, then try again."
                    sleep(20)
                    try_get_image_times = try_get_image_times - 1
            #print len(html)
            
            f1 = open("data\%08d.png"%total_index, "wb")
            f1.write(imagedata)
            f1.close()
            #print "total_index", total_index
            total_index = total_index + 1

            # save value of findexSave_index
            findexSave = open(findexSavefilename,"w")
            findexSave.write(str(total_index))
            findexSave.close()
        
            #print "total_index", total_index
            print "get done\n"
            sleep(1+3*random.random())
        
            browser.close()
            
            #return to list page
            browser.switch_to.window(browser.window_handles[-1])
        else:
            total_index = total_index + 1
    try:
        e6 = browser.find_element_by_class_name("next")
        e6.click()
    except:
        print "have done"
    

#e6 = browser.find_element_by_class_name("next")
#e6.click()

#e7 = browser.find_element_by_xpath("//div/div[@class='clearfix right']")
#e8 = e7.find_elements_by_tag_name("a")[0]

#element=browser.find_element_by_link_text("50")
#element.click()

#while(1):
#    element=browser.find_element_by_link_text("下一页")
#    element.click()
    



#browser.get(url1+"1"+url2)

#element=browser.find_element_by_class_name("newsList02 clearfix")
#print element

#browser.quit()


#5.设置链接内容
#element=browser.find_element_by_link_text("新闻")
#element.click()

#element=browser.find_element_by_link_text("习近平的“下团组”时间")
#element.click()
