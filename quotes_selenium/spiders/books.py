# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import  Request
from selenium.common.exceptions import NoSuchElementException
from quotes_selenium.items import QuotesSeleniumItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/carlos/Escritorio/curso scrapy/chromedriver')
        self.driver.get('http://books.toscrape.com/')

        while True:
         try:
             button_next = self.driver.find_element_by_xpath('//a[text()="next"]')
             sleep(3)
             self.logger.info('Esperando 3 segundos...')
             button_next.click()

             sel = Selector(text=self.driver.page_source)
             books = sel.xpath('//h3/a/@href').extract()

             for book in books:
                 url = 'http://books.toscrape.com/catalogue/' + book
                 yield Request(url, callback=self.parse_book)

         except NoSuchElementException:
            self.logger.info('No hay mas elemntos para extraer')
            self.driver.quit()
            break

    def parse_book(self, response):
        items = QuotesSeleniumItem()
        url = response.request.url
        title = response.xpath('//article/h3/a/@title').extract_first()
        price = response.xpath('//div[@class="product_price"]/p/text()').extract_first()

        items['url'] = url
        items['title'] = title
        items['price'] = price

        yield items