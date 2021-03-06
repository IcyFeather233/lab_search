import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.common.exceptions import NoSuchElementException
# from util.utils import getHTMLText

from lxml import etree

options = EdgeOptions()
options.use_chromium = True
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 浏览器的位置
driver = Edge(options=options, executable_path=r"D:\edgeDriver_win64\msedgedriver.exe")  # 相应的浏览器的驱动位置​


def crawl_the_poetry(url, target):  # 爬该首诗的所有信息
    # outputfile = open('./data/' + outfilename, mode='a', encoding='utf-8')
    try:
        driver.get(url)
        poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    except:
        print("3爬取失败")
        return

    try:
        if_chuzi = poetry_soup.select("#sonsyuanwen > div.cont > p")[0].text
        if "出自" in if_chuzi:
            trueurl = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(2)")[0].get('href')
            trueurl = "https://so.gushiwen.cn" + trueurl
            crawl_the_poetry(trueurl, target)
            return
    except:
        pass

    poetry_dict = {"诗名": "", "朝代": "", "作者": "", "原文": "", "翻译": "", "注释": "", "鉴赏": "", "新解": "", "创作背景": "", "目标句子": ""}
    # 找标题
    try:
        title = poetry_soup.select("#sonsyuanwen > div.cont > h1")[0].text
    except:
        print("no title")
        return
    print("标题：" + title)
    # outputfile.write("标题 " + title + "\n")
    poetry_dict['诗名'] = title
    author = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(1)")[0].text
    print("作者：" + author)
    # outputfile.write("作者 " + author + "\n")
    poetry_dict['作者'] = author
    dynasty = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(2)")[0].text[1:-1]
    print("朝代：" + dynasty)
    # outputfile.write("朝代 " + dynasty + "\n")
    poetry_dict['朝代'] = dynasty
    # 原文
    temp_content1 = poetry_soup.select("#sonsyuanwen > div.cont > div.contson")[0]
    temp_content2 = str(temp_content1)[47:-11].strip().replace("<p>", "").replace("</p>", "|").replace("<br/>", "|").replace("\n", "")
    # 把括号去掉
    no_bracket_content = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", temp_content2)
    content = no_bracket_content + "|"
    print("原文：" + content)
    # outputfile.write("原文 " + content + "\n")
    # 用原文的分割来找目标句子，文件处理完了再对文件用目标句子去重就行
    content_match_list = content.split("|")
    print(content_match_list)
    for e in content_match_list:
        if target in e.replace("？", "").replace("！", "").replace("：", ""):
            poetry_dict['目标句子'] = e
            print("目标句子：" + poetry_dict['目标句子'])
    # outputfile.write("目标句子 " + poetry_dict['目标句子'] + "\n")
    # 译文
    try:
        input = driver.find_element_by_xpath('//*[@alt="译文"]')
        input.click()
    except:
        print("没有译文按钮")

    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    raw_yiwen = poetry_soup.select("#sonsyuanwen > div.cont > div.contson > p > span")
    yiwen = ""
    for each in raw_yiwen:
        yiwen += each.text + "|"
    print("译文：" + yiwen)
    # outputfile.write("译文 " + yiwen + "\n")
    # 注释
    try:
        input = driver.find_element_by_xpath('//*[@alt="注释"]')
        input.click()
    except:
        print("没有注释按钮")

    # 取消掉
    try:
        input = driver.find_element_by_xpath('//*[@alt="译文2"]')
        input.click()
    except:
        print("没有取消译文按钮")

    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    raw_zhushi = poetry_soup.select("#sonsyuanwen > div.cont > div.contson > p > span")
    zhushi = ""
    for each in raw_zhushi:
        zhushi += each.text + "|"
    print("注释：" + zhushi)
    # outputfile.write("注释 " + zhushi + "\n")
    # 点开“展开阅读全文”
    try:
        buttons = driver.find_elements_by_link_text("展开阅读全文 ∨")
        for button in buttons:
            button.click()
    except:
        print("没有展开全文按钮")

    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    hide_list = poetry_soup.select("div.main3 > div.left > div.sons > div.contyishang")

    all_hide_tags = []
    for each in hide_list:
        if (each.span.text not in all_hide_tags):
            if (each.span.text != '译文及注释'):
                all_hide_tags.append(each.span.text)
    print(all_hide_tags)

    for each in all_hide_tags:
        output = ""
        for e in hide_list:
            if (e.span.text == each):
                if (e.span.text[:2] == "译文"):
                    output = str(e.text)[5:].strip()
                    continue
                each_pList = e.select('p')
                for p in each_pList:
                    output += p.text.strip()
        print(each + " " + output)
    #     outputfile.write(each + " " + output + "\n")
    #
    # outputfile.write("\n")
    # outputfile.close()

# crawl_the_poetry("https://so.gushiwen.cn/guwen/bookv_46653FD803893E4F90F0E5E10F25A1E5.aspx", "愿修燕好")

