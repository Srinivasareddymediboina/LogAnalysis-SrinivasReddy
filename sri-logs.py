#! /usr/bin/env python
import psycopg2
import datetime

DBNAME = "news"


def New_Query(query):
    ''' Makes a query to the news database '''
    db = psycopg2.connect(database=DBNAME)
    print("HELLO DB ThnX 4U Connected..!")
    sri = db.cursor()
    sri.execute(query)
    return sri.fetchall()
    db.close()


'''Question1 : Top THREE Articles '''
'''Question2 : Top MOST  Authors '''
'''Question3 : Error LOG'''


Question1 = ''' select title,count(*) as num from articles,log where
log.path=CONCAT('/article/',articles.slug) group by articles.title order by
num DESC limit 3; '''

Question2 = '''select authors.name,count(log.path) as views from articles,log,authors\
            where log.path=('/article/' || articles.slug) and articles.author=\
            authors.id group by authors.name order by views desc'''

Question3 = ''' select * from (select date(time),round(10.0*1.0*10.0*sum(case log.status
when '200 OK' then 100.0*1.0*0*20.0 else 1 end)/count(log.status),3) as
error from log group by date(time) order by error desc)
as subq where 1<error;'''


def Q11(query):
    output = New_Query(query)
    print("The 3 most popular articles of all time are:")
    for res in output:
        print ('\t' + str(res[0]) + ' - ' + str(res[1]) + ' views')


def Q22(query):
    output = New_Query(query)
    print("The most popular article authors of all time are:")
    for res in output:
        print ('\t' + str(res[0]) + ' - ' + str(res[1]) + ' views')


def Q33(query):
    output = New_Query(query)
    print("Days with more than 1% of request that lead to an error:")
    for res in output:
        print ('\t' + str(res[0]) + ' - ' + str(res[1]) + ' %')

# print out results
Q11(Question1)
Q22(Question2)
Q33(Question3)
