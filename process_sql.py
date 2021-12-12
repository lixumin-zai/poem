# python3.7
# -*- coding: utf-8 -*-
# @Author : listen
# @Time   :
import pymysql


class Poem:
    def __init__(self, id, image_url, poem_title, poem_text):
        self.id = id
        self.image_url = image_url
        self.poem_title = poem_title
        self.poem_text = poem_text
        self.cursor = self.connection()

    def connection(self):
        self.conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='lixumin1030',
                               db='poem',
                               charset='utf8')
        cursor = self.conn.cursor()
        return cursor

    def insert(self):
        a = self.cursor.execute(
            f"INSERT INTO `poem`.`new_table` (`id`, `image_url`, `poem_name`, `poem`) VALUES ({self.id}, '{self.image_url}', '{self.poem_title}', '{self.poem_text}');")
        print(a)

    def select(self, poem_title):
        self.cursor.execute(f"SELECT * FROM `new_table` WHERE `poem_name`='{poem_title}'")
        result = self.cursor.fetchmany(10)
        return result

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


