# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from scrapy.http import Request
from urllib import parse

from ArticleSpider.items import CnBlogsArticleItem

from ArticleSpider.utils.common import get_md5


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com']

    def parse(self, response):
        """
        1，获取文章列表页中的文章url 并交给scrapy下载后并进行解析
        2，获取下一页的url 并交给scrapy进行下载 下载完成后交给parse函数

        # 解析列表页中的所有文章url 并交给scrapy下载后并进行解析

        :param response:
        :return:
        """

        post_urls = response.css(".news_entry a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse_detail)

        # post_nodes = response.css(".news_entry a:")
        # for post_node in post_nodes:
        #     image_url = post_node.css("img::arrt(src)").extract_first("")
        #     post_url = post_node.css("::arrt(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url,post_url), meta={"front_image_url":image_url},callback=self.parse_detail)

        # next_url = response.css(".pager :last-child::attr(href)").extract_first()
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url,),callback=self.parse)


        # 提取下一页并交给scrapy进行下载
        # next_urls = response.css(".pager a").extract_first("")

        # title = response.xpath('//*[@id="news_title"]/a/text()').extract()[0]
        # create_date = response.xpath('//*[@id="news_info"]/span[2]/text()').extract()[0]
        # create_time = response.xpath('//*[@id="news_info"]/span[2]/text()').extract()[0]
        # match_pattern = ".*(\d{4}-\d{2}-\d{2}).*?(\d+:\d+)"
        # match_re = re.match(match_pattern,create_date)
        # if match_re:
        #     create_date = match_re.group(1)
        #     create_time = match_re.group(2)
        # writer = response.xpath('//*[@id="news_info"]/span[1]/a/text()').extract()[0]
        #
        # content = response.xpath('//*[@id="news_body"]').extract()[0]

    def parse_detail(self,response):
        article_item = CnBlogsArticleItem()

        title = response.css("#news_title a::text").extract_first()

        create_date = response.css(".time::text").extract_first()
        # create_time = response.css(".time::text").extract_first()

        match_pattern = ".*(\d{4}-\d{2}-\d{2}).*?(\d+:\d+)"
        match_re = re.match(match_pattern, create_date)
        if match_re:
            create_date = match_re.group(1)
            # create_time = match_re.group(2)

        content = response.css('#news_body').extract_first()

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strftime(create_date,"%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        article_item["create_date"] = create_date
        # article_item["create_time"] = create_time
        article_item["content"] = content

        yield article_item




