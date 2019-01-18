from urllib import request
import re


class Spider():
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '<span class="video-nickname" title="([\s\S]*?)">'
    number_pattern = '<i class="ricon ricon-eye"></i>([\s\S]*?)</span>'

    def __fetch_content(self):  # 获取网页内容
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8',)
        return htmls

    def analysis(self, htmls):
        anchors = []
        root_htmls = re.findall(Spider.root_pattern, htmls)
        for html in root_htmls:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        l = lambda  anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0].strip()
        }
        return map(l, anchors)

    def __sorted(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def show(self, anchors):
        i = 0
        for anchor in anchors:
            i +=1
            print(str(i)+'号主播 '+anchor['name']+'   的人气为：'+anchor['number'])

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors =self.__sorted(anchors)
        self.show(anchors)


spider = Spider()
spider.go()
