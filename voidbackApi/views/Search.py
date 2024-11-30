from functools import reduce
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Search import *
from ..serializers import AccountSerializer, ResearchPaperSerializer, PostMetadata, PostSerializer, ResearchPaper, Account
from ..models.Search import *



# create and get top search queries
class SearchQueryView(APIView):
    permission_classes = [AllowAny]

    # when the user hits eneter on a query send a post instead of a get
    def post(self, request: Request):
        try:

            dat = request.data

            instance = SearchQuery.objects.all().filter(query=dat.get("query")).first()


            if instance:
                instance.rank+=1
                instance.save()

                serializer = SearchQuerySerializer(instance)

                return Response(data=serializer.data, status=200)

            else:
                serializer = SearchQuerySerializer(data=dat) 
                if serializer.is_valid():
                    serializer.create(dat)
                    return Response(data=serializer.data, status=200)

            return Response(data=[], status=200)
        except KeyboardInterrupt:
            return Response(status=400)



    # when a user is in the process of typing a query send a get
    def get(self, request: Request):
        try:
            query = request.GET.get("query", None)
            object_name = request.GET.get("object", None)

            if query and object_name:
                instance = SearchQuery.objects.all().filter(query__contains=query, object_name=object_name).order_by("-created_at")[:10]

                if instance:
                    serializer = SearchQuerySerializer(instance, many=True) 
                    return Response(data=serializer.data, status=200)

                return Response(status=400)
            else:
                if object_name:
                    instance = SearchQuery.objects.all().filter(object_name=object_name).order_by("-rank", "-created_at")[:10]
                else:
                    instance = SearchQuery.objects.all().order_by("-rank", "-created_at")[:10]


                if instance:
                    serializer = SearchQuerySerializer(instance, many=True) 
                    return Response(data=serializer.data, status=200)
                    
                return Response(status=400)
        except Exception:
            return Response(status=400)







@api_view(['GET'])
@permission_classes([AllowAny])
def exploreSearch(request: Request):
    try:

        query = request.query_params.get("query", None)
        skip = request.query_params.get("skip", None)
        limit = request.query_params.get("limit", None)
        category = request.query_params.get("category", None)


        skip = int(skip)
        limit = int(limit)



        if category == "research":
            instance = ResearchPaper.objects.all().filter(title__icontains=query).order_by("-created_at")[skip:limit]

            serializer = ResearchPaperSerializer(instance, many=True)

            return Response(serializer.data, status=200)


        elif category == "accounts":
            instance = Account.objects.all().filter(username__icontains=query, full_name__icontains=query).order_by("-created_at")[skip:limit]

            serializer = AccountSerializer(instance, many=True)

            return Response(serializer.data, status=200)
        

        else:
            posts = []
            instance = PostMetadata.objects.all().filter(text__icontains=query)[skip:limit]

            for i in instance:
                posts.append(i.post)

            serializer = PostSerializer(posts, many=True)

            return Response(serializer.data, status=200)



    except Exception:
        return Response(data={"error": "unexpected search query!"}, status=400)




@api_view(['GET'])
@permission_classes([AllowAny])
def exploreSearchCount(request: Request):
    try:
        query = request.query_params.get("query", None)

        postCount = PostMetadata.objects.all().filter(text__icontains=query).count()
        researchCount = ResearchPaper.objects.all().filter(title__icontains=query).count()
        accountCount = Account.objects.all().filter(username__icontains=query, full_name__icontains=query).count()

        return Response({"posts": postCount, "research": researchCount, "accounts": accountCount})

    except Exception:
        return Response(data={"error": "unexpected search query!"}, status=400)


