
import re
from ast import literal_eval
import sqlite3


# read in comments for analysis
class CorpusParser:

	def __init__(self, filename):
		self.filename = filename
		self.regex = re.compile('^#\s*\d+')
		self.corpus = dict()
		self.db_corpus = dict()
		self.db_name = 'pldb.db'

	def parse(self):
		#with open(self.filename) as f:
		#	s = ''.join(f.readlines())
		# blobs = s.split('#')[1:]
		#blobs = s.split('##')[1:]
		#print("==TEXT: comments content==")
		#for x in blobs:
			#text = x.split()
			# todo: add stop word removal
			# todo: perform stemming
			# todo: add in min / max word sizes

			# print('text: {0}'.format(text))
			#docid = text.pop(0)

			#print(docid)

			#print(text)
			#self.corpus[docid] = text
			# print(self.corpus)
		print("==DB:  comments content==")
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()
		c.execute("select comment_id,comment_raw from comments")
		data = c.fetchall()
		db_work = {}
		for row in data:
			docid = str(row[0])
			comments = row[1].split()
			#print(docid," ",comments)
			#db_work[docid] = comments
			self.corpus[docid] = comments
		print(self.corpus)


	def get_corpus(self):
		return self.corpus

# read in the current terms we want to search for in the comments

class QueryParser:

	def __init__(self, db_name):
		#self.filename = filename
		self.queries = []
		# db_name = 'pldb.db'
		#self.db_name = 'pldb.db'
		self.db_name = '../db.sqlite3'

	def parse(self):
		#print("==text==")
		#with open(self.filename) as f:
		#	lines = ''.join(f.readlines())
		#	for x in lines.split('\n')[:]:
		#		print('query: ', x)
		#self.queries = [x.rstrip().split() for x in lines.split('\n')[:]]
		#for row in self.queries:
		#	print(row)
		#print(self.queries)
		print('==DB==')
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()
		c.execute("select query from main_queries")
		data = c.fetchall()
		for row in data:
			query = row[0].split()
			self.queries.append(query)
		print(self.queries)


	def get_queries(self):
		return self.queries

class oldKeywordParser:

	def __init__(self, filename):
		self.filename = filename
		self.keywords = []

	def parse(self):
		with open(self.filename) as f:
			lines = ''.join(f.readlines())
		kw = literal_eval(lines)
		# print("==keywords weights ===")

		for key, value in kw.items():
			value = round(value / 100, 3)
		# print(key, value)
		# print('')
		self.keywords = kw

	def get_keywords(self):
		return self.keywords


class KeywordParser:

	def __init__(self, db_name):
		# db_name = 'pldb.db'
		self.db_name = db_name
		self.keywords = []

	def parse(self):
		kw = {}
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()
		c.execute("select keyword, default_weight from main_keyword_master order by default_weight desc")
		data = c.fetchall()

		for row in data:
			# print('keyword:', row[0], 'weight: ', row[1])
			kw.update({row[0]: row[1]})

		for key, value in kw.items():
			value = round(value / 100, 3)
			# print(key, value)
		self.keywords = kw

	def get_keywords(self):
		return self.keywords


class KeywordTypeParser:
	def __init__(self, db_name):
		# db_name = 'pldb.db'
		self.db_name = db_name
		self.keywords = []

	def parse(self):
		kwt = {}
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()
		c.execute("select keyword, category from main_keyword_master km left join main_keyword_categories kc on km.keyword_category_id_id = kc.keyword_category_id ")
		data = c.fetchall()

		for row in data:
			# print('keyword:', row[0], 'category: ', row[1])
			kwt.update({row[0]: row[1]})

		self.keywords_types = kwt

	def get_keywords(self):
		return self.keywords_types

	# pull in keywords and their assigned type


class KeywordTypeParser_old:

	def __init__(self, filename):
		self.filename = filename
		self.keywords = []

	def parse(self):
		with open(self.filename) as f:
			lines = ''.join(f.readlines())
		kwt = literal_eval(lines)
		#print("==keywords types ===")

		#for key, value in kwt.items():
		#	print(key, value)
		#print('')
		self.keywords_types = kwt

	def get_keywords(self):
		return self.keywords_types

# pull in source articles that are the parent to the comments
class ArticleParser:

	def __init__(self, filename):
		self.filename = filename
		self.regex = re.compile('^#\s*\d+')
		self.articles = {}

	def parse(self):
		with open(self.filename) as f:
			s = ''.join(f.readlines())
			blobs = s.split('##')[1:]
			work_dict = {}
			for x in blobs:
				text = x.split(',')
				text = [x.strip(' ') for x in text]
				# print('text: {0}'.format(text))
				docid = int(text.pop(0))
				title = text.pop(0)
				source = text.pop(0)
				pub_date = text.pop(0)
				pub_url = text.pop(0)
				# work_dict = {}
				work_dict[docid] = {"title": title, "source": source, "pub_date": pub_date, "pub_url": pub_url}
				self.articles = work_dict

	def get_articles(self):
		return self.articles


if __name__ == '__main__':
	qp = QueryParser('text/queries.txt')
	#print(qp.get_queries())
