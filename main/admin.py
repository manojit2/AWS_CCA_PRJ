from django.contrib import admin
from .models import Tutorial, Keyword_Master, Keyword_Categories, Queries, Articles, Comments, Profiles, Query_Runs, Rank,Sources, Source_Types
from .models import Hashtags,Tweets, Replies, Twitter_Imports


class TutorialAdmin(admin.ModelAdmin):
	

	fieldsets = [
		("Title/Date", {"fields":["tutorial_title", "tutorial_published"]}),
		("Content",{"fields":["tutorial_content"]})

	]
#class Keyword_MasterAdmin(admin.ModelAdmin):
#	fieldsets =[
#	("Keywords", {"fields":["keyword_id","keyword","default_weight","keyword_category_id"]})
#	]

# Register your models here.
admin.site.register(Tutorial, TutorialAdmin)
#admin.site.register(Keyword_Master, Keyword_MasterAdmin)
admin.site.register(Keyword_Master)
admin.site.register(Keyword_Categories)
admin.site.register(Queries)
admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(Profiles)
admin.site.register(Query_Runs)
admin.site.register(Rank)
admin.site.register(Hashtags)
admin.site.register(Tweets)
admin.site.register(Replies)
admin.site.register(Sources)
admin.site.register(Source_Types)
admin.site.register(Twitter_Imports)
