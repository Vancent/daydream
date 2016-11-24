# -*- encoding:utf-8 -*-
# -*- encoding:utf-8 -*-

import scrapy
from scrapy import Request
from ..util import get_date
import re

class DmozSpider(scrapy.spiders.Spider):
    name = "daydream"
    allowed_domains = ["https://play.google.com/", "play.google.com"]
    start_urls = [
        "https://play.google.com/store/apps/collection/promotion_300259a_daydream_getinthegame",
    ]

    preusl = "https://play.google.com"

    def parse(self, response):
        print "############################"
        for sel in response.xpath('//div[@class="details"]'):
            title = sel.xpath('a[@class="title"]/text()').extract()
            link = sel.xpath('a[@class="title"]/@href').extract()
            print "game title:", title
            print "game link:", link
            if len(link) > 0:
                next_url = self.preusl + link[0] + "&hl=en"
                print next_url
                yield Request(next_url, callback=self.parse_game)
        print "############################"

    def parse_game(self, response):
        print "*******************************************"
        dataitem = {}
        dataitem["Date"] = get_date()
        dataitem["game_link"] = response.url
        for sel in response.xpath('//div[@class="id-app-title"]'):
            title = sel.xpath('text()').extract()
            dataitem["title"] = title[0]
            print "title:", title[0]

        for sel in response.xpath('//div[@class="rating-box"]'):
            score = sel.xpath('div[@class="score-container"]/div[@class="score"]/text()').extract()
            reviews_num = sel.xpath('div[@class="score-container"]/div[@class="reviews-stats"]/span[@class="reviews-num"]/text()').extract()
            print "score:", score[0]
            print "reviews_num:", reviews_num[0]
            dataitem["score"] = score[0]
            dataitem["reviews_num"] = reviews_num[0]

            five_num = sel.xpath('div[@class="rating-histogram"]/div[@class="rating-bar-container five"]'
                                    '/span[@class="bar-number"]/text()').extract()
            four_num = sel.xpath('div[@class="rating-histogram"]/div[@class="rating-bar-container four"]'
                                    '/span[@class="bar-number"]/text()').extract()
            three_num = sel.xpath('div[@class="rating-histogram"]/div[@class="rating-bar-container three"]'
                                    '/span[@class="bar-number"]/text()').extract()
            two_num = sel.xpath('div[@class="rating-histogram"]/div[@class="rating-bar-container two"]'
                                    '/span[@class="bar-number"]/text()').extract()
            one_num = sel.xpath('div[@class="rating-histogram"]/div[@class="rating-bar-container one"]'
                                    '/span[@class="bar-number"]/text()').extract()
            print "five_num:", five_num[0]
            print "four_num:", four_num[0]
            print "three_num:", three_num[0]
            print "two_num:", two_num[0]
            print "one_num:", one_num[0]
            dataitem["five_num"] = five_num[0]
            dataitem["four_num"] = four_num[0]
            dataitem["three_num"] = three_num[0]
            dataitem["two_num"] = two_num[0]
            dataitem["one_num"] = one_num[0]

        #获得游戏价格信息
        for sel in response.xpath('//div[@class="details-actions"]/span/span[@class="apps medium play-button buy-button-container is_not_aquired_or_preordered"]'
                                  '/button[@class="price buy id-track-click id-track-impression"]'):
            priceinfo = sel.xpath('span/text()').extract()
            price = priceinfo[2]
            idx = price.find("Buy")
            if idx != -1:
                price = price[0:idx]
            else:
                price = "Free"
            dataitem["price"] = price

        ###获取游戏的评论，评论有很多个，注意格式
        dataitem["player_review"] = []
        for sel in response.xpath('//div[@class="single-review"]'):
            view_header = sel.xpath('div[@class="review-body with-review-wrapper"]/span[@class="review-title"]/text()').extract()
            view = sel.xpath('div[@class="review-body with-review-wrapper"]/text()').extract()
            view_item ={}
            if len(view_header) > 0:
                print "header:", view_header[0]
                view_item["header"] = view_header[0]
            else:
                print "header:", ""
                view_item["header"] = ""

            print "     view:", view[1]
            view_item["content"] = view[1]
            #获得view_star
            view_stars = sel.xpath('div[@class="review-header"]/div[@class="review-info"]/div[@class="review-info-star-rating"]'
                                   '/div[@class="tiny-star star-rating-non-editable-container"]/@aria-label').extract()
            view_stars = re.sub("\D", "", view_stars[0])
            view_item["view_star"] = int(view_stars)
            dataitem["player_review"].append(view_item)

        for sel in response.xpath('//div[@class="details-section metadata"]'):
            nex_sel = sel.xpath('div[@class="details-section-contents"]')
            for met_sel in nex_sel.xpath('//div[@class="meta-info"]'):
                title = met_sel.xpath('div[@class="title"]/text()').extract()
                if title[0] == "Updated":
                    datePublished = met_sel.xpath('div[@class="content"]/text()').extract()
                    print "datePublished:", datePublished[0]
                    dataitem["datePublished"] = datePublished[0]

                elif title[0] == "Installs":
                    installs = met_sel.xpath('div[@class="content"]/text()').extract()
                    installs = installs[0]
                    print "installs:", installs
                    min_installs = re.sub(r'-.*$', "", installs)
                    min_installs = re.sub(r'\D', "", min_installs)
                    min_installs = int(min_installs)
                    dataitem["installs"] = installs
                    dataitem["min_installs"] = min_installs

        print "*******************************************"
        return dataitem

