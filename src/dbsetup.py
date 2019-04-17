# dbsetup.py
# setups the database and tables for detector
__author__ = 'David Jamriska'

import sqlite3
import time
import datetime
import random

default_db_name = 'pldb.db'  #project light db
load_sample_data = True


def create_table():
    print('creating tables')
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(keyword Text, value REAL)')
    conn.commit()
    c.execute('CREATE TABLE IF NOT EXISTS query_overrides(query_id, keyword_id, keyword_weight)')
    conn.commit()
    c.execute('CREATE TABLE IF NOT EXISTS keywordMaster(keyword_id Integer, keyword TEXT, system Integer, '
              'owner Integer, keyword_category_id Integer, default_weight Integer, public Integer)')
    conn.commit()
    c.execute('CREATE TABLE IF NOT EXISTS keyword_categories(keyword_category_id Integer, category text, '
              'system integer, owner integer, public integer)')
    conn.commit()
    c.execute('CREATE TABLE IF NOT EXISTS queries(query_id integer, query Text, system integer, owner integer, '
              'public integer,override integer)')
    conn.commit()


def data_keyword_entry(keyword, default_weight, keyword_id, system, owner, public,keyword_category):
    c.execute("Insert into keywordMaster (keyword, keyword_id,default_weight,system,owner,public, "
              "keyword_category_id) VALUES (?,?,?,?,?,?,?)",
              (keyword.lower(), keyword_id,default_weight,system,owner,public,keyword_category))
    conn.commit()


def data_query_entry(query_id,query, owner, system, public,override):
    c.execute("Insert into queries(query_id, query, system, owner,public,override) VALUES (?,?,?,?,?,?)",
              (query_id, query.lower(), system, owner,public, override) )
# When you try to connect to a DB that does not exist it will automatically create the file for you

def clean_keyword_alldata():
    sqls = 'Delete from keywordMaster'
    c.execute(sqls)
    conn.commit()

def keywords_get_all():
    c.execute("select keyword, default_weight from keywordMaster order by default_weight desc")
    data = c.fetchall()
    for row in data:
        print('keyword:',row[0],'weight: ',row[1] )
    return data

def keywords_get_mine(owner_id):
    c.execute("select* from keywordMaster order by default_weight where owner ")
    data = c.fetchall()
    #for row in data:
    #    print('keyword_id: ',row[0],'keyword: ',row[1], 'weight : ',row[5] )


def load_data_for_test():
    create_table()
    clean_keyword_alldata()
    data_keyword_entry('Python', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('SQLite3', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1',
                       '1')
    data_keyword_entry('Java', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('MongoDB', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1',
                       '1')
    data_keyword_entry('Spark', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('Hadoop', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')

    data_keyword_entry('SQL', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('C#', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('Java', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('Windows', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1',
                       '1')
    data_keyword_entry('crash', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('docker', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')

    data_query_entry('11,', 'python hadoop spark', '14', '1', '1', '0')
    data_query_entry('12,', 'C# SQL Windows crash', '14', '1', '1', '0')

    data_keyword_entry('hate', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('race', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('trump', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('assault', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1',
                       '1')
    data_keyword_entry('kill', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')
    data_keyword_entry('murder', str(random.randrange(100, 1000)), str(random.randrange(0, 1000)), '13', '14', '1', '1')

conn = sqlite3.connect(default_db_name)
conn.row_factory = sqlite3.Row
c = conn.cursor()

load_data_for_test()
my_data = keywords_get_all()
print(my_data)
keywords = []
print(type(my_data))
for row in my_data:
    print(row)
    keywords.append({row[0]:row[1]})

my_list = [{'python':100},{'docker':120}]
my_dict = {'python':100, 'sql':120, 'mongodb':180}

term = 'C#'
value = 100
my_dict.update({'SQLite3':100})
my_dict.update({term:value})
for row in my_data:
    my_dict.update({row[0]:row[1]})

for item in my_list:
    print(item)
for key, value in my_dict.items():
    print(key,value)

for key, value in my_dict.items():
    value = round(value/100, 3)
    print(key, value)
