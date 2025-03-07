from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    # ACCOUNT
    send_otp,
    send_AnonymousOtp,
    verify_otp,
    resetPassword,
    AccountView,
    SignupView,
    followAccount,
    unfollowAccount,
    isAccountFollowed,
    isFollowingBack,
    getAccountByUsername,
    getAccountLikedPosts,
    getUsernameFollowing,
    getUsernameFollowingCount,
    getUsernameFollowers,
    searchAccounts,
    getAccountMutuals,
    getAccountRecommendations,
    getAccountStatus,
    getFriends,


    # POST
    PostView,
    getPostById,
    getPostImpressions,
    AccountPostImpressionView,

    SymbolView,
    HashtagView,

    getHashtagPostsCount,
    getSymbolPostsCount,
    
    getTrendingHashtags, 
    searchHashtags,

    getPostRepliesCount,
    PostRepliesView,

    getTrendingSymbols,
    searchSymbols,

    searchPosts,

    forYou,

    AuthorPostsView,




    # SEARCH
    SearchQueryView,
    


    # EXPLORE
    exploreSearch,
    exploreSearchCount,

    # SYMBOL
    getSymbolPosts,


    # HASHTAG
    getHashtagPosts,


    # NOTIFICATIONS
    getNotifications,
    readNotification,
    deleteNotification,
    deleteAllNotification,



    # PLATFORM
    getPlatformMessage,

    # REPORT
    ReportView,


    # DMs
    CreateDMSession,
    DeleteDMSession,
    SendDirectMessage,
    DeleteDirectMessage,
    getSessions,
    DirectMessageSessionView,
    archiveSession,
    unarchiveSession,
    getArchivedSessions,


    # Edge Room
    CreateEdgeRoomView,
    ListMyEdgeRoomsAdminView,
    ListMyEdgeRoomsView,
    ListRoomPostsView,
    getMembership,
    joinEdgeRoom,
    getTopRankingRooms
)





urlpatterns = [

    # AUTHENTICATION
    path("signup", SignupView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path('token/blacklist', TokenBlacklistView.as_view()),


    # ACCOUNT
    path("account", AccountView.as_view()), # get account object of current access token
    path("account/sendOtp", send_otp), # send an email otp
    path("account/verifyOtp", verify_otp), # verify email otp
    path("account/reset", resetPassword), # reset password
    path("account/recommendations", getAccountRecommendations),
    path("account/anonymous_sendOtp", send_AnonymousOtp),


    path("account/search", searchAccounts), # search for an account (used by autocomplete)
    path("account/following/<str:username>", getUsernameFollowing), # get all the accounts this username follows,
    path("account/following/count/<str:username>", getUsernameFollowingCount), # get count of all the accounts that follow this username

    path("account/followers/<str:username>", getUsernameFollowers), # get all the accounts that follow this username

    path("account/isFollowed", isAccountFollowed), # is account followed
    path("account/follow", followAccount), # follow an account
    path("account/unfollow", unfollowAccount), # unfollow an account
    path("account/isFollowingBack", isFollowingBack), # is account following me
    path("account/getAccount/<str:username>", getAccountByUsername),
    path("account/getMutuals/<str:username>", getAccountMutuals),
    path("account/status", getAccountStatus),
    path("account/friends/<str:username>", getFriends),



    # POST
    path("post", PostView.as_view()), # create, delete or view post
    path("post/get/<int:post_id>", getPostById), # get post by id
    path("post/impressions/<int:post_id>", getPostImpressions), # get specific post impressions
    path("post/account/impression/<int:post_id>", AccountPostImpressionView.as_view()), # get specific liked post
    path("post/account/liked", getAccountLikedPosts), # get all liked posts by specific account
    path("post/search", searchPosts), # search for a post
    path("post/author", AuthorPostsView.as_view()), # get all the posts of a specific author


    path("post/repliesCount/<int:parent_post_id>", getPostRepliesCount), # get replies count to parent_post
    path("post/replies", PostRepliesView.as_view()), # get replies to parent_post


    # FEED
    path("foryou", forYou), # get for you posts


    # RIGHT SECTION
    path("symbols", SymbolView.as_view()), # get all symbols
    path("symbols/trending", getTrendingSymbols), # get trending symbols
    path("symbols/search", searchSymbols), # search for a symbol (used by autocomplete)

    path("hashtags", HashtagView.as_view()), # get all hashtags
    path("hashtags/trending", getTrendingHashtags), # get trending hashtags
    path("hashtags/search", searchHashtags), # search for a hashtag (used by autocomplete)
    path("hashtags/postCount/<int:hashtag>", getHashtagPostsCount),
    path("symbols/postCount/<int:symbol>", getSymbolPostsCount),


    # SEARCH QUERY
    path("searchQuery", SearchQueryView.as_view()), # search query



    # EXPLORE
    path("exploreSearch", exploreSearch),
    path("exploreSearchCount", exploreSearchCount),



    # SYMBOL
    path("symbol/<str:symbol>", getSymbolPosts),
    path("hashtag/<str:hashtag>", getHashtagPosts),


    # NOTIFICATIONS
    path("notifications", getNotifications),
    path("notifications/read", readNotification),
    path("notifications/delete/<int:pk>", deleteNotification),
    path("notifications/delete/all", deleteAllNotification),


    # PLATFORM
    path("platform/message", getPlatformMessage),

    # REPORT
    path("report", ReportView.as_view()),



    # DMs
    path("dm/create/session", CreateDMSession.as_view()),
    path("dm/delete/session", DeleteDMSession.as_view()),
    path("dm/send/message", SendDirectMessage.as_view()),
    path("dm/delete/message", DeleteDirectMessage.as_view()),
    path("dm/get/sessions", getSessions),
    path("dm/view/session", DirectMessageSessionView.as_view()),
    path("dm/archive/session", archiveSession),
    path("dm/unarchive/session", unarchiveSession),
    path("dm/get/archives", getArchivedSessions),



    # Edge Room
    path("edgeRoom/create", CreateEdgeRoomView.as_view()),
    path("edgeRoom/list", ListMyEdgeRoomsView.as_view()),
    path("edgeRoom/list/admin", ListMyEdgeRoomsAdminView.as_view()),
    path("edgeRoom/list/posts", ListRoomPostsView.as_view()),
    path("edgeRoom/membership", getMembership),
    path("edgeRoom/join", joinEdgeRoom),
    path("edgeRoom/topRanking", getTopRankingRooms)


]


