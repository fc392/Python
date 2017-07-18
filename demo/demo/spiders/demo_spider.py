from scrapy.spider import Spider

class DemoSpider(Spider):
    name='demo'
    allowed_domains=["http://www.people.com.cn/"]
    start_urls=["http://paper.people.com.cn/rmrb/html/2017-07/18/nw.D110000renmrb_20170718_1-01.htm"]

    def parse(self,response):
        filename=response.url.split("/")[6:8]
        open(filename,'wb').write(response.body)