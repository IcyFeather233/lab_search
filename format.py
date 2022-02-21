def step3(filename):
    f = open("data/new_" + filename, 'r', encoding='utf-8')

    all_tags = ['标题', '作者', '朝代', '原文', '目标句子', '点赞数', '译', '析', '注', '释', '赏', '创作背景', '诗名']
    all_line = []

    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n' or line == '\r' or line == '\n\r' or line == '\r\n':
            all_line.append(line)
        tag = line.split(' ')[0].split('　')[0]
        if len(tag) > 10 and (tag[:2] == '译文' or tag[:2] == '注释'):
            true_tag = tag[:2]
            line = true_tag + ' ' + tag[2:]
        for e in all_tags:
            if e in tag:
                all_line.append(line)
                break

    f.close()

    new_file = open('data/new1_' + filename, 'w', encoding='utf-8')
    for line in all_line:
        new_file.write(line)
    new_file.close()


