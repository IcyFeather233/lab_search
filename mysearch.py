import requests
from bs4 import BeautifulSoup


class MySearch(object):
    list = []
    url = 'https://so.gushiwen.cn/search.aspx?value='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
    targetlink = ""

    def __init__(self, target):
        self.target = target

    def search(self):
        text = requests.get(self.url + self.target, headers=self.headers).text
        soup = BeautifulSoup(text, 'html.parser')
        try:
            author = ""
            authorlist = soup.select(
                "div.sons:nth-child(5) > div:nth-child(1) > p:nth-child(3) > a:nth-child(1) > span")
            for e in authorlist:
                author += e.text
            if author == self.target:
                print("这行是诗人名，跳过")
                return [False, ""]
        except IndexError as e:
            # print("不是诗人名")
            pass

        try:
            title = soup.select("div.cont > p > a > b")[0].text.strip()
            if title == self.target:
                print("这是诗名，跳过")
                return [False, ""]
        except IndexError as e:
            # print("不是诗名")
            pass

        try:
            red = soup.select("span[style='color:#B00815;']")
            if len(red) == 0:
                red = soup.select("span[style='color:#B00815']")
            red = red[0].text
            # print(red)
            if red == self.target:
                print("完全匹配，这是一句诗")
                # print(self.target)
                link = soup.select("div.sons > div.cont > a")
                if len(link) == 0:
                    link = soup.select("div.sons > div.cont > p > a")
                link = link[0].get('href')
                # print(link)
                self.targetlink = "https://so.gushiwen.cn" + link
                # print(self.targetlink)
                return [True, self.targetlink]
        except IndexError as e:
            # print("啥也不是")
            pass
        return [False, ""]

#
mysearch = MySearch("此日别离卿可久")

data = mysearch.search()
print(data[0], data[1])
