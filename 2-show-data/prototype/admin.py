from wpe.prototype.models import Users, Tweets
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Tweets
    extra = 3


class UserAdmin (admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['handle', 'name', 'description', 'link']}),
    ]

    inlines = [ChoiceInline]
    list_display = ('handle', 'name', 'description', 'link')
    list_filter = ['handle']
    search_fields = ['handle', 'name', 'description']

class TweetsInline(admin.TabularInline):
    model = Tweets
    extra = 3


class TweetsAdmin (admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'tweet', 'timestamp']}),
    ]

    inlines = [TweetsInline]
    list_display = ('user', 'tweet', 'timestamp')
    list_filter = ['user']
    search_fields = ['user', 'tweet']

admin.site.register(Users, UserAdmin)
admin.site.register(Tweets, TweetsAdmin)