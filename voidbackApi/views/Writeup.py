from collections import Counter
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from voidbackApi.tasks.notifications import create_notification
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Writeup import *
from ..models.Writeup import *
import json
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend




# create and delete writeup
class WriteUpView(APIView):
    permission_classes = [IsAuthenticated]



    def post(self, request: Request):
        try:

            data = json.loads(request.data.get("writeUp", None))

            data['author'] = request.user

            
            if data['series']:
                data['series'] = Series.objects.all().filter(pk=data['series']).first()


            data['thumbnail'] = request.FILES.get("thumbnail", None)

            serializer = WriteUpSerializer(data=data)

            if serializer.is_valid():

                r = serializer.create(data)

                dat = serializer.data
                dat.update({"id": r.id})

                return Response(data=dat, status=200)

            else:
                return Response(data=serializer.errors, status=400)

        except Exception:
            return Response(data={"error": "Failed to validate write up, please try again!"},status=400)



    def delete(self, request: Request):
        try:
            instance = WriteUp.objects.all().filter(pk=request.data.get('id')).first() 

            if instance and instance.author.username==request.user.username:
                instance.thumbnail.thumbnail.delete(save=False)
                instance.delete()

            return Response(status=200)

        except Exception:
            return Response(data={"error": "Failed to delete post, please try again!"}, status=400)






@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMySeries(request: Request):
    try:
        series = Series.objects.all().filter(author=request.user).order_by("-created_at")
        s = SeriesSerializer(series, many=True)
        return Response(data=s.data, status=200)
    except Exception:
        return Response(data={"error": "Failed to fetch your series!"}, status=400)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newSeries(request: Request):
    try:
        data = request.data


        data['author'] = request.user

        s = SeriesSerializer(data=data)

        if s.is_valid():
            s.create(data)

            series = Series.objects.all().filter(author=request.user).order_by("-created_at")
            sres = SeriesSerializer(series, many=True)

            return Response(data=sres.data, status=200)

        return Response(data={"error": s.errors}, status=400)
    except Exception:
        return Response(data={"error": "Failed to validate new series!"}, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSeries(request: Request):
    try:
        sid = request.data.get("id")

        s = Series.objects.all().filter(pk=sid).first()
        
        if s and s.author==request.user:
            s.delete()

        return Response(status=200)
    except Exception:
        return Response(status=400)





class TagsListView(ListAPIView):     
    queryset = Tag.objects.all().order_by("-rank", "-updated_at")     
    serializer_class = TagSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination


    # check if the user is authenticated and return tags based on foryou instance of the user -> (if none or unauthenticated) return trending tags
    # def get_queryset(self):
    #     try:
    #         pass 
    #




class WriteUpListView(ListAPIView):     
    queryset = WriteUp.objects.all().order_by("-created_at", '-updated_at')     
    serializer_class = WriteUpSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "content", "description", 'tags__tag', 'author__username', "series__name", "author__full_name"]


    # return's personalized write ups if the user is authenticated else: the most recent trending write ups
    def get_queryset(self):
        try:

            series = self.request.query_params.get("series", None)

            if series:
                queryset = WriteUp.objects.all().filter(series__name=series).order_by("-created_at")
                return queryset


            queryset = WriteUp.objects.all().order_by("-created_at", '-updated_at')     

            if self.request.user.is_authenticated:
                fy = ForYou.objects.all().filter(account=self.request.user).first()

                if fy:
                    queryset = WriteUp.objects.all().filter(
                        Q(tags__tag__in=fy.tags) |
                        Q(series__name__in=fy.series) |
                        Q(author__username__in=fy.authors)
                    ).order_by("-created_at", "-updated_at")

                    return queryset

                return queryset

            return queryset

        except Exception:
            return []



@api_view(['GET'])
@permission_classes([AllowAny])
def getWriteUp(request: Request):
    try:
        wid = request.query_params.get("id", None)


        inst = WriteUp.objects.all().filter(pk=wid).first()

        if not inst:
            return Response(data={"error": "Not Found!"}, status=404)
        else:
            # create neutral impression if none exist
            if request.user.is_authenticated:
                imp = WriteUpImpression.objects.all().filter(writeup=inst, account=request.user).first()
                if not imp:
                    imp = WriteUpImpression(account=request.user, impression=0, writeup=inst, hash=f"{request.user.id}:{inst.id}")
                    imp.save()


        s = WriteUpSerializer(inst)

        return Response(data=s.data, status=200)

    except Exception:
        return Response(data={"error": "Failed to fetch write up!"}, status=400)




