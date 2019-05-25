from django.db import models
from datetime import datetime


# Create your models here.

class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()

	def __str__(self):
		return self.tutorial_title

class Keyword_Categories(models.Model):
	keyword_category_id = models.AutoField(primary_key = True, blank = True, verbose_name="Keyword Category ID")
	category = models.CharField(max_length=100)


	def __str__(self):
		return self.category


class Keyword_Master(models.Model):
	keyword_id = models.AutoField(primary_key=True, blank = True, verbose_name="Keyword Id")
	#keyword_id = models.IntegerField()
	keyword = models.CharField(max_length=200)
	keyword_category_id = models.ForeignKey(Keyword_Categories, default = 1, on_delete = models.SET_DEFAULT)
	#keyword_category_id = models.IntegerField("Keyword Category", default = 1)
	default_weight = models.FloatField("Default Weight", default = 100)


	def __str__(self):
		return self.keyword



class Queries(models.Model):
	query_id = models.AutoField(primary_key=True, verbose_name="Query ID")
	query = models.TextField()
	override = models.IntegerField(default = 0)

	def __str__(self):
		return self.query

class Source_Types(models.Model):
	source_type_id = models.IntegerField()
	source_type = models.CharField(max_length=200)

	def __str__(self):
		return self.source_type

class Sources(models.Model):
	source_id = models.AutoField(primary_key=True, verbose_name="Source Id")
	description = models.CharField(max_length=200)
	top_uri = models.CharField(max_length=200)
	source_type = models.ForeignKey(Source_Types, default = 1, verbose_name="Source Types", on_delete=models.SET_DEFAULT)

	def __str__(self):
		return self.description


class Profiles(models.Model):
	profile_id = models.AutoField(primary_key=True, verbose_name="Profile Id")
	#profile_id = models.BigIntegerField()
	profile = models.CharField(max_length=200)
	source_id = models.ForeignKey(Sources, default = 1, verbose_name="Source", on_delete= models.SET_DEFAULT)

	def __str_(self):
		return self.profile


class Articles(models.Model):
	article_id = models.CharField(max_length=255, null = True, blank = True)
	title = models.CharField(max_length=255, null = True, blank = True)
	source_id = models.ForeignKey(Sources, null = True, blank = True, verbose_name = "Source", on_delete = models.SET_NULL)
	source_type_id = models.ForeignKey(Source_Types, null = True, blank = True, verbose_name = "Source Type", on_delete = models.SET_NULL)
	profile_id = models.ForeignKey(Profiles, null = True, verbose_name = "Profile", on_delete=models.SET_NULL, blank = True)
	source_url = models.TextField(blank=True, null = True,  default = "")
	article_raw = models.TextField(blank=True, null = True, default = "")
	author = models.CharField(max_length=200, blank=True, null = True, default = "")
	author_topics = models.TextField(blank=True, null=True)
	article_date = models.CharField(max_length=255, blank=True, null = True)

	def __str__(self):
		return self.title


class Comments(models.Model):
	comment_id = models.AutoField(primary_key=True, blank = True)
	#article_id = models.ForeignKey(Articles, blank=True, verbose_name="Article", null=True, on_delete=models.SET_NULL)
	article_id = models.CharField(max_length=255, blank = True, null = True)
	profile_id = models.ForeignKey(Profiles,  blank = True, verbose_name = "Profile",null = True,  on_delete = models.SET_NULL)
	comment_raw = models.TextField( blank = True,null = True)
	comment_clean = models.TextField(blank=True, null = True)
	parent_comment_id = models.BigIntegerField( blank = True,null = True)
	screen_name = models.CharField(max_length=255, blank = True, null = True)


	def __str__(self):
		return self.comment_raw



class Query_Runs(models.Model):
	query_run_id = models.IntegerField(blank = True, null = True)
	query_id = models.ForeignKey(Queries, default = 1, verbose_name="Query", blank=True, null=True, on_delete = models.SET_DEFAULT)
	query_text = models.TextField()
	query_runtime = models.DateTimeField("Query Runtime", default = datetime.now())
	query_short_name = models.CharField(max_length=255, null=True, blank=True)
	query_short_desc = models.CharField(max_length=255, null=True, blank=True)
	term_count = models.IntegerField(null=True, blank=True)
	doc_count = models.IntegerField(null=True, blank=True)
	max_score = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=8)
	avg_score = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=8)
	std_dev = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=8)
	std_mode = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=8)
	total_score = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=8)

	def __str__(self):
		return str(self.query_id) + " @ " + str(self.query_runtime) + "   ...QUERY:...   " + self.query_text

