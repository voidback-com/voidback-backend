from django.contrib import admin
from .models import (
    Account,
    Post,
    PostImage,
    PostImpression,
    Symbol,
    Hashtag,
    ForYou,
    Follow,
    SearchQuery,
    Report,
    Notification,
    PlatformMessage,
    PlatformMessageImpression,
    DMMessage,
    DirectMessageSession,
    DMImage,
    AccountActiveStatus,
    EdgeRoom,
    EdgeRoomConfig,
    MemberPermissions,
    RoomMembership,
    RoomCategory
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




@admin.register(Post)
class PostAdmin(ModelAdmin):
    search_fields = ['id']
    sortable_by = ['id']



@admin.register(PostImage)
class PostImageAdmin(ModelAdmin):
    pass


@admin.register(PostImpression)
class PostImpressionAdmin(ModelAdmin):
    search_fields = ['post__id', "account__username"]



@admin.register(Symbol)
class SymbolAdmin(ModelAdmin):
    search_fields = ['symbol']


@admin.register(Hashtag)
class HashtagAdmin(ModelAdmin):
    search_fields = ['hashtag']


@admin.register(ForYou)
class ForYouAdmin(ModelAdmin):
    search_fields = ['account__username']


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



# DMS registered only for development
@admin.register(DirectMessageSession)
class DirectMessageSessionAdmin(ModelAdmin):
    pass


@admin.register(DMMessage)
class DMMessageAdmin(ModelAdmin):
    pass



@admin.register(DMImage)
class DMImageAdmin(ModelAdmin):
    pass



@admin.register(AccountActiveStatus)
class AccountActiveStatusAdmin(ModelAdmin):
    pass



@admin.register(EdgeRoom)
class EdgeRoomAdmin(ModelAdmin):
    pass



@admin.register(EdgeRoomConfig)
class EdgeRoomConfigAdmin(ModelAdmin):
    pass



@admin.register(MemberPermissions)
class MemberPermissionsAdmin(ModelAdmin):
    pass


@admin.register(RoomMembership)
class RoomMembershipAdmin(ModelAdmin):
    pass


@admin.register(RoomCategory)
class RoomCategoryAdmin(ModelAdmin):
    pass