@api_view(["GET"])
@permission_classes([AllowAny])
# return impressions and account impression of the write up
def getImpressions(request: Request):
    try:
        wid = request.query_params.get("writeup") # writeup id

        writeupImp = None

        if request.user.is_authenticated:
            writeupImp = WriteUpImpression.objects.all().filter(writeup=wid, account=request.user).first()
            if writeupImp:
                writeupImp = writeupImp.impression


        writeUpLikes = WriteUpImpression.objects.all().filter(writeup=wid, impression=1).count()

        writeUpViews = WriteUpImpression.objects.all().filter(writeup=wid).count()

        return Response(data={"views": writeUpViews, "likes": writeUpLikes, "impression": writeupImp}, status=200)

    except Exception:
        return Response(data={"error": "Failed to fetch write up impressions!"}, status=400)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def likeWriteUp(request: Request):
    try:
        wid = request.query_params.get("writeup") # writeup id

        writeupImp = WriteUpImpression.objects.all().filter(writeup=wid, account=request.user).first()

        if not writeupImp:
            w = WriteUp.objects.all().filter(pk=wid).first()
            writeupImp = WriteUpImpression.objects.create(writeup=w, account=request.user, impression=0, hash=f"{request.user.username}:{wid}")


        if writeupImp.impression == 0:
            writeupImp.impression = 1
            writeupImp.save()

        else:
            writeupImp.impression = 0
            writeupImp.save()


        fy = ForYou.objects.all().filter(account=request.user).first()

        if not fy:
            fy = ForYou(account=request.user)

            fy.save()



        inst = WriteUp.objects.all().filter(pk=wid).first()

        ser_inst = WriteUpSerializer(inst).data


        if ser_inst['tags']:
            for t in ser_inst['tags']:
                if t['tag'] not in fy.tags:
                    fy.tags.append(t['tag'])


        if ser_inst['series']:
            if ser_inst['series']['name'] not in fy.series:
                fy.series.append(ser_inst['series']['name'])


        if ser_inst['author']['username'] not in fy.authors:
            fy.authors.append(ser_inst['author']['username'])


        fy.save()


        likes = WriteUpImpression.objects.all().filter(writeup=wid, impression=1).count()

        views = WriteUpImpression.objects.all().filter(writeup=wid).count()


        if inst.author!=request.user and writeupImp.impression==1:

            create_notification(inst.author, {
                "from": PublicAccountSerializer(request.user).data,
                "title": f"@{request.user.username} read and liked your write-up.",
                "objectType": "writeup",
                "object": WriteUpSerializer(inst).data,
                "icon": "heart",
                "link": f"/view/writeup/{wid}"
            })



        return Response(data={"impression": writeupImp.impression, "likes": likes, "views": views}, status=200)

    except Exception:
        return Response(data={"error": "Failed to make an impression!"}, status=400)






# create and delete comment
class CommentView(APIView):
    permission_classes = [IsAuthenticated]



    def post(self, request: Request):
        try:

            data = request.data

            if data['parent']:
                c = Comment.objects.all().filter(pk=int(data['parent'])).first()
                data['parent'] = c

                c.rank+=1 # increment rank of comment
                c.save()


            data['author'] = request.user

            serializer = CommentSerializer(data=data)


            if serializer.is_valid():

                r = serializer.create(data)


                if r.parent and r.parent.author != request.user:
                    create_notification(r.parent.author, {
                        "from": PublicAccountSerializer(request.user).data,
                        "title": f"@{request.user.username} replied to your comment.",
                        "objectType": "comment",
                        "object": CommentSerializer(r).data,
                        "icon": "chat",
                        "link": f"/view/writeup/{r.writeup.id}"
                    })


                elif r.writeup.author != request.user:
                    create_notification(r.writeup.author, {
                        "from": PublicAccountSerializer(request.user).data,
                        "title": f"@{request.user.username} commented on your write up.",
                        "objectType": "comment",
                        "object": CommentSerializer(r).data,
                        "icon": "chat",
                        "link": f"/view/writeup/{r.writeup.id}"
                    })


                return Response(data=CommentSerializer(r).data, status=200)

            else:
                return Response(data=serializer.errors, status=400)

        except Exception:
            return Response(data={"error": "Failed to validate comment, please try again!"},status=400)



    def delete(self, request: Request):
        try:
            instance = Comment.objects.all().filter(pk=request.data.get('id')).first() 

            if instance and instance.author.username==request.user.username:
                instance.delete()

            return Response(status=200)

        except Exception:
            return Response(data={"error": "Failed to delete comment, please try again!"}, status=400)





