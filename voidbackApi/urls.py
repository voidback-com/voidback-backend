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


    # POST
    PostView,
    getPostById,
    getPostImpressions,
    AccountPostImpressionView,
    PostMetadataView,

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




    # INBOX
    CreateInboxMessage,
    InboxMessagesView,
    deleteInboxMessage,


    # RESEARCH
    MyResearchPaperView,
    makePaperImpression,
    getAllPaperImpressions,
    getMyPaperImpression,
    TopResearchPapersView,
    searchPapers,
    getAccountResearch,
    getResearchPaper,


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


    # DATA-HUB
    DataHubQueryView,
    DataHubFeedbackPollView,
    DataHubPollView,

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
    path("account/recommendations", getAccountRecommendations),



    # POST
    path("post", PostView.as_view()), # create, delete or view post
    path("post/get/<int:post_id>", getPostById), # get post by id
    path("post/impressions/<int:post_id>", getPostImpressions), # get specific post impressions
    path("post/account/impression/<int:post_id>", AccountPostImpressionView.as_view()), # get specific liked post
    path("post/account/liked", getAccountLikedPosts), # get all liked posts by specific account
    path("post/metadata", PostMetadataView.as_view()), # create post metadata
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


    #INBOX
    path("inbox/forward", CreateInboxMessage.as_view()), # send an inbox message
    path('inbox/get', InboxMessagesView.as_view()), # get all my inbox messages
    path("inbox/delete/<int:message_id>", deleteInboxMessage), # delete an inbox message


    # RESEARCH
    path("researchPaper/myResearch", MyResearchPaperView.as_view()),
    path("researchPaper/makeImpression/<int:paper_id>", makePaperImpression),
    path("researchPaper/allImpressions/<int:paper_id>", getAllPaperImpressions),
    path("researchPaper/myImpression/<int:paper_id>", getMyPaperImpression),
    path("researchPaper/topResearch", TopResearchPapersView.as_view()),
    path("researchPaper/search", searchPapers),
    path("researchPaper/accountResearch", getAccountResearch),
    path("researchPaper/getPaper/<int:paper_id>", getResearchPaper),


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


    # DATA-HUB
    path("data-hub/query", DataHubQueryView.as_view()),
    path("data-hub/poll/feedback", DataHubFeedbackPollView.as_view()),
    path("data-hub/poll/position", DataHubPollView.as_view()),

]
