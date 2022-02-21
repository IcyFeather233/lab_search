import re

def step2(filename):
    fileHandler = open("data/" + filename, "r", encoding='utf-8')
    all_line = []

    while True:
        # Get next line from file
        line = fileHandler.readline()
        # If line is empty then end of file reached
        if not line:
            break
        # print(line.strip())
        s = line[:2]
        new_line = line
        if s == '注释' or s == '翻译':
            new_line = re.sub(u"\\(.*?\\)|\\{.*?\\}|\\[.*?\\]|\\<.*?\\>", "", line)
            new_line = ''.join(new_line.split('|'))
            for i in range(len(new_line)):
                # 检测到:
                if new_line[i] == '：':
                    j = 1
                    front = i-j
                    while front >= 0:
                        if new_line[front] == '。':
                            str1 = new_line[:front]
                            str2 = new_line[front+1:]
                            new_line = str1 + '|' + str2
                            break
                        elif new_line[front] == '，':
                            break
                        j = j + 1
                        front = i - j
            new_line = new_line.replace('|', '。|')
        new_line = new_line.replace('|”', '”|')
        new_line = new_line.replace('。。', '。')
        all_line.append(new_line)

    fileHandler.close()

    new_file = open('data/new_' + filename, 'w', encoding='utf-8')
    for line in all_line:
        new_file.write(line)
    new_file.close()
