from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import (
    Account,
    WriteUp,
    WriteUpImpression,
    WriteUpThumbnail,
    Series,
    Tag,
    ForYou,
    Follow,
    SearchQuery,
    Report,
    Notification,
    PlatformMessage,
    PlatformMessageImpression,
    Comment,
    CommentImpression
)
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin


admin.site.unregister(Group)



@admin.register(Account)
class UserAdmin(ModelAdmin):
    search_fields = ['username', 'full_name', 'id']


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass




@admin.register(WriteUp)
class WriteupAdmin(ModelAdmin):
    search_fields = ['title']
    sortable_by = ['id']



@admin.register(Token)
class TokenAdmin(ModelAdmin):
    search_fields = ["id", "key", "user__username"]
    sortable_by = ["id"]


@admin.register(Series)
class SeriesAdmin(ModelAdmin):
    search_fields = ['name']
    sortable_by = ['id']



@admin.register(WriteUpThumbnail)
class WriteUpThumbnailAdmin(ModelAdmin):
    pass


@admin.register(WriteUpImpression)
class WriteupImpressionAdmin(ModelAdmin):
    search_fields = ['writeup__title', "account__username"]




@admin.register(Tag)
class TagAdmin(ModelAdmin):
    search_fields = ['tag']


@admin.register(Follow)
class FollowAdmin(ModelAdmin):
    search_fields = ['follower__username', 'following__username']


@admin.register(SearchQuery)
class SearchQueryAdmin(ModelAdmin):
    search_fields = ['query']


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    search_fields = ['object_type', 'resolved_by__username']
    ordering = ['resolved', '-priority', '-disturbance']





@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    search_fields = ['account__username']



@admin.register(PlatformMessage)
class PlatformMessageAdmin(ModelAdmin):
    search_fields = ['title']


@admin.register(PlatformMessageImpression)
class PlatformMessageImpressionAdmin(ModelAdmin):
    search_fields = ['message__title', 'account__username']





@admin.register(CommentImpression)
class CommentImpressionAdmin(ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass



@admin.register(ForYou)
class ForYouAdmin(ModelAdmin):
    search_fields = ['tags', 'series', 'authors', 'account__username']



