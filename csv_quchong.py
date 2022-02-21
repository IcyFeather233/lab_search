import csv
import pandas as pd

def step6(filename):
    csv.field_size_limit(500 * 1024 * 1024)
    # columns=['标题', '作者', '朝代', '原文', '目标句子', '点赞数', '翻译', '注释', '赏析']
    all_lines = []

    originfile = open('data/csv_' + filename[:-3] + 'csv', 'r', encoding='utf-8')

    reader = csv.reader(originfile, )
    rows = [row for row in reader]

    sum = len(rows)
    cur_num = 0

    for each in rows[1:]:
        cur_num += 1
        print(each)
        # 跳过空行
        if len(each) == 0:
            continue
        print('当前是第' + str(cur_num) + '行，进度为' + str(1.0 * cur_num / sum))
        print(each)
        # 4 是原文, 5 是目标句子
        if ('span' in each[4]) or each[4] == '':
            continue
        each_content = each[5].replace('|', '').strip()
        print(each_content)
        isRepeat = False
        index = 0
        for e in all_lines:
            e_content = e[4].replace('|', '').strip()
            print("each content: " + each_content)
            print("e content: " + e_content)
            if each_content == e_content:
                isRepeat = True
                break
            index += 1
        if not isRepeat:
            print('这首诗没有重复')
            all_lines.append(each[1:])
        else:
            print('这首诗重复了')

    for e in all_lines:
        print(e)
    save = pd.DataFrame(columns=['标题', '作者', '朝代', '原文', '目标句子', '点赞数', '翻译', '注释', '赏析'], index=None, data=all_lines)
    fh = open('data/去重' + filename[:-3] + '.csv', 'w+', encoding='utf-8')
    save.to_csv(fh)
    fh.close()


# step6("“约么”，用古诗如何委婉的表达？.txt")