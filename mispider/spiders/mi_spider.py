import scrapy
import json
import tablib

class mispider(scrapy.Spider): 
      
    name = "goods_spider"

    def start_requests(self): 
        
        urls = [
            'https://www.xiaomiyoupin.com/homepage/main/v1002?platform=pc',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        goods = json.loads(response.body)
        data = []
        
        for floor in goods.get("data").get("homepage").get("floors"):
            items = floor.get("data").get("items")
            if items is not None :
                for item in items:
                    if item.get("gid") is not None:
                        body = []
                        body.append(item.get("gid"))
                        body.append(item.get("name"))
                        body.append(item.get("price_min"))
                        data.append(tuple(body))
                        
        header = tuple(["gid","name","price"])
        tbdata = tablib.Dataset(*data,headers=header)
        open('data.xls', 'wb').write(tbdata.xls)
