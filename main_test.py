# 月上柳梢头，人约黄昏后。

import re
import myline
import mysearch
import mypoem

filename = "test.csv"
filepath = "res/" + filename

fin = open(filepath, encoding='utf-8')

line = fin.readline()
isfirst = True

while line:
    data = myline.washdata(line)

    for e in data:
        if e != '':
            print(e)
            ms = mysearch.MySearch(e)
            linkdata = ms.search()
            if linkdata[0]:
                link = linkdata[1]
                print(link)
                mypoem.crawl_the_poetry(link, e, filename)
            print("-------------")

    line = fin.readline()

fin.close()