class Results(models.Model):
	result_id = models.AutoField(primary_key=True, verbose_name="Rank Id")
	query_run_id = models.ForeignKey(Query_Runs, default = 1, verbose_name ="Query Run Id", blank=True, null=True, on_delete = models.SET_DEFAULT)
	article_id = models.ForeignKey(Articles, default = 1, verbose_name = "Article Id", blank=True, null=True, on_delete = models.SET_DEFAULT)
	#result_id = models.IntegerField("Rank Result ID")
	#query_run_id = models.IntegerField("Query Run")
	#article_id = models.IntegerField("Article/Tweet")
	rank_score = models.FloatField("Weighted Score", blank=True, null=True)
	core_score = models.FloatField("Core Score(BM25 Native)", blank=True, null=True)
	ranking = models.FloatField("Ranking", blank=True, null=True)
	source = models.IntegerField("Source", default = 1, blank=True, null=True)
	date = models.DateTimeField("Date", blank=True, null=True)
	url = models.CharField("URL",max_length=255, blank=True, null=True)
	tweet_id = models.BigIntegerField("Tweet Id", default = 1, blank=True, null=True)
	article_text = models.TextField("Original Title/Tweet", blank=True, null=True)
	comments_raw = models.TextField("Comments/Replies", blank=True, null=True)
	comment_id = models.CharField(max_length=255, blank=True, null=True)
	author = models.CharField(max_length=255, blank=True, null=True)
	small_comments = models.TextField(blank=True, null=True)

	def __str__(self):
		return (str(self.result_id))

class Hashtags(models.Model):
	hashtag_id = models.AutoField(primary_key=True, verbose_name="Hashtag ID")
	hashtag_string = models.CharField(max_length=255)
	hashtag_lastvalue = models.CharField(max_length=255, null=True, blank=True)
	hashtag_active = models.IntegerField(default=1, null=True, blank=True)

	def __str__(self):
		return self.hashtag_string

class Twitter_Imports(models.Model):
	import_id = models.IntegerField()
	hashtag = models.CharField(max_length=255, blank = True, null=True)
	run_time = models.DateTimeField("Run Time", default = datetime.now())
	history_time = models.IntegerField("Lookback period", default=24)

class Tweets(models.Model):
	tweet_id = models.BigAutoField(primary_key = True, verbose_name = "Tweet ID (System)", blank=True)
	created_at = models.DateTimeField(blank=True, null=True)
	id_str = models.CharField(max_length=255, blank=True, null=True)
	tweet_text = models.CharField(max_length=255, blank=True, null=True)
	in_reply_to_status_id_str = models.CharField(max_length=255, blank=True, null=True)
	in_reply_to_user_id_str = models.CharField(max_length=255, blank=True, null=True)
	n_reply_to_screen_name = models.CharField(max_length=255, blank=True, null=True)
	user_name = models.CharField(max_length=255, blank=True, null=True)
	user_screen_name = models.CharField(max_length=255, blank=True, null=True)
	entities_hashtags = models.CharField(max_length=255, blank=True, null=True)
	entities_urls = models.CharField(max_length=255, blank=True, null=True)
	entities_user_mentions = models.CharField(max_length=255, blank=True, null=True)
	hashtag_id = models.ForeignKey(Hashtags, null = True, on_delete=models.SET_NULL, blank=True)
	hashtag_text = models.IntegerField(null =True, blank = True)
	topic = models.CharField(max_length=255, blank=True, null=True)


	def __str__(self):
		return self.tweet_text


class Replies(models.Model):
	reply_id = models.BigAutoField(primary_key = True, verbose_name = "Reply ID (System)")
	created_at = models.DateTimeField(blank=True, null=True)
	id_str = models.CharField(max_length=255, blank=True, null=True)
	tweet_text = models.CharField(max_length=255, blank=True, null=True)
	in_reply_to_status_id_str = models.CharField(max_length=255, blank=True, null=True)
	in_reply_to_user_id_str = models.CharField(max_length=255, blank=True, null=True)
	n_reply_to_screen_name = models.CharField(max_length=255, blank=True, null=True)
	user_name = models.CharField(max_length=255, blank=True, null=True)
	user_screen_name = models.CharField(max_length=255, blank=True, null=True)
	entities_hashtags = models.CharField(max_length=255, blank=True, null=True)
	entities_urls = models.CharField(max_length=255, blank=True, null=True)
	entities_user_mentions = models.CharField(max_length=255, blank=True, null=True)
	topic = models.CharField(max_length=255, blank=True, null=True)
	def __str__(self):
		return self.tweet_text


class Topics(models.Model):
	topic_id = models.IntegerField(verbose_name="Topic ID")
	topic_desc = models.CharField(max_length=255, blank=True, null=True)
	active = models.IntegerField(default=1, blank=True, null=True)
	last_tweet = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.topic_desc




class test_hello():
	def myhello(self):
		print('hello')

