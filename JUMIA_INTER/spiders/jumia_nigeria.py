import scrapy
from JUMIA_INTER.items import (JumiaInterItem, clean_discountrate, 
                     add_discount, clean_refurbished, 
                     is_flashsales, flash_remaintime, 
                     remain_items,get_seller, get_sellerfollowers,
                     get_breadlist, add_brand, get_sellerOrderRate, 
                     get_sellerscore, clean_stock)
from scrapy.loader import ItemLoader


class JumiaNigeriaSpider(scrapy.Spider):
    name = "jumia_nigeria"
    allowed_domains = ["jumia.com.ng"]
    start_urls = ["https://www.jumia.com.ng/"]
    
    cats_nig = ['groceries', 'health-beauty', 'home-office', 'phones-tablets', 
                    'computing', 'electronics', 'category-fashion-by-jumia', 
                    'baby-products', 'video-games', 'sporting-goods', 'automobile']

    def start_requests(self):
        url = self.start_urls[0]
        for cat in self.cats_nig:
            yield scrapy.Request(url=url+cat, callback=self.parse_listing_page)
    
    def parse_listing_page(self, response):
        product_urls = response.xpath("//div[contains(@class, '-pax')]//a[@class='core']//@href")
        for product_url in product_urls.extract():
            if product_url:
                yield scrapy.Request(response.urljoin(product_url), callback=self.parse_data)


        #pagination
        next_page_link = response.xpath("//a[@aria-label='Next Page']/@href")
        if next_page_link:
        # If there is a link to the next page, follow it and call this function recursively
            yield scrapy.Request(response.urljoin(next_page_link.extract_first()), callback=self.parse_listing_page)

    def parse_data(self, response):
        lang =  response.xpath("//html/@lang").get()
        if 'en' in lang:
            language = 'en'
            brand_xpath = "//div[contains(text(), 'Brand')]//following-sibling::a/text()"
            isflash_xpath = "//span[contains(text(), 'Flash Sales')]"
            flashtime_xpath = "//div[contains(text(), 'Time Left')]/time/text()"
            sellerorder_xpath = "//p[contains(text(), 'Order Fulfillment')]/span/text()"
            customerratings_xpath = "//p[contains(text(), 'Customer Rating')]/span/text()"
        else :
            language = 'fr'
            brand_xpath ="//div[contains(text(), 'Marque')]//following-sibling::a/text()"
            isflash_xpath = "//span[contains(text(), 'Ventes Flash')]"
            flashtime_xpath = "//div[contains(text(), 'Temps restant')]/time/text()"
            sellerorder_xpath = "//p[contains(text(), 'expédition')]/span/text()"
            customerratings_xpath = "//p[contains(text(), 'consommateurs')]/span/text()"
        
        stock_value = response.xpath("//p[@class='-df -i-ctr -fs12 -pbs -rd5']/text()").get()
        l = ItemLoader(item= JumiaInterItem(),response=response)
        l.add_xpath('siteName', '//meta[@property="og:site_name"]/@content')
        l.add_xpath('country', '//meta[@property="og:site_name"]/@content')
        l.add_value('language', language)
        l.add_xpath('title', "//meta[@property='og:title']/@content")
        l.add_value('url', response.url)
        l.add_xpath('category', "//div[@class='brcbs col16 -pts -pbm']/a[2]/@href")
        l.add_xpath('subCategory', "//div[@class='brcbs col16 -pts -pbm']/a[3]/@href")
        l.add_xpath('SKU', "//span[contains(text(), 'SKU')]/following-sibling::text()" )
        l.add_xpath('brand', brand_xpath, add_brand)
        l.add_xpath("stars", "//div[@class='stars _s _al']/text()")
        l.add_xpath("ratings", "//a[@class='-plxs _more']/text()")
        l.add_xpath("refurbished", "//img[contains(@alt, 'REFU')]", clean_refurbished)
        l.add_xpath("currentPrice_value", "//span[@class='-b -ltr -tal -fs24']/text()")
        l.add_xpath("originalPrice_value", "//span[contains(@class, '-fs16')][1]/text()")
        l.add_value('stock', clean_stock(stock_value))
        l.add_xpath('priceUSD',"//span[@class='-b -ltr -tal -fs24']/text()")
        l.add_xpath('originalPriceUSD', "//span[contains(@class, '-fs16')][1]/text()")
        l.add_xpath('device', "//span[contains(@class, '-fs16')][1]/text()")
        l.add_xpath('currency', "//span[contains(@class, '-fs16')][1]/text()")
        l.add_xpath("isDiscount", "//span[contains(@class, 'bdg _dsct _dyn -mls')]/text()", add_discount)
        l.add_xpath("discountRate", "//span[contains(@class, 'bdg _dsct _dyn -mls')]/text()", clean_discountrate)
        l.add_xpath("isFlashsales", isflash_xpath, is_flashsales)
        l.add_xpath("Flashtime", flashtime_xpath, flash_remaintime)
        l.add_xpath("FlashRemainItems", "//span[contains(@class, '-fsh0 -prs -fs12')]", remain_items)
        l.add_xpath("seller", "//div[@class='-hr -pas']/p/text()", get_seller)
        l.add_xpath("sellerScore", "//bdo[@class='-m -prxs']/text()")
        l.add_xpath("sellerFollowers", "//p[@data-followers='true']/span/text()", get_sellerfollowers)
        l.add_xpath("sellerOrderFulfillmentRate", sellerorder_xpath, get_sellerOrderRate)
        l.add_xpath("sellerQualityScore", "//p[contains(text(), 'Score')]/span/text()", get_sellerscore)
        l.add_xpath("sellerCustomerRating", customerratings_xpath)
        l.add_xpath("picture", "//div[@id='imgs']//a/@href")
        l.add_xpath("breadcumbs","//div[@class='brcbs col16 -pts -pbm']/a/text()", get_breadlist)
        l.add_xpath('description', "//meta[@property='og:description']/@content")
        yield l.load_item()