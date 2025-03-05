from collections import Counter
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from Analytics.models import Event
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Post import *
from ..models.Post import *
from ..models.EdgeRoom import EdgeRoom
from ..models.Notifications import newNotification
import json




# create and delete posts
class PostView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: Request):
        try:

            if not request.user.email_verified:
                return Response({"error": "You have to verify your email first, before you can post!"}, status=400)

            data = json.loads(request.data.get("post", None))

            data['author'] = request.user


            data['image'] = request.FILES.get("image", None)


            if data['room']:
                inst =  EdgeRoom.objects.all().filter(name=data['room']).first()
                data['room'] = inst

                if inst:
                    inst.rank+=1
                    inst.save()


            if data['parent_post']:
                inst = Post.objects.all().filter(pk=data['parent_post']).first()
                data['parent_post'] = inst

                if inst:
                    inst.rank+=1
                    inst.save()


            for h in data['hashtags']:
                i = Hashtag.objects.all().filter(hashtag=h['hashtag']).first()
                if i:
                    i.rank+=1
                    i.save()

            for s in data['symbols']:
                i = Symbol.objects.all().filter(symbol=s['symbol']).first()

                if i:
                    i.rank+=1
                    i.save()


            mentions = data['mentions']
            symbols = data['symbols']
            hashtags = data['hashtags']


            serializer = PostSerializer(data=data)

            if serializer.is_valid():

                r = serializer.create(data)


                if data['parent_post']:
                    newNotification(data['parent_post'].author, request.user.full_name, f"/view/post/{r.id}", body=f"@{request.user.username} replied to your post!", fromAvatar=request.user.avatar, avatarVerified=request.user.isVerified, icon="message")

                dat = serializer.data
                dat.update({"id": r.id})


                for m in mentions:
                    if m['username']==request.user.username:
                        continue
                    macc = Account.objects.all().filter(username=m['username']).first()

                    newNotification(macc, request.user.full_name, f"/view/post/{r.id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} mentioned you.", avatarVerified=request.user.isVerified, icon="mention")


                return Response(data=dat, status=200)

            else:
                print("Here")
                return Response(data=serializer.errors, status=400)

        except KeyboardInterrupt:
            return Response(data={"error": "Failed to validate post data, please try again!"},status=400)



    def delete(self, request: Request):
        try:
            instance = Post.objects.all().filter(pk=request.data.get('id')).first() 

            if instance and instance.author.username==request.user.username:
                if instance.image:
                    instance.image.image.delete(save=False)
                instance.delete()

            return Response(status=200)

        except Exception:
            return Response(data={"error": "Failed to delete post, please try again!"}, status=400)



# search posts
@api_view(["GET"])
@permission_classes([AllowAny])
def searchPosts(request):
    try:

        query = request.GET.get("query", None)

        if query:

            topResults = PostMetadata.objects.all().filter(text__contains=query).values("post")
    
            serializer = PostSerializer(topResults, many=True)

            return Response(data=serializer.data, status=200)
        
        else:
            return Response(data={"error": "Error processing empty query!"}, status=200)


    except Exception:
        return Response(data={"error": "Error searching posts!"}, status=400)





# most recent and most viewed posts
def topPosts(exclude: list, username=""):
    try:

        # most recent and highest ranking
        top10 = Post.objects.all().filter(parent_post=None).order_by("-created_at").order_by("-updated_at").order_by('-rank').exclude(pk__in=exclude).exclude(title=None).exclude(room=None).distinct()[0:10]

        serializer = PostSerializer(top10, many=True)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data={"error": "Error fetching top posts!"}, status=400)



# get post by id
@api_view(['GET'])
@permission_classes([AllowAny])
def getPostById(request: Request, post_id: int):
    try:
        instance = Post.objects.all().filter(pk=post_id).first()

        if instance:
            serializer = PostSerializer(instance)

            return Response(data=serializer.data, status=200)

        else:
            return Response(status=404)

    except Exception:
        return Response(data={"error": "failed to fetch liked posts!"}, status=400)






# get account liked posts
@api_view(['GET'])
@permission_classes([AllowAny])
def getAccountLikedPosts(request: Request):
    try:
        username = request.query_params.get("username")
        skip = int(request.query_params.get("skip", 0))
        limit = int(request.query_params.get("limit", 5))

        instance = PostImpression.objects.all().filter(impression=1, account=username).order_by("-created_at").values("post")[skip:limit]

        results = []

        for i in instance:
            results.append(Post.objects.all().filter(pk=i['post']).first())


        if instance:
            serializer = PostSerializer(results, many=True)

            return Response(data=serializer.data, status=200)

        else:
            return Response(data=[], status=200)

    except Exception:
        return Response(data={"error": "failed to fetch liked posts!"}, status=400)




class AuthorPostsView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = DefaultSetPagination
    serializer_class = PostSerializer


    def get_queryset(self):
        try:
            username = self.request.query_params.get("username")
            post_type = self.request.query_params.get("type", None)

            instance = Post.objects.all().filter(author=username).order_by("-created_at") # hybrid of orphan and child posts

            if post_type == "orphan": # original posts without a parent post
                instance = Post.objects.all().filter(author=username, parent_post=None).order_by("-created_at")

            
            elif post_type == "child": # reply posts with a parent post
                instance = Post.objects.all().filter(author=username).exclude(parent_post=None).order_by("-created_at")

            return instance
        except Exception:
            return []



# get posts from specific author
@api_view(["GET"])
@permission_classes([AllowAny])
def getAuthorPosts(request: Request):
    try:
        username = request.data.get("username")

        instance = Post.objects.all().filter(author=username).exclude().order_by("-created_at")

        if instance:

            serializer = PostSerializer(instance, many=True)

            return Response(data=serializer.data, status=200)

        return Response(data=[], status=200)


    except Exception:
        return Response(data={"error": "failed to fetch posts!"}, status=400)



# For you posts
@api_view(['POST'])
@permission_classes([AllowAny]) # available for non authenticated users
def forYou(request: Request):
    try:

        exclude = request.data.get("exclude") # a list of already seen posts to be excluded from the query result



        if not request.user.username:
            return topPosts(exclude)

        else:
            fy = ForYou.objects.filter(account=request.user.username).first()

            if fy:
                posts = Post.objects.all().filter(
                    Q(hashtags__in=fy.hashtags) |
                    Q(symbols__in=fy.symbols) |
                    Q(room__name__in=fy.rooms) |
                    Q(room__categories__category__in=fy.categories) |
                    Q(author__in=fy.accounts),
                    parent_post=None
                ).order_by("-created_at").order_by("-updated_at").order_by("-rank").exclude(pk__in=exclude).exclude(room=None).exclude(title="").distinct()[0:10]


                if len(posts) < 10:
                    return topPosts(exclude, request.user.username)

                serializer = PostSerializer(instance=posts, many=True)

                if posts:
                    return Response(data=serializer.data, status=200)

                else:
                    return topPosts(exclude, username=request.user.username)

            else:
                data = {
                    "hashtags": [],
                    "rooms": [],
                    "categories": [],
                    "symbols": [],
                    "accounts": [],
                    "account": request.user
                }


                fyinstance = ForYou(**data)
                fyinstance.save()

            return topPosts(exclude, username=request.user.username)

    except KeyError:
        return Response(data={"error": "Error fetching pots!"}, status=400)




# get all post impressions
@api_view(['GET'])
@permission_classes([AllowAny])
def getPostImpressions(request: Request, post_id: int):

    try:
        views = PostImpression.objects.all().filter(post=post_id).count()
        likes = PostImpression.objects.all().filter(post=post_id, impression=1).count()
        dislikes = PostImpression.objects.all().filter(post=post_id, impression=-1).count()

        return Response(data={"likes": likes, "dislikes": dislikes, "views": views}, status=200)

    except Exception:
        return Response(data={"error": "Error fetching post impressions"}, status=400)




# create, get, update, delete post impressions for (Account)
class AccountPostImpressionView(APIView):
    permission_classes = [AllowAny]


    def post(self, request: Request, post_id: int):
        try:
            if request.user == 'AnonymousUser':
                return Response(data={"error": "unauthenticated"}, status=400)

            impression = request.data.get("impression", None)

            if impression not in [1, -1, 0]:
                return Response(data={"error": "Error making a post impression!"}, status=400)


            post = Post.objects.filter(pk=post_id).first()

            if not post:
                return Response(data={"error": "Error making a post impression, the post does not exist!"}, status=400)


            # update for you if the impression is positive
            if impression==1:

                fy = ForYou.objects.filter(account=request.user.username).first()
                if fy:
                    for hashtag2 in post.hashtags.all():
                        if hashtag2.id not in fy.hashtags:
                            fy.hashtags.append(hashtag2.id)


                    for symbol2 in post.symbols.all():
                        if symbol2.id not in fy.symbols:
                            fy.symbols.append(symbol2.id)


                    
                    if post.author.username not in fy.accounts and post.author.username == request.user.username:
                        fy.accounts.append(post.author.username)

                fy.save()


            impression_hash = f"{request.user.username}:{post_id}"

            data = {"post": post_id, "impression": impression, "account": request.user, "hash": impression_hash}


            instance = PostImpression.objects.all().filter(hash=impression_hash).first()

            serializer = PostImpressionSerializer(data=data)

            if impression==1:
                newNotification(post.author, request.user.full_name, f"/view/post/{post_id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} liked your post!", avatarVerified=request.user.isVerified, icon="like")

            elif impression==-1:
                newNotification(post.author, request.user.full_name, f"/view/post/{post_id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} disliked your post!", avatarVerified=request.user.isVerified, icon="dislike")

            if instance:

                serializer = PostImpressionSerializer(data=data, instance=instance, partial=True)

                if serializer.is_valid():
                    serializer.update(instance, {"impression": impression})
                    return Response(data=serializer.data, status=200)

                return Response(data=serializer.errors, status=400)


            else:
                if impression == -1:
                    post.rank -= 1
                    post.save()
                else:
                    post.rank += 1
                    post.save()
                    
                if serializer.is_valid():
                    serializer.create(data)
                    return Response(data=serializer.data, status=200)

            return Response(data=serializer.errors, status=400)

        except Exception:
            return Response(data={"error": "Error making a post impression!"}, status=400)



    def get(self, request: Request, post_id: int):
        try:
            instance = PostImpression.objects.all().filter(post=post_id, account=request.user.username).first()

            if instance:
                serializer = PostImpressionSerializer(instance)
                return Response(data=serializer.data, status=200)
            
            return Response(status=404)

        except Exception:
            return Response(data={"error": "Error retrieving post impression!"}, status=400)





# create a new hashtag
class HashtagView(APIView):
    permission_classes = [IsAuthenticated]
 

    def post(self, request: Request):
        try:
            data = request.data

            if data:

                serializer = HashtagSerializer(data=data)

                if serializer.is_valid():
                    serializer.create(data);
                    return Response(data=serializer.data, status=200)
                else:
                    return Response(data=serializer.errors, status=400)
            else:
                return Response(data="Error processing the hashtag!", status=400)
                
        except Exception:
            return Response(status=400)

       


# create a new symbol
class SymbolView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: Request):
        try:
            data = request.data

            if data:

                serializer = SymbolSerializer(data=data)

                if serializer.is_valid():
                    serializer.create(data);
                    return Response(data=serializer.data, status=200)
                else:
                    return Response(data=serializer.errors, status=400)
            else:
                return Response(data="Error processing the hashtag!", status=400)
                
        except Exception:
            return Response(status=400)




# get top 5 trending hashtags (autocomplete)
@api_view(['GET'])
@permission_classes([AllowAny])
def getTrendingHashtags(request):
    try:

        # most posts and most recent (descending)
        top5 = Hashtag.objects.all().order_by("-created_at").order_by("-rank")[:5]

        data = list()

        for s in top5:
            events = Event.objects.all().filter(
                event_type="view-hashtag-posts",
                data={"hashtag": s.hashtag}
            ).values("device__country", "device__city").order_by("-created_at")[0:10] # top 10 last countries that viewed this hashtag

            
            events = list(events)

            if len(events):
                most_common = Counter([inst['device__country'] for inst in events]).most_common(1)

                if len(most_common):
                    most_common = most_common[0][0]
                else:
                    most_common = Counter([inst['device__city'] for inst in events]).most_common(1)

                    if len(most_common):
                        most_common = most_common[0][0]

                    else:
                        most_common = ""
            else:
                most_common = ""


            s = HashtagSerializer(s)

            dat = dict()

            dat.update(s.data)

            dat.update({"location":  most_common})


            data.append(dat)


        return Response(data=data, status=200)

    except Exception:
        return Response(data={"error": "Error retrieving trending hashtags!"}, status=400)



# search for a hashtag (used by autocomplete)
@api_view(['GET'])
@permission_classes([AllowAny])
def searchHashtags(request: Request):
    try:

        query = request.GET.get("query", None)

        if query:
            topResults = Hashtag.objects.all().filter(hashtag__contains=query)[:10]

    
            serializer = HashtagSerializer(topResults, many=True)

            return Response(data=serializer.data, status=200)
        
        else:
            return Response(data=[], status=200)


    except Exception:
        return Response(data=[], status=400)




# return top 5 most used symbols latley
@api_view(['GET'])
@permission_classes([AllowAny])
def getTrendingSymbols(request):
    try:

        # most posts and most recent (descending)
        top5 = Symbol.objects.all().order_by("-created_at").order_by("-rank")[:5]


        data = list()

        for s in top5:
            events = Event.objects.all().filter(
                event_type="view-symbol-posts",
                data={"symbol": s.symbol},
            ).values("device__country", "device__city").order_by("-created_at")[0:10] # top 10 last countries that viewed this symbol's
            
            events = list(events)


            if len(events):
                most_common = Counter([inst['device__country'] for inst in events]).most_common(1)

                if len(most_common):
                    most_common = most_common[0][0]
                else:
                    most_common = Counter([inst['device__city'] for inst in events]).most_common(1)

                    if len(most_common):
                        most_common = most_common[0][0]

                    else:
                        most_common = ""
            else:
                most_common = ""

            s = SymbolSerializer(s)

            dat = dict()

            dat.update(s.data)

            dat.update({"location":  most_common})

            data.append(dat)

        return Response(data=data, status=200)

    except Exception:
        return Response(data={"error": "Error retrieving trending symbols!"}, status=400)



# search for a symbol (used by autocomplete)
@api_view(['GET'])
@permission_classes([AllowAny])
def searchSymbols(request: Request):
    try:

        query = request.GET.get("query", None)

        if query:
            topResults = Symbol.objects.all().filter(symbol__contains=query)[:10]

    
            serializer = SymbolSerializer(topResults, many=True)

            return Response(data=serializer.data, status=200)
        
        else:
            return Response(data=[], status=200)


    except Exception:
        return Response(data=[], status=200)



# get the hashtag posts count
@api_view(['GET'])
@permission_classes([AllowAny])
def getHashtagPostsCount(request: Request, hashtag: int):
    try:

        count = Post.objects.all().filter(hashtags__pk=hashtag).count()

        return Response(data={"posts": count}, status=200)

    except Exception:
        return Response(data={"posts": 1}, status=200)




# get the symbol posts count
@api_view(['GET'])
@permission_classes([AllowAny])
def getSymbolPostsCount(request: Request, symbol: int):
    try:

        count = Post.objects.all().filter(symbols__pk=symbol).count()

        return Response(data={"posts": count}, status=200)

    except Exception:
        return Response(data={"posts": 1}, status=200)







# get replies-count of parent post
@api_view(['GET'])
@permission_classes([AllowAny])
def getPostRepliesCount(request: Request, parent_post_id: int):
    try:

        count = Post.objects.all().filter(parent_post=parent_post_id).count()

        return Response(data={"replies": count}, status=200)

    except Exception:
        return Response(data={"replies": 0}, status=200)





# get replies of parent post
class PostRepliesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    pagination_class = DefaultSetPagination

    def get_queryset(self): # ?parent_post=[id]
        parent = self.request.query_params.get("parent_post", None)


        if parent:
            return Post.objects.all().filter(parent_post=parent).order_by("-created_at")
        return []






@api_view(["GET"])
@permission_classes([AllowAny])
def getSymbolPosts(request: Request, symbol: str):
    try:
        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        posts = Post.objects.all().filter(symbols__symbol=symbol).order_by("-created_at")[int(skip):int(limit)]

        serializer = PostSerializer(posts, many=True)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data={"error": f"Error fetching symbol posts!"}, status=200)






@api_view(["GET"])
@permission_classes([AllowAny])
def getHashtagPosts(request: Request, hashtag: str):
    try:
        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        posts = Post.objects.all().filter(hashtags__hashtag=hashtag).order_by("-created_at")[int(skip):int(limit)]

        serializer = PostSerializer(posts, many=True)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data={"error": f"Error fetching symbol posts!"}, status=200)




