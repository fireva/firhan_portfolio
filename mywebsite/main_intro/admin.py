from django.contrib import admin
from .models import PersonalInfo, Experience, SocialLink,Article, Comment

# Register the models
admin.site.register(PersonalInfo)
admin.site.register(Experience)
admin.site.register(SocialLink)



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'date_updated')
    search_fields = ('title',)
    list_filter = ('date_created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'content', 'date_created')
    list_filter = ('date_created',)