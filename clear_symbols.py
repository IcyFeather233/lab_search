def step4(filename):
    f = open("data/new1_" + filename, 'r', encoding='utf-8')

    all_tags = ['▲', '%', '&', '$', '￥', '#', '@', '\u3000', '0', '1', '3', '4', '5', '6', '7', '8', '9', u'\xa0', '&nbsp;']
    all_line = []

    while True:
        line = f.readline()
        if not line:
            break
        for each in all_tags:
            line.replace(each, '')
        all_line.append(line)

    f.close()

    new_file = open('data/new2_' + filename, 'w', encoding='utf-8')
    for line in all_line:
        new_file.write(line)
    new_file.close()