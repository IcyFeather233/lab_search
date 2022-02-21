import pandas as pd



def step5(filename):
    f = open('data/new2_' + filename, 'r', encoding='utf-8')
    line = f.readline()
    sum = 0
    while True:
        if not line:
            break
        else:
            tag = line.split(' ')[0].split('　')[0]
            if tag == '诗名' or tag == '标题':
                sum += 1
            line = f.readline()

    f.close()
    print('共有' + str(sum) + '行。')

    title = ""
    author = ""
    dynasty = ""
    content = ""
    target = ""
    zan = ""
    translation = ""
    zhushi = ""
    shangxi = ""

    all_line = []

    cur_index = 0


    def init():
        global title
        global author
        global dynasty
        global content
        global target
        global zan
        global translation
        global zhushi
        global shangxi
        title = ""
        author = ""
        dynasty = ""
        content = ""
        target = ""
        zan = ""
        translation = ""
        zhushi = ""
        shangxi = ""


    f = open('data/new2_' + filename, 'r', encoding='utf-8')
    res = []
    # 标题 作者 朝代 原文 目标句子 点赞数 翻译 注释 赏析

    while True:
        line = f.readline()
        print(line)
        if not line:
            break
        # -----------------------------------
        tag = line.split(' ')[0].split('　')[0]
        temp = line.split(' ')[1:]
        # tag 后面的东西
        except_tag = ""
        for each in temp:
            except_tag += each.strip().replace('▲', '')
        # -----------------------------------
        if tag == '诗名' or tag == '标题':
            title = except_tag
            # print(title)
            line = f.readline()
            cur_index += 1
            print('当前第' + str(cur_index) + '首诗，进度： ' + str(1.0 * cur_index / sum))
            print(line)
            # -----------------------------------
            tag = line.split(' ')[0].split('　')[0]
            # print("tag: " + tag)
            temp = line.split(' ')[1:]
            except_tag = ""
            for each in temp:
                except_tag += each.strip().replace('▲', '')
            # print("except tag: " + except_tag)
            # -----------------------------------
            while True:
                if not line:
                    break
                if tag == '诗名' or tag == '标题':
                    csv_line = [title, author, dynasty, content, target, zan, translation, zhushi, shangxi]
                    print("csv_line： ")
                    print(csv_line)
                    all_line.append(csv_line)
                    init()
                    # global title
                    # global author
                    # global dynasty
                    # global content
                    # global target
                    # global zan
                    # global translation
                    # global zhushi
                    # global shangxi
                    title = ""
                    author = ""
                    dynasty = ""
                    content = ""
                    target = ""
                    zan = ""
                    translation = ""
                    zhushi = ""
                    shangxi = ""
                    f.seek(pointer)
                    break
                elif tag == '作者':
                    author = except_tag
                elif tag == '朝代':
                    dynasty = except_tag
                elif tag == '原文':
                    content = except_tag
                elif tag == '目标句子':
                    target = except_tag
                elif tag == '点赞数':
                    zan = except_tag
                elif tag == '翻译' or tag == '译文':
                    translation = except_tag
                elif tag == '赏析':
                    shangxi += except_tag + '|~|'
                elif tag == '注释':
                    zhushi += except_tag
                elif '及' in tag:
                    pass
                elif '释' in tag:
                    if (zhushi == ""):
                        zhushi += except_tag
                elif '析' in tag:
                    shangxi += except_tag + '|~|'
                elif '赏' in tag:
                    shangxi += except_tag + '|~|'
                pointer = f.tell()
                line = f.readline()
                print(line)
                tag = line.split(' ')[0].split('　')[0]
                temp = line.split(' ')[1:]
                except_tag = ""
                for each in temp:
                    except_tag += each.strip().replace('▲', '')
    f.close()

    save = pd.DataFrame(columns=['标题', '作者', '朝代', '原文', '目标句子', '点赞数', '翻译', '注释', '赏析'], index=None, data=all_line)
    fh = open('data/csv_' + filename[:-3] + "csv", 'w+', encoding='utf-8')
    save.to_csv(fh)
    fh.close()
