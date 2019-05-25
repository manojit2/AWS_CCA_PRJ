from django.shortcuts import render
from django.http import HttpResponse
from .models import Tutorial, Queries, Query_Runs, Keyword_Master, Articles, Comments, Results, \
	Tweets, Twitter_Imports, Hashtags, test_hello
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def register(request):
	form = UserCreationForm
	return render(request, "main/register.html", context={"form": form})


def homepage(request):
	return render(request=request, template_name ="main/home.html", context={"query_runs": Query_Runs.objects.all})


def queries(request):
	return render(request=request, template_name ="main/queries.html", context={"queries": Queries.objects.all})


def keywords(request):
	return render(request=request, template_name ="main/keywords.html",	context={"keywords": Keyword_Master.objects.all})


def query_runs(request):
	return render(request=request, template_name="main/query_runs.html", context={"query_runs": Query_Runs.objects.all})


def hashtags(request):
	return render(request=request, template_name="main/hashtags.html", context={"hashtags": Hashtags.objects.all})


def twitter_imports(request):
	return render(request=request, template_name="main/twitterimports.html", context={"tweets": Tweets.objects.all})


def results(request):
	return render(request=request, template_name="main/results.html", context={"results": Results.objects.all().order_by( '-query_run_id_id', 'ranking' )})


def articles(request):


	return render(request=request, template_name="main/articles.html", context={"articles": Articles.objects.all})


def comments(request):
	return render(request=request, template_name="main/comments.html", context={"comments": Comments.objects.all})
