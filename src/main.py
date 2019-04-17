
# todo: figure out how to credit original program to the author
# todo: figure out all required modules and build a requirements.txt
#
from parse import *
from query import QueryProcessor

import operator
import datetime
import json
import csv
import sys

import sqlite3
import time
import datetime
import random

#default_db_name = 'pldb.db'  #project light db
default_db_name = '../db.sqlite3'  #new combined django and light DB


def main():
    # qp = QueryParser(filename='../text/queries.txt')
    # cp = CorpusParser(filename='../text/corpus.txt')
    # cp = CorpusParser(filename='../text/comments.txt')
    # kw = KeywordParser(filename='default_db_name)
    # ar = ArticleParser(filename='../text/articles.txt')
    # kwt = KeywordTypeParser(filename='../text/hatetype.txt')

    run_results_file = '../results/run_results.txt'  # this is the file used to write master activity
    #qp = QueryParser(filename='../text/queries.txt')
    qp = QueryParser(db_name=default_db_name)
    cp = CorpusParser(filename='../text/comments.txt')
    kw = KeywordParser(db_name=default_db_name)
    ar = ArticleParser(filename='../text/articles.txt')
    kwt = KeywordTypeParser(db_name=default_db_name)


    qp.parse()
    queries = qp.get_queries()

    cp.parse()
    corpus = cp.get_corpus()

    kw.parse()
    keywords = kw.get_keywords()
    #print('keywords retrieved successfull')
    #print('printing keywords')
    #for key, value in keywords.items():
        #print(key, value)

    kwt.parse()
    keyword_types = kwt.get_keywords()

    ar.parse()
    articles = ar.get_articles()
    run_date = datetime.datetime.now()


    proc = QueryProcessor(queries, corpus, keywords, keyword_types, run_date, run_results_file, articles)
    results = proc.run()
    qid = 0
    data = {}

    for result in results:
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        j = 0
        for i in sorted_x[:100]:
            tmp = (qid, i[0], index, i[1])
            # todo: add lookup to the original article and add to output
            # print('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
            j += 1
            score = i[1]
            docid = i[0]
            title = articles[int(i[0])]['title'].rstrip()
            pub_url = articles[int(i[0])]['pub_url'].rstrip()
            pub_date = articles[int(i[0])]['pub_date'].rstrip()
            source = articles[int(i[0])]['source'].rstrip()
            data.update({'docId': i[0], 'rank_score': j, 'Score': score, 'source': source, 'title': title,
            						'pub_date': pub_date})

            out_string = docid + ', ' + str(j) + ', '+str(round(score, 4))+', "' + title + '", "' + source + '", "'+pub_date + '", "' + pub_url
           # print(out_string)
           # with open('../results/rankings.csv', 'a') as f:
           #     f.write(out_string)
            index += 1
        qid += 1
       # print('\n**The application has finished: You may view the results and supporting files in '
       #      'the ../results directory for this run.\nEach query in the /text/query.txt file'
       #      'will generate one directory with the format YYYYMMDDHHMMSSQ# with # being the query #.\n'
       #       'Inside the director you will find the following files:\n\n'
       #       'xxxxx.category - This file contains a record for each document showing the most prevelant category, the number\n'
       #       '\t\tof occurances, if the document contained terms considered threatening and all additional categories and '
       #       'their counts\nxxxxx.details - This file contains all documents, each term found and count and the weight applied'
       #       'to the specific term found.  This is supporting for the analysis on how a document was ranked\n'
       #       'xxxxx.query - This file contains the terms used for this query\nxxxxx.rank - this contains a list of all'
       #       'documents that were ranked including their score, the source, title, date\nxxxxx.weights - this file'
       #       'contains all of the terms found and the weights in effect at the time of the run.')
    # todo: setup the ability to pass K and b in as paramters



if __name__ == '__main__':
    main()
