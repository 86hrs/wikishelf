from django.contrib import admin

# Register your models here.
from .models import User, Collection, Article, Tag, UserNote, SearchHistory, CollectionShare

admin.site.register(User)
admin.site.register(Collection)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(UserNote)
admin.site.register(SearchHistory)
admin.site.register(CollectionShare)
