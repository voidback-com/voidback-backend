from math import perm
from django.db.models import Q, Count
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Post, PostMetadata, Account, ResearchPaper
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Research import *
from ..models.Research import *
import json
from ..models.Notifications import newNotification



# (publish, retrieve and delete) my research papers
class MyResearchPaperView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: Request):
        try:

            data = json.loads(request.data.get("data", None))

            data['author'] = request.user

            data['pdf'] = request.FILES.get("pdf")

            data['thumbnail'] = request.FILES.get("thumbnail")


            serializer = ResearchPaperSerializer(data=data)

            if serializer.is_valid():
                serializer.create(data)

                return Response(data=serializer.data, status=200)

            return Response(data={"error": serializer.errors}, status=400)

        except Exception:
            return Response(data={"error": "Error publishing the research paper."}, status=400)



    def get(self, request: Request):
        try:
            skip = request.query_params.get("skip", 0)
            limit = request.query_params.get("limit", 10)

            instance = ResearchPaper.objects.all().filter(author=request.user).order_by("-created_at")[int(skip):int(limit)]

            serializer = ResearchPaperSerializer(instance, many=True)

            return Response(data=serializer.data, status=200)

        except Exception:
            return Response(data={"error": "Error retrieving your research papers."}, status=400)


    
    def delete(self, request: Request):
        try:
            paper = request.data.get("paper", None)

            if paper:
                instance = ResearchPaper.objects.all().filter(pk=paper).first()

                if instance:
                    instance.pdf.delete(save=False)
                    instance.delete()

            return Response(data={"message": "success"}, status=200)

        except Exception:
            return Response(data={"error": "Error deleting your research paper, please try again."}, status=400)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makePaperImpression(request: Request, paper_id: int):
    try:
        impression = request.data.get("impression", None)

        impression = int(impression)

        if impression not in [1, 0, -1]:
            return Response(data={"error": "Can't make an unknown impression."}, status=400)

        instance_hash =  f"{request.user.username}:{paper_id}"

        instance = ResearchPaperImpression.objects.all().filter(hash=instance_hash).first()


        if instance:

            if impression == 1:
                newNotification(instance.paper.author, request.user.full_name, f"/research/{instance.paper.id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} liked your research paper!", icon="like")

            elif impression == -1:
                newNotification(instance.paper.author, request.user.full_name, f"/research/{instance.paper.id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} disliked your research paper!", icon="dislike")


            data = {"impression": impression}
            serializer = ResearchPaperImpressionSerializer(instance, data=data, partial=True)

            if serializer.is_valid():
                serializer.update(instance, data)
                return Response(data=serializer.data, status=200)
                
        paper = ResearchPaper.objects.all().filter(pk=paper_id).first()


        if impression == 1:
            newNotification(paper.author, request.user.full_name, f"/research/{paper.id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} liked your research paper!", avatarVerified=request.user.isVerified, icon="like")

        elif impression == -1:
            newNotification(paper.author, request.user.full_name, f"/research/{paper.id}", fromAvatar=request.user.avatar, body=f"@{request.user.username} disliked your research paper!", avatarVerified=request.user.isVerified, icon="dislike")


        data = {"impression": impression, "paper": paper, "account": request.user, "hash": instance_hash}

        serializer = ResearchPaperImpressionSerializer(data=data)

        if serializer.is_valid():
            serializer.create(data)
            return Response(data=serializer.data, status=200)

        return Response(data=serializer.errors, status=400)

    except Exception:
        return Response(data={"error": "Error making an impression on this research paper."}, status=400)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def getAllPaperImpressions(request: Request, paper_id: int):
    try:
        views = ResearchPaperImpression.objects.all().filter(paper=paper_id).count()

        likes = ResearchPaperImpression.objects.all().filter(paper=paper_id, impression=1).count()

        dislikes = ResearchPaperImpression.objects.all().filter(paper=paper_id, impression=-1).count()

        data = {"likes": likes, "dislikes": dislikes, "views": views}

        return Response(data=data, status=200)

    except Exception:
        return Response(data={"error": "Error retrieving research paper impressions."}, status=400)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyPaperImpression(request: Request, paper_id: int):
    try:

        instance_hash =  f"{request.user.username}:{paper_id}"
        impression = ResearchPaperImpression.objects.all().filter(hash=instance_hash).first()

        serializer = ResearchPaperImpressionSerializer(impression)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data={"error": "Error retrieving paper impression!."}, status=400)





class TopResearchPapersView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResearchPaperSerializer
    pagination_class = DefaultSetPagination


    # get the most recent posts with the most impressions
    def get_queryset(self): # 
        return ResearchPaper.objects.annotate(
            nused=Count("paperImpression")
        ).order_by('-nused', "-created_at")




@api_view(['GET'])
@permission_classes([AllowAny])
def searchPapers(request: Request):
    try:
        query = request.query_params.get("query", None)

        instance = ResearchPaper.objects.all().filter(title__icontains=query)[:20]

        serializer = ResearchPaperSerializer(instance, many=True)

        return Response(data=serializer.data, status=200)

    except KeyError:
        return Response(data={"error": "Error searching research papers."}, status=400)



@api_view(['GET'])
@permission_classes([AllowAny])
def getAccountResearch(request: Request):
    try:
        username = request.query_params.get("username", None)

        skip = request.query_params.get("skip", 0)
        limit = request.query_params.get("limit", 10)

        instance = ResearchPaper.objects.all().filter(author=username)[int(skip):int(limit)]

        serializer = ResearchPaperSerializer(instance, many=True)

        return Response(data=serializer.data, status=200)

    except KeyError:
        return Response(data={"error": "Error fetching research papers."}, status=400)




@api_view(['GET'])
@permission_classes([AllowAny])
def getResearchPaper(request: Request, paper_id: int): # by id
    try:

        instance = ResearchPaper.objects.all().filter(pk=paper_id).first()

        serializer = ResearchPaperSerializer(instance)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data={"error": "Error fetching research papers."}, status=400)





