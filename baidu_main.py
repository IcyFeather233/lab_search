import os
import re
import myline
import mypoem as mypoem
import mysearch
import zan
import zs_fy
import format
import clear_symbols
import txt2csv
import csv_quchong
import multiprocessing

file_list = []


def eachFile(filepath):
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回List
    for s in pathDir:
        newDir = os.path.join(filepath, s)  # 将文件命加入到当前文件路径后面
        if os.path.isfile(newDir):  # 如果是文件
            if os.path.splitext(newDir)[1] == ".csv":  # 判断是否是txt
                file_list.append(newDir)
                pass
        else:
            eachFile(newDir)  # 如果不是文件，递归这个文件夹的路径


def handle_one_file(filename):
    filepath = "res/" + filename

    # 创建文件
    new_file = open("data/" + filename, 'w', encoding='utf-8')
    new_file.close()

    f = open(filepath, encoding='utf-8')

    line = f.readline()
    isfirst = True

    while line:
        if isfirst:
            # 这是分割行，下一行必是作者名，直接跳过
            line = f.readline()
            isfirst = False
            continue

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

        line = f.readline()

    f.close()

    # step 2
    zs_fy.step2(filename)

    # step3
    format.step3(filename)

    # step4
    clear_symbols.step4(filename)

    # step5
    txt2csv.step5(filename)

    # step6
    csv_quchong.step6(filename)


def main():
    pool = multiprocessing.Pool(processes=10)
    eachFile('res')
    # print(file_list)
    for each in file_list:
        e = each[4:]
        print("开启新进程：")
        print(e)
        pool.apply_async(handle_one_file, args=(e,))
    print("----分配结束------")
    pool.close()
    pool.join()
    print("----end-----")


if __name__ == '__main__':
    main()
