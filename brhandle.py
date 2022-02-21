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
    pathDir = os.listdir(filepath)      #获取当前路径下的文件名，返回List
    for s in pathDir:
        newDir=os.path.join(filepath,s)     #将文件命加入到当前文件路径后面
        if os.path.isfile(newDir) :         #如果是文件
            if os.path.splitext(newDir)[1]==".csv":  #判断是否是txt
                file_list.append(newDir)
                pass
        else:
            eachFile(newDir)                #如果不是文件，递归这个文件夹的路径

def handle_one_file(filename):
    filepath = "data/去重" + filename[:-3] + '.csv'

    # 创建文件
    new_file = open("data/最终去重" + filename, 'w', encoding='utf-8')

    f = open(filepath, encoding='utf-8')

    line = f.readline()

    while line:
        new_line = line.replace('<br/>', '')
        new_file.write(new_line)
        line = f.readline()

    f.close()
    new_file.close()


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