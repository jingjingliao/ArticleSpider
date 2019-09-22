# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.exporters import JsonItemExporter

import MySQLdb


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义jason文件的导出
    def __init__(self):
        self.file = codecs.open("article.json","w",encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipleline(object):
    # 调用scrapy提供的jason exporter导出jason文件
    def __init__(self):
        self.file = open("articleexport.json","wb")
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("127.0.0.1","root","Cherryjingjing1!2@","cnblogs",charset = "utf8",use_unicode = True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql="""
            insert into article_spider(title,create_date,url,url_object_id,content)
            VALUES (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["content"]))
        self.conn.commit()
