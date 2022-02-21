# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

sentence = '怀旧空吟闻笛赋<span style="color:#518564;">(fù)</span>，到乡翻似烂柯<span style="color:#518564;">(kē)</span>人。'

temp_soup = BeautifulSoup(sentence, 'html.parser')
for tag in temp_soup.find_all("span", {'style': 'color:#518564;'}):
    tag.replaceWith('')
print(temp_soup.get_text())