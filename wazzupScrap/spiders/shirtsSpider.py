import scrapy
from ..items import QuotescrapItem
class ShirtsSpider(scrapy.Spider):
    name = 'shirts'
    start_urls = ['https://inyourshoe.com/collections/t-shirts/?section_id=template--19419656028381__main&page=1']
    allowed_domains = ["inyourshoe.com"]
    page = 2

    
    # def start_requests(self):
    #     url = 'https://inyourshoe.com/collections/t-shirts/?section_id=template--19419656028381__main&page=1'
    #     yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        items = QuotescrapItem()
        all_shirts = response.css('.m-product-item')
        for shirt in all_shirts:
            name = shirt.css('.m-product-card__name::text').get().strip()
            price = shirt.css('span.money::text').get().replace("EGP","").replace(",","").strip()
            price = price.replace("EGP","")
            productLink = "inyourshoe.com" + shirt.css('.m-product-card__name::attr(href)').get()
            imageLink = shirt.css('.m-product-card__main-image img::attr(src)').get()
            imageLink = "https:" + imageLink  
            print("Image LINK: ", imageLink)

            items['name'] = name
            items['price'] = price
            items['productLink'] = productLink
            items['image_urls'] = [imageLink]
            yield items
        


        load_more = response.css('button[data-load-more] > span::text').extract()
        print("Load More: ", load_more)


        next_page = 'https://inyourshoe.com/collections/t-shirts/?section_id=template--19419656028381__main&page='+str(ShirtsSpider.page)
        print("NEXT PAGE: ", next_page)


        # if(load_more):
        #     ShirtsSpider.page+=1
        #     yield response.follow(next_page, callback = self.parse)


        # next_page = 'https://quotes.toscrape.com/page/'+str(QuoteSpider.page_number)+'/'

        # if QuoteSpider.page_number < 11:
        #     QuoteSpider.page_number+=1
        #     yield response.follow(next_page, callback = self.parse)