
## Api Endpoints

```python


# AUTHENTICATION
path("signup", SignupView.as_view()), # handles user signup
path("login", LoginView.as_view()), # handles login and returns a token upon successful authentication!
path("logout", LogoutView.as_view()), # deletes the auth-token


# ACCOUNT
path("account", AccountView.as_view()), # returns account object
path("account/sendOtp", send_otp), # send an email otp 
path("account/verifyOtp", verify_otp), # verify email otp 
path("account/reset", resetPassword), # reset password 
path("account/recommendations", getAccountRecommendations), # returns account objects
path("account/anonymous_sendOtp", send_AnonymousOtp), # unauthenticated otp request


path("account/search", searchAccounts), # search for an account (used by autocomplete)
path("account/following/<str:username>", getUsernameFollowing), # get all the accounts this username follows,
path("account/following/count/<str:username>", getUsernameFollowingCount), # get count of all the accounts that follow this username

path("account/followers/<str:username>", getUsernameFollowers), # get all the accounts that follow this username

path("account/isFollowed", isAccountFollowed), # is account followed
path("account/follow", followAccount), # follow an account
path("account/unfollow", unfollowAccount), # unfollow an account
path("account/isFollowingBack", isFollowingBack), # is account following me
path("account/getAccount/<str:username>", getAccountByUsername), # returns account with the given username
path("account/getMutuals/<str:username>", getAccountMutuals), # get mutual friends with the given username
path("account/friends/<str:username>", getFriends), # returns friends of this username
path("account/writeups", AccountWriteUpListView.as_view()), # return writeups by authenticated user
path("account/series", SeriesListView.as_view()), # return series by authenticated user



# WRITEUPs
path("writeup", WriteUpView.as_view()), # create, delete or view writeup
path("writeup/list", WriteUpListView.as_view()), # view a bunch of writeups with pagination
path("getWriteUp", getWriteUp), # view a single writeup called when the user requests to (view/writeup/id)
path("writeup/impressions", getImpressions), # returns writeup impressions
path("writeup/like", likeWriteUp), # like a writeup
path("writeup/comment", CommentView.as_view()), # create/delete comment
path("writeup/comments", CommentListView.as_view()), # returns comments with pagination
path("writeup/comments/count", commentsCount), # returns comment count for writeup
path("writeup/comment/like", likeComment), # like a comment
path("writeup/comment/impressions", getCommentImpressions), # get impressions of a given comment (e.g., likes and replies)
path("writeup/list/liked", LikedWriteUpListView.as_view()), # returns writeups liked by a given username
path("writeup/series/delete", deleteSeries), # delete a series


# WriteUp Tags
path("getSeries", getMySeries),  # retrieve a series
path("newSeries", newSeries),  # create a series
path('tags', TagsListView.as_view()), # return tags with pagination



# SEARCH QUERY
path("searchQuery", SearchQueryView.as_view()), # create / retrieve searchquery



# NOTIFICATIONS
path("notifications", getNotifications), # get all notifications for authenticated user
path("notifications/read", readNotification), # update status of a notification to (isRead=true)
path("notifications/delete/<int:pk>", deleteNotification), # delete a single notification for authenticated user
path("notifications/delete/all", deleteAllNotification), # clear all notifications for authenticated user


# PLATFORM
path("platform/message", getPlatformMessage), # returns unseen platform messages if any

# REPORT
path("report", ReportView.as_view()), # create a report object



# SEO RELATED
path("sitemap/writeups", getSiteMapWriteUps), # returns an array of writeups between 1 and 50k since google's limit is 50k objects in array

```
