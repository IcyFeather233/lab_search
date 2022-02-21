# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions

options = EdgeOptions()
options.use_chromium = True

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')

options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 浏览器的位置
driver = Edge(options=options, executable_path=r"D:\edgeDriver_win64\msedgedriver.exe")  # 相应的浏览器的驱动位置​


def crawl_the_poetry(url, target, outfilename, zannum):  # 爬该首诗的所有信息
    outputfile = open('./data/' + outfilename, mode='a', encoding='utf-8')
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
            crawl_the_poetry(trueurl, target, outfilename)
            return
    except:
        pass

    poetry_dict = {"诗名": "", "朝代": "", "作者": "", "原文": "", "翻译": "", "注释": "", "鉴赏": "", "新解": "", "创作背景": "",
                   "目标句子": "", "点赞数": ""}

    poetry_dict['点赞数'] = zannum

    # 找标题 作者 朝代，如果没有大概率不是一般的诗句，属于误判，直接返回
    try:
        title = poetry_soup.select("#sonsyuanwen > div.cont > h1")[0].text
        print("标题：" + title)
        poetry_dict['诗名'] = title
    except:
        print("no title")
        return

    try:
        author = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(1)")[0].text
        print("作者：" + author)
        poetry_dict['作者'] = author
    except:
        print("no author")
        return

    try:
        dynasty = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(2)")[0].text[1:-1]
        print("朝代：" + dynasty)
        poetry_dict['朝代'] = dynasty
    except:
        print("no dynasty")
        return

    # 原文
    try:
        temp_content1 = poetry_soup.select("#sonsyuanwen > div.cont > div.contson")[0]
        temp_content2 = str(temp_content1)[47:-11].strip().replace("<p>", "").replace("</p>", "|").replace("<br/>",
                                                                                                           "|").replace(
            "\n", "")
        # 把括号去掉
        no_bracket_content = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", temp_content2)
        content = no_bracket_content + "|"
        print("原文：" + content)
    except:
        print("no content")
        return

    # 先把译文按钮点了再说
    try:
        input = driver.find_element_by_xpath('//*[@alt="译文"]')
        input.click()
        print("点了译文按钮")
    except:
        print("没有译文按钮")
        return

    try:
        input = driver.find_element_by_xpath('//*[@alt="注释"]')
        input.click()
        print("点了注释按钮")
    except:
        print("没有注释按钮")
        return

    # 寻找目标句子对应的原文段
    # 先只点译文按钮，记下来是第一个段落的，然后再点注释，不然注释的拼音会打乱原文
    is_sentence = False
    try:
        poetry_soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_yiwen_list = poetry_soup.select("#sonsyuanwen > div.cont > div.contson > p")
        for e in content_yiwen_list:
            print("e: " + str(e))
            reg = re.findall(r".*<p>(.*?)<br/>", str(e))

            if len(reg) > 0:
                print(reg)
                sentence = reg[0]

                temp_soup = BeautifulSoup(sentence, 'html.parser')
                for tag in temp_soup.find_all("span", {'style': 'color:#518564;'}):
                    tag.replaceWith('')

                sentence = temp_soup.get_text()
                print(sentence)

                if target in sentence.strip().replace("？", "").replace("！", "").replace("：", ""):
                    is_sentence = True
                    poetry_dict['目标句子'] = sentence
                    print("目标句子：" + poetry_dict['目标句子'])
                    # 找到了目标句子直接把对应译文也找到再说
                    yiwen = re.findall(r'.*<span style="color:#af9100;">(.*?)</span>', str(e))
                    if len(yiwen) > 0:
                        poetry_dict['译文'] = yiwen[0].replace('<br/>', '')
                    else:
                        poetry_dict['译文'] = ""
                    print("译文：" + poetry_dict['译文'])
                    # 顺便看看这一句有没有注释
                    zhushi = re.findall(r'.*<span style="color:#518564;">(.*?)</span>', str(e))
                    if len(zhushi) > 0:
                        a = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", zhushi[0])
                        poetry_dict['注释'] = a
                    else:
                        poetry_dict['注释'] = ""
                    print("注释：" + poetry_dict['注释'])

        if not is_sentence:
            print("no target sentence")
            return
    except:
        print("no target sentence")
        return

    outputfile.write("标题 " + title + "\n")
    outputfile.write("作者 " + author + "\n")
    outputfile.write("朝代 " + dynasty + "\n")
    outputfile.write("原文 " + content + "\n")
    outputfile.write("目标句子 " + poetry_dict['目标句子'] + "\n")
    outputfile.write("点赞数 " + poetry_dict['点赞数'] + '\n')
    outputfile.write("译文 " + poetry_dict['译文'] + "\n")
    outputfile.write("注释 " + poetry_dict['注释'] + "\n")

    # 最后找赏析
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
                    continue
                each_pList = e.select('p')
                for p in each_pList:
                    output += p.text.strip() + '|'
        print(each + " " + output)
        outputfile.write(each + " " + output + "\n")

    outputfile.write("\n")
    outputfile.close()


