import scrapy
import json
import tablib

class mispider(scrapy.Spider): 
      
    name = "goods_spider"

    def start_requests(self): 
        
        #待爬取的URL
        urls = [
            'https://www.xiaomiyoupin.com/homepage/main/v1002?platform=pc',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        goods = json.loads(response.body)
        data = []  #存放商品信息
        
        for floor in goods.get("data").get("homepage").get("floors"):
            items = floor.get("data").get("items")
            if items is not None :
                for item in items:
                    if item.get("gid") is not None:        #除去非商品item
                        body = []
                        body.append(item.get("gid"))       #商品id
                        body.append(item.get("name"))      #商品名
                        body.append(item.get("price_min")) #商品价格，最后两位为小数
                        data.append(tuple(body))
        #将信息存入Excel                
        header = tuple(["gid","name","price"])
        tbdata = tablib.Dataset(*data,headers=header)
        open('data.xls', 'wb').write(tbdata.xls)
