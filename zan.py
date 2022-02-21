

def zan_num(line, f):
    zan = "0"
    tf = f.tell()
    print("当前行的内容是：" + line)
    while line and (not line.replace('/r', '').replace('/n', '').strip().isdigit()):
        line = f.readline()
    zan = line
    f.seek(tf)
    return zan
