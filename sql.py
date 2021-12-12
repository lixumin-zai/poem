# python3.7
# -*- coding: utf-8 -*-
# @Author : listen
# @Time   :
import pymysql
connection = pymysql.connect(host='localhost',
      port=3306,
      user='root',
      password='lixumin1030',
      db='poem',
      charset='utf8')


cursor = connection.cursor()
# 执行查询 SQL
a = cursor.execute('SELECT * FROM `new_table` where `poem_name`="绝句"')
b = cursor.fetchmany(10)
# c = cursor.execute('INSERT INTO `new_table` (`id`, `image_url`, `poem_name`, `poem`) VALUES ("1", "{sel中", "{self.中}", "{self.第三方}")')
connection.commit()
# 获取单条数据
# b = cursor.fetchone()
# 获取前N条数据
# a= cursor.fetchmany(1)
print(a,b)
#关闭数据库
cursor.close()
connection.close()