class CommentListView(ListAPIView):     
    queryset = Comment.objects.all().order_by("-created_at")     
    serializer_class = CommentSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['comment', 'author__username', "author__full_name"]



    def get_queryset(self):
        try:

            sortby = self.request.query_params.get("sortby", "top")
            # sortby: my, latest, top

                # my: my comments first
                # new: newest comments first
                # top: most replied to comments first

            if sortby=="latest":
                queryset_latest = Comment.objects.all().filter(writeup=self.request.query_params.get("writeup"), parent=self.request.query_params.get("parent", None)).order_by("-created_at")     

                return queryset_latest


            elif sortby=="my":
                queryset_my = Comment.objects.all().filter(writeup=self.request.query_params.get("writeup"), parent=self.request.query_params.get("parent", None), author=self.request.user).order_by("-created_at")     

                return queryset_my


            else:
                queryset_top = Comment.objects.all().filter(writeup=self.request.query_params.get("writeup"), parent=self.request.query_params.get("parent", None)).order_by("-rank", "-created_at")     

                return queryset_top
        except Exception:
            return []




@api_view(['GET'])
@permission_classes([AllowAny])
def commentsCount(request: Request):
    try:
        wid = request.query_params.get("writeup", None)
        parent = request.query_params.get("parent", None)

        
        qcount = Comment.objects.all().filter(writeup=wid, parent=parent).count() 

        return Response(data={"count": qcount}, status=200)

    except Exception:
        return Response(data={"error": "Failed to fetch comments count, please try again!"}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def likeComment(request: Request):
    try:
        cid = request.query_params.get("comment") # comment id

        commentImp = CommentImpression.objects.all().filter(comment=cid, account=request.user).first()

        if commentImp:
            if commentImp.impression == 0:
                commentImp.impression = 1
                commentImp.save()

            else:
                commentImp.impression = 0
                commentImp.save()

            likes = CommentImpression.objects.all().filter(comment=cid, impression=1).count()

            return Response(data={"impression": commentImp.impression, "likes": likes}, status=200)

        else:

            data = {"account": request.user, "comment": cid, "impression": 1, "hash": f"{request.user.id}:{cid}"}
            ser = CommentImpressionSerializer(data=data)

            if ser.is_valid():
                ser.create(data)

                likes = CommentImpression.objects.all().filter(comment=cid, impression=1).count()

                return Response(data={"impression": ser.impression, "likes": likes}, status=200)


            return Response(data=ser.errors, status=400)

    except Exception:
        return Response(data={"error": "Failed to make an impression!"}, status=400)




@api_view(["GET"])
@permission_classes([AllowAny])
# return comment impressions and account impression
def getCommentImpressions(request: Request):
    try:
        cid = request.query_params.get("comment") # comment id

        commentImp = None

        if request.user.is_authenticated:
            commentImp = CommentImpression.objects.all().filter(comment=cid, account=request.user).first()
            if commentImp:
                commentImp = commentImp.impression


        commentLikes = CommentImpression.objects.all().filter(comment=cid, impression=1).count()

        return Response(data={"likes": commentLikes, "impression": commentImp}, status=200)

    except Exception:
        return Response(data={"error": "Failed to fetch comment impressions!"}, status=400)






# returns write ups & series by this author
class AccountWriteUpListView(ListAPIView):     
    queryset = []
    serializer_class = WriteUpSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination


    def get_queryset(self):
        try:
            series = self.request.query_params.get("series") # series name
            author = self.request.query_params.get("author") # author's username


            if series and author:
                queryset = WriteUp.objects.all().filter(author__username=author, series__name=series).order_by("-created_at", "-updated_at")
                return queryset


            if not series and author:
                queryset = WriteUp.objects.all().filter(author__username=author).order_by("-created_at", "-updated_at")
                return queryset


            return []

        except Exception:
            return []




class SeriesListView(ListAPIView):     
    queryset = []
    serializer_class = SeriesSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination


    # return's personalized write ups if the user is authenticated else: the most recent trending write ups
    def get_queryset(self):
        try:
            author = self.request.query_params.get("author") # author's username

            if author:
                queryset = Series.objects.all().filter(author__username=author).order_by("-created_at", "-updated_at")
                return queryset

            return []
        except Exception:
            return []




# returns write ups liked by the given username
class LikedWriteUpListView(ListAPIView):     
    queryset = []
    serializer_class = WriteUpSerializer     
    permission_classes = [AllowAny]     
    pagination_class = DefaultSetPagination


    def get_queryset(self):
        try:
            account = self.request.query_params.get("account", None) # account username


            if account:
                queryset = WriteUp.objects.all().filter(
                    pk__in=WriteUpImpression.objects.all().filter(account__username=account, impression=1).order_by("-created_at").values("writeup")
                )

                return queryset

            return []

        except Exception:
            return []







