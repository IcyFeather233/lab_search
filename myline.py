import re


def washdata(line):
    nosign = re.sub(r'[0-9]+', '', line)
    allsign = "《》——-<>（）()"

    for i in allsign:
        nosign = nosign.replace(i, '')
    #
    # print("去掉奇怪符号之后：")
    # print(nosign)

    allparts = re.split(r'[.,:，。！|、；@#￥%：？!?\s]\s*', nosign)

    longger_than_5 = []

    # 选取长度 >=5 的
    for e in allparts:
        if len(e) >= 5:
            longger_than_5.append(e)

    #
    # print("分割之后：")
    # print(allparts)
    return longger_than_5

# washdata("花径不曾缘客扫，蓬门今始为君开。")
