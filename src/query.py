
from invdx import build_data_structures
from rank import score_BM25
from collections import defaultdict
import os
import operator
import parse
import sqlite3


class QueryProcessor:
    def __init__(self, queries, corpus, keywords, keyword_types, run_date, run_results_file, articles):
        self.queries = queries
        self.index, self.dlt = build_data_structures(corpus)
        self.keywords = keywords
        self.keyword_types = keyword_types
        self.run_date = run_date
        self.run_results_file = run_results_file
        self.file_runtime = run_date.strftime("%Y%m%d%H%M%S")  # what to use as the link base
        self.articles = articles

    def write_query_file(self, query_run_count, query, results_dir):
        """write the query used for this run"""
        t_count = 0
        query_string_short = ''  # for display in the run_results_list.txt file
        query_string_full = ''  # for display in the query file .query
        query_result_file = results_dir + '/' + self.file_runtime + 'Q' + str(query_run_count) + '.query'
        for term_str in query:
            print(term_str)
            if t_count == 0:
                query_string_short = term_str
                query_string_full = term_str
            elif t_count >= 1 and t_count <= 3:
                query_string_short += ',' + term_str
            elif t_count == 4:
                query_string_short += '...(more)'
            query_string_full += ', ' + term_str
            t_count += 1
        with open(query_result_file, mode='w') as qf:

            qf.write(str(t_count) + 'term \n')
            qf.write(query_string_full)
            qf.close()
        return query_string_short

    def write_weights_file_header(self, results_dir, query_run_count):
        """write the weights used for this run"""
        weight_file = results_dir + '/' + self.file_runtime + 'Q' + str(query_run_count) + '.weights'
        with open(weight_file, mode='w') as wf:
            wf.write('term,weight\n')
            wf.close()

    def write_weights_file(self, results_dir, query_run_count, weight_string):
        """write the weights used for this run"""
        weight_file = results_dir + '/' + self.file_runtime + 'Q' + str(query_run_count) + '.weights'
        with open(weight_file, mode='a') as wf:
            wf.write(weight_string)
            wf.close()

    def write_details_file_header(self, results_dir, query_run_count):
        details_result_file = results_dir + '/' + self.file_runtime + 'Q' + str(
            query_run_count) + '.details'  # ranked values by doc
        with open(details_result_file, mode='w') as df:
            df.write('doc,freq,score,term,weight,category\n')
            df.close()

    def write_details_file(self, results_dir, query_run_count,detail_string):
        """write out the line by line docit, term, freq, category for each run"""
        details_result_file = results_dir + '/' + self.file_runtime + 'Q' + str(
            query_run_count) + '.details'  # ranked values by doc
        with open(details_result_file, mode='a') as df:
            df.write(detail_string+'\n')
            df.close()

    def write_ranked_documents_file(self, results_dir, query_run_count, result):
        """write out the results of the run, docid, rank, score, title, etc"""
        ranking_result_file = results_dir + '/' + self.file_runtime + 'Q' + str(query_run_count) + '.rank'  # ranked values by doc
        self.db_name = 'pldb.db'
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("select comment_id,comment_raw from comments")
        data = c.fetchall()
        b_work = {}
        for row in data:
            docid = str(row[0])
            comments = row[1].split()
            print(docid," ",comments)
            # db_work[docid] = comments
            # self.corpus[docid] = comments
        #print(self.corpus)

        with open(ranking_result_file, mode='w') as rf:
            rf.write('docid,ranking,score,title,source,date,URLLink\n')
            sorted_x = sorted(result.items(), key=operator.itemgetter(1))
            sorted_x.reverse()
            index = 0
            j = 0
            for i in sorted_x[:100]:
                # tmp = (qid, i[0], index, i[1])
                # print('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
                j += 1
                score = i[1]
                doc_id = i[0]
                title = self.articles[int(i[0])]['title'].rstrip()
                pub_url = self.articles[int(i[0])]['pub_url'].rstrip()
                pub_date = self.articles[int(i[0])]['pub_date'].rstrip()
                source = self.articles[int(i[0])]['source'].rstrip()
                #data.update({'docId': i[0], 'rank_score': j, 'Score': score, 'source': source, 'title': title,
                #			 'pub_date': pub_date})

                out_string = doc_id + ',' + str(j) + ',' + str(round(score, 4)) + ',"' + title + '","' + source \
                             + '","' + pub_date + '","' + pub_url + '"\n'
                # print(out_string)
                rf.write(out_string)
                print("Out String: ", out_string)
                index += 1
            rf.close()
        return ranking_result_file

    def update_results_file(self, results_directory, query_run_count, t_count, max_score, doc_count,query_string_short):
        """update the master list of runs used to load into D3"""
        display_runtime = self.run_date.strftime("%d %B %Y %H:%M:%S")  # what to display in the rankings master file
        with open("../results/run_results.txt", mode='a') as rf:  # todo: make 'a' this a for production
            rf.write(display_runtime+',Q' + str(query_run_count) + ',http://results2.html?'
                    +results_directory+'/'+self.file_runtime + 'Q' + str(query_run_count)+','+str(max_score)
                     +','+str(t_count) + ','+str(doc_count)+',' + query_string_short + '\n')
        return True

    def write_category_file(self, results_dir, query_run_count, doc_category_count):
        category_result_file = results_dir + '/' + self.file_runtime + 'Q' + str(
            query_run_count) + '.category'  # ranked values by type
        #print(category_result_file)
        with open(category_result_file, mode='a') as cf:
            cf.write('docId,primary,primary_count,threat_result,secondary\n')
            for doc_id, cat_count_dict in doc_category_count.items():
                # print('Doc #:', doc_id)
                # print(cat_count_dict)
                threat_found = False
                for key, count in sorted(cat_count_dict.items(), reverse=True, key=lambda tup: tup[1]):
                    if key.lower() == 'threat':
                        threat_found = True
                i = 0
                for key, count in sorted(cat_count_dict.items(), reverse=True, key=lambda tup: tup[1] ):
                    if i == 0:
                        cf.write('{0}, Primary: {1}, Count: {2} '.format(doc_id, key.capitalize(), count))
                        if threat_found:
                            cf.write(', Threat: 1')
                        else:
                            cf.write(', Threat: 0')
                    elif i >= 1:
                        cf.write(', Support: {0}, Count: {1}'.format(key.capitalize(), count))
                    # if i > 1:
                        # break
                    i += 1
                cf.write('\n')
            cf.close()
        return category_result_file

    def create_results_directory(self, query_run_count):
        # create a directory for each run to store results
        results_dir = '../results/' + self.file_runtime + 'Q' + str(query_run_count)  # create the directory for output
        os.mkdir(results_dir)
        return results_dir

    def create_query_short_string(self, query_run_count, query, results_dir):
        return self.write_query_file(query_run_count, query, results_dir)

    def run(self):
        query_run_count = 1
        results = []
        for query in self.queries:
            results_dir = self.create_results_directory(query_run_count)
            self.write_details_file_header(results_dir, query_run_count)
            self.write_weights_file_header(results_dir, query_run_count)
            short_query_string = self.create_query_short_string(query_run_count, query, results_dir)
            term_count = len(query)
            max_score = 0
            result = self.run_query(query, query_run_count, results_dir)
            doc_count = len(result)
            sorted_x = sorted(result.items(), key=operator.itemgetter(1))
            sorted_x.reverse()
            j = 0
            for i in sorted_x[:100]:
                j += 1
                max_score = i[1]
                break
                index += 1

            self.update_results_file(results_dir, query_run_count, term_count, max_score, doc_count, short_query_string)
            self.write_ranked_documents_file(results_dir,query_run_count,result)
            results.append(result)
            query_run_count += 1

        return results

    def run_query(self, query, query_run_count, results_directory):
        query_result = dict()
        doc_category_count = dict()  # key: doc_id, val: cat_counts_dict
        term_count = 0
        for term in query:
            # look for term weights, if we don't find one assign a 1
            term_count += 1
            if self.keywords.get(term):
                weight = self.keywords.get(term)/100
                if self.keyword_types.get(term):
                    keyword_type = self.keyword_types.get(term)
                    #  print("keyword Type: {}".format(keyword_type))
            else:
                weight = 1
                #  print('Term: {0} Weight:{1}'.format(term, weight))
            weight_string = term + ',' + str(weight*100) + '\n'
            self.write_weights_file(results_directory, query_run_count, weight_string)

            if term in self.index:
                doc_dict = self.index[term]  # retrieve index entry
                for doc_id, freq in doc_dict.items():  # for each document and its word frequency
                    # print('41', doc_id, term, freq)
                    if doc_id in doc_category_count:
                        cat_counts_for_doc = doc_category_count[doc_id]
                    else:
                        cat_counts_for_doc = defaultdict(int)
                        doc_category_count[doc_id] = cat_counts_for_doc

                    cat_counts_for_doc[keyword_type] += freq

                    # print("50:", doc_category_count)
                    # print('\t docID: {0} Freq: {1}'.format(doc_id, freq))
                    # print('doc ID: {0}'.format(doc_id))
                    # print('term freq in this.doc: {0}'.format(freq))
                    # calculate score
                    score = score_BM25(weight=weight, n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
                                       dl=self.dlt.get_length(doc_id), avdl=self.dlt.get_average_length())

                    if doc_id in query_result:  # this document has already been scored once
                        query_result[doc_id] += score
                    else:
                        query_result[doc_id] = score
                    # print('\t docID: {0} Term: {3}  Freq: {1} Score:  {2}'.format(doc_id, freq, score, term))
                    detail_string = str(doc_id) + ',' + str(freq) + ',' + str(score) + ',' + term + ',' \
                                    + str(weight) + ',' + keyword_type
                    self.write_details_file(results_directory, query_run_count, detail_string)

            # dump cat_count_dicts
        # print('=============================================')
        #for doc_id, cat_count_dict in doc_category_count.items():
            # print('Doc #:', doc_id)
            # print(cat_count_dict)

        #	threat_found = False
        #	for key, count in sorted(cat_count_dict.items(), reverse=True, key=lambda tup: tup[1]):
        #		if key.lower() == 'threat':
        #			threat_found = True
        #			print('===========THREAT FOUND=============')
            # i = 0
            # for key, count in sorted(cat_count_dict.items(), reverse=True, key=lambda tup: tup[1] ):
            # 	if i == 0:
            # 		print('doc: {0}, primary: {1} - {2}'.format(doc_id, key, count))
            # 	elif i == 1:
            # 		print('\t\t Support: {0} - {1}'.format(key, count))
            # 	if i > 1:
            # 		break
            # 	i += 1
            # print('\n')
        self.write_category_file(results_directory, query_run_count, doc_category_count)
        return query_result
