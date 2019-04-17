from django.db import models
from datetime import datetime


# Create your models here.

class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField("date published", default = datetime.now())

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
	#source_id = models.IntegerField("Source ID")	

	def __str_(self):
		return self.profile


class Articles(models.Model):
	article_id = models.BigIntegerField(null = True)
	title = models.CharField(max_length=255)
	source_id = models.ForeignKey(Sources, null = True, blank = True, verbose_name = "Source", on_delete = models.SET_NULL)
	source_type_id = models.ForeignKey(Source_Types, null = True, blank = True, verbose_name = "Source Type", on_delete = models.SET_NULL)
	profile_id = models.ForeignKey(Profiles,null = True, verbose_name = "Profile", on_delete=models.SET_NULL, blank = True)
	#source_id = models.IntegerField()
	#source_type_id = models.IntegerField()
	#profile_id = models.BigIntegerField()
	source_url = models.TextField(blank = True, default = "")
	article_raw = models.TextField(blank = True, default = "")
	author = models.CharField(max_length=200, blank = True, default = "")

	def __str__(self):
		return self.title

class Comments(models.Model):
	comment_id = models.AutoField(primary_key=True, blank = True,)
	article_id = models.ForeignKey(Articles,  blank = True, verbose_name = "Article", null = True, on_delete = models.SET_NULL)
	profile_id = models.ForeignKey(Profiles,  blank = True, verbose_name = "Profile",null = True,  on_delete = models.SET_NULL)
	#profile_id = models.BigIntegerField()
	#source_id = models.IntegerField()
	comment_raw = models.TextField( blank = True,null = True)
	parent_comment_id = models.BigIntegerField( blank = True,null = True)

	def __str__(self):
		return self.comment_raw



class Query_Runs(models.Model):
	query_run_id = models.IntegerField(blank = True, null = True)
	#user_id = models.IntegerField(default=1)
	query_id = models.ForeignKey(Queries, default = 1, verbose_name="Query", on_delete = models.SET_DEFAULT)
	query_text = models.TextField()
	query_runtime = models.DateTimeField("Query Runtime", default = datetime.now())

	def __str__(self):
		return str(self.query_id) + " @ " + str(self.query_runtime) + "   ...QUERY:...   " + self.query_text

class Rank(models.Model):
	result_id = models.AutoField(primary_key=True, verbose_name="Rank Id")
	query_run_id = models.ForeignKey(Query_Runs, default = 1, verbose_name ="Query Run Id", on_delete = models.SET_DEFAULT)
	article_id = models.ForeignKey(Articles, default = 1, verbose_name = "Article Id", on_delete = models.SET_DEFAULT)
	#result_id = models.IntegerField("Rank Result ID")
	#query_run_id = models.IntegerField("Query Run")
	#article_id = models.IntegerField("Article/Tweet")
	rank_score = models.FloatField("Weighted Score")
	core_score = models.FloatField("Core Score(BM25 Native)")
	ranking = models.FloatField("Ranking")
	source = models.IntegerField("Source", default = 1)
	date = models.DateTimeField("Date")
	url = models.CharField("URL",max_length=255)
	tweet_id = models.BigIntegerField("Tweet Id", default = 1)
	article_text = models.TextField("Original Title/Tweet")
	comments_raw = models.TextField("Comments/Replies")

	def __str__(self):
		return (str(self.result_id))

class Hashtags(models.Model):
	hashtag_id = models.AutoField(primary_key=True, verbose_name="Hashtag ID")
	#hashtag_id = models.IntegerField("Hashtag Id")
	hashtag_string = models.CharField(max_length=255)

	def __str__(self):
		return self.hashtag_string

class Twitter_Imports(models.Model):
	import_id = models.IntegerField()
	hashtag_id = models.ForeignKey(Hashtags, null=True, on_delete=models.SET_NULL)
	run_time = models.DateTimeField("Run Time", default = datetime.now())
	history_time = models.IntegerField("Lookback period", default=24)

class Tweets(models.Model):
	tweet_id = models.BigAutoField(primary_key = True, verbose_name = "Tweet ID (System)")
	created_at = models.DateTimeField()
	id_str = models.CharField(max_length=255)
	tweet_text = models.CharField(max_length=255)
	in_reply_to_status_id_str = models.CharField(max_length=255)
	in_reply_to_user_id_str = models.CharField(max_length=255)
	n_reply_to_screen_name = models.CharField(max_length=255)
	user_name = models.CharField(max_length=255)
	user_screen_name = models.CharField(max_length=255)
	entities_hashtags = models.CharField(max_length=255)
	entities_urls = models.CharField(max_length=255)
	entities_user_mentions = models.CharField(max_length=255)
	hashtag_id = models.ForeignKey(Hashtags, null = True, on_delete = models.SET_NULL)
	hashtag_text = models.IntegerField(null =True, blank = True)


	def __str__(self):
		return self.tweet_text


class Replies(models.Model):
	reply_id = models.BigAutoField(primary_key = True, verbose_name = "Reply ID (System)")
	created_at = models.DateTimeField()
	id_str = models.CharField(max_length=255)
	tweet_text = models.CharField(max_length=255)
	in_reply_to_status_id_str = models.CharField(max_length=255)
	in_reply_to_user_id_str = models.CharField(max_length=255)
	n_reply_to_screen_name = models.CharField(max_length=255)
	user_name = models.CharField(max_length=255)
	user_screen_name = models.CharField(max_length=255)
	entities_hashtags = models.CharField(max_length=255)
	entities_urls = models.CharField(max_length=255)
	entities_user_mentions = models.CharField(max_length=255)

	def __str__(self):
		return self.tweet_text

