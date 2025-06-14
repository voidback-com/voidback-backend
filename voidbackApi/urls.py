from django.urls import path, include

from .views import (
    # ACCOUNT
    send_otp,
    send_AnonymousOtp,
    verify_otp,
    resetPassword,
    AccountView,
    SignupView,
    LoginView,
    LogoutView,
    followAccount,
    unfollowAccount,
    isAccountFollowed,
    isFollowingBack,
    getAccountByUsername,
    getUsernameFollowing,
    getFollowingUsernameCount,
    getUsernameFollowsCount,
    getUsernameFollowers,
    searchAccounts,
    getAccountMutuals,
    getAccountRecommendations,
    getFriends,
    AccountListView,


    # WRITEUP
    WriteUpView,
    newSeries,
    TagsListView,
    WriteUpListView,
    getWriteUp,
    getImpressions,
    likeWriteUp,
    CommentView,
    CommentListView,
    commentsCount,
    likeComment,
    getCommentImpressions,
    AccountWriteUpListView,
    SeriesListView,
    LikedWriteUpListView,
    deleteSeries,


    # SEARCH
    SearchQueryView,



    # NOTIFICATIONS
    getNotifications,
    readNotification,
    deleteNotification,
    deleteAllNotification,



    # PLATFORM
    getPlatformMessage,

    # REPORT
    ReportView,


)


urlpatterns = [

    # AUTHENTICATION
    path("signup", SignupView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),


    # ACCOUNT
    # get account object of current access token
    path("account", AccountView.as_view()),
    path("account/sendOtp", send_otp),  # send an email otp
    path("account/verifyOtp", verify_otp),  # verify email otp
    path("account/reset", resetPassword),  # reset password
    path("account/recommendations", getAccountRecommendations),
    path("account/anonymous_sendOtp", send_AnonymousOtp),

    path("account/list", AccountListView.as_view()),  # list all accounts

    # search for an account (used by autocomplete)
    path("account/search", searchAccounts),
    # get all the accounts this username follows,
    path("account/following/<str:username>", getUsernameFollowing),
    # get count of all the accounts that follow this username
    path("account/followingUsername/count/<str:username>",
         getFollowingUsernameCount),
    # get count of all the accounts that follow this username
    path("account/usernameFollows/count/<str:username>", getUsernameFollowsCount),

    # get all the accounts that follow this username
    path("account/followers/<str:username>", getUsernameFollowers),

    path("account/isFollowed", isAccountFollowed),  # is account followed
    path("account/follow", followAccount),  # follow an account
    path("account/unfollow", unfollowAccount),  # unfollow an account
    path("account/isFollowingBack", isFollowingBack),  # is account following me
    path("account/getAccount/<str:username>", getAccountByUsername),
    path("account/getMutuals/<str:username>", getAccountMutuals),
    path("account/friends/<str:username>", getFriends),
    path("account/writeups", AccountWriteUpListView.as_view()),
    path("account/series", SeriesListView.as_view()),



    # WRITEUPs
    path("writeup", WriteUpView.as_view()),  # create, delete or view writeup
    path("writeup/list", WriteUpListView.as_view()),
    path("getWriteUp", getWriteUp),
    path("writeup/impressions", getImpressions),
    path("writeup/like", likeWriteUp),
    path("writeup/comment", CommentView.as_view()),
    path("writeup/comments", CommentListView.as_view()),
    path("writeup/comments/count", commentsCount),
    path("writeup/comment/like", likeComment),
    path("writeup/comment/impressions", getCommentImpressions),
    path("writeup/list/liked", LikedWriteUpListView.as_view()),
    path("writeup/series/delete", deleteSeries),


    # WriteUp Tags & newSeries
    path("newSeries", newSeries),
    path('tags', TagsListView.as_view()),



    # SEARCH QUERY
    path("searchQuery", SearchQueryView.as_view()),  # search query



    # NOTIFICATIONS
    path("notifications", getNotifications),
    path("notifications/read", readNotification),
    path("notifications/delete/<int:pk>", deleteNotification),
    path("notifications/delete/all", deleteAllNotification),


    # PLATFORM
    path("platform/message", getPlatformMessage),

    # REPORT
    path("report", ReportView.as_view()),



]
