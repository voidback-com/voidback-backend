from django.db.models import Q, Count
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Analytics.models import Event
from voidbackApi.models.Post import ForYou
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Post import Symbol
from ..models.dataHub import *
from ..serializers.dataHub import DataHubQuerySerializer, DataHubAccountSerializer, DataHubPositionPollSerializer, DataHubFeedbackPollSerializer
from ..serializers.Post import PostMetadata, PostImpression, PostMetadataSerializer
import json



def canQuery(account):
    today = timezone.now()
    start_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
    end_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
    # all todays queries
    queries = DataHubQuery.objects.all().filter(account=account, created_at__range=[start_date, end_date]).count()


    if queries < 10:
        account.queries_left = 10-queries
        account.save()
        return True

    elif queries == 10:
        account.queries_left = 0
        account.save()
        return False



def querySymbol(qdata, account):
    try:
        totalPosts = PostMetadata.objects.all().filter( 
            Q(text__icontains=qdata['includes_keywords']),
            post__created_at__range=[qdata['startDate'], qdata['endDate']],
            post__symbols__id__exact=qdata['symbol']
           ).count()


        total_likes = PostImpression.objects.all().filter(
            post__symbols__id__exact=qdata['symbol'],
            impression=1, 
            post__created_at__range=[qdata['startDate'], qdata['endDate']]
        ).count()

        total_dislikes = PostImpression.objects.all().filter(
            post__symbols__id__exact=qdata['symbol'],
            impression=-1, 
            post__created_at__range=[qdata['startDate'], qdata['endDate']]
        ).count()


        total_views = PostImpression.objects.all().filter(
            post__symbols__id__exact=qdata['symbol'],
            post__created_at__range=[qdata['startDate'], qdata['endDate']]
        ).count()


        # top post in the date range specified
        topPost = Post.objects.all().filter(
            symbols__id__exact=qdata['symbol'],

            created_at__range=[qdata['startDate'], qdata['endDate']],

        ).order_by("-rank").first()


        if topPost:
            topPostMetadata = PostMetadataSerializer(instance=PostMetadata.objects.get(pk=topPost.pk)).data
        else:
            topPostMetadata = None


        total_positive_sentiments_count = PostMetadata.objects.all().filter(
            Q(text__icontains=qdata['includes_keywords']),
            post__symbols__id__exact=qdata['symbol'],
            post__created_at__range=[qdata['startDate'], qdata['endDate']], 
            text_sentiment='POSITIVE',
        ).count()

        try:
            positive_sentiments_percentage = total_positive_sentiments_count/totalPosts * 100
        except ZeroDivisionError:
            positive_sentiments_percentage = 0


        total_negative_sentiments_count = PostMetadata.objects.all().filter(
            Q(text__icontains=qdata['includes_keywords']),
            post__created_at__range=[qdata['startDate'], qdata['endDate']],                       text_sentiment='NEGATIVE', 
            post__symbols__id__exact=qdata['symbol'],
        ).count()

        try:
            negative_sentiments_percentage = total_negative_sentiments_count/totalPosts * 100
        except ZeroDivisionError:
            negative_sentiments_percentage = 0


        ticker = Symbol.objects.get(pk=qdata['symbol']).symbol


        total_SymbolPostsViewedEvents = Event.objects.all().filter(
            event_type='view-symbol-posts',
            data={"symbol": ticker},
            created_at__range=[qdata['startDate'], qdata['endDate']]
        ).count()


        symbolsInForyous = ForYou.objects.all().filter(
            Q(symbols__icontains=qdata['symbol']),
            created_at__range=[qdata['startDate'], qdata['endDate']]
        ).count()

        data = {
            "ticker": ticker,
            "totalPosts": totalPosts,
            "totalViews": total_views,
            "totalLikes": total_likes,
            "totalDislikes": total_dislikes,
            "topPost": topPostMetadata,
            "positiveSentiments": {"count": total_positive_sentiments_count, "percentage": positive_sentiments_percentage},
            "negativeSentiments": {"count": total_negative_sentiments_count, "percentage": negative_sentiments_percentage},
            "symbolPostsViewedEvents": total_SymbolPostsViewedEvents,
            "symbolsInForYous": symbolsInForyous,
            "dateRange": [qdata['startDate'], qdata['endDate']]
        }

        dhq = {
            "query": qdata['symbol'],
            "query_category": "symbol",
            "query_startDate": qdata['startDate'],
            "query_endDate": qdata['endDate'],
            "includes_keywords": qdata['includes_keywords'],
            'query_results': data,
            "account": account
        }

        i = DataHubQuerySerializer(data=dhq)

        if i.is_valid():
            i.create(dhq)
            return Response(i.data, status=200)

        return Response(status=400)

    except Exception:
        return Response(status=400)




# make, view and delete queries made in the past
class DataHubQueryView(APIView):
    permission_classes = [IsAuthenticated]


    # get previous queries
    def get(self, request: Request):
        try:
            skip, limit = request.query_params.get("skip", 0), request.query_params.get("limit", 10)

            acc = DataHubAccount.objects.all().filter(account=request.user.username).first()

            if not acc:
                return Response(data={"queries": [], "queriesLeft": 0}, status=200)

            queries = DataHubQuery.objects.all().filter(account=acc).order_by("-created_at")[int(skip):int(limit)]

            serializer = DataHubQuerySerializer(queries, many=True)

            q = serializer.data

            return Response(data={"queries": q, "queriesLeft": acc.queries_left}, status=200)

        except KeyboardInterrupt:
            return Response(status=400)


    # make a query
    def post(self, request: Request):
        try:

            category = request.data.pop("category")
            startDate = request.data.pop("startDate")
            endDate = request.data.pop("endDate")

            request.data['startDate'] = f"{startDate['year']}-{startDate['month']}-{startDate['day']}"

            request.data['endDate'] = f"{endDate['year']}-{endDate['month']}-{endDate['day']}"


            acc = DataHubAccount.objects.all().filter(account=request.user.username).first()

            if not acc:
                acc = DataHubAccount(account=request.user)
                acc.save()

            if canQuery(acc):

                if category=="symbol":
                    q = querySymbol(request.data, acc)
                    return q

                else:
                    return Response({"error": "Unknown query category!"}, status=400)


            else:
                return Response({"error": "You've reached your daily query limit, please respect our terms of service!"}, status=400)


        except Exception:
            return Response(data={"error": "Failed to process your query, please try again!"},status=400)



    # delete a query by it's id
    def delete(self, request: Request):
        try:
            qid = request.data.get("id")

            obj = DataHubQuery.objects.all().filter(pk=qid).first()

            if obj:
                obj.delete()
                return Response(status=200)
            
            return Response(status=400)

        except Exception:
            return Response(status=400)







# make and get votes
class DataHubPollView(APIView):
    permission_classes = [IsAuthenticated]


    # get all votes and positions
    def get(self, request: Request):
        try:

            ticker = request.query_params.get("ticker")

            votes = DataHubPositionPoll.objects.all().filter(ticker=ticker).count()

            firstp = DataHubPositionPoll.objects.all().filter(ticker=ticker, position=1).count()
            secondp = DataHubPositionPoll.objects.all().filter(ticker=ticker, position=2).count()
            thirdp = DataHubPositionPoll.objects.all().filter(ticker=ticker, position=3).count()
            fourthp = DataHubPositionPoll.objects.all().filter(ticker=ticker, position=4).count()

            voted = DataHubPositionPoll.objects.all().filter(ticker=ticker, account__account=request.user).first()


            if not voted:
                voted = None
            else:
                voted = voted.position


            return Response(data={
                "votes": votes,
                "positions": [firstp, secondp, thirdp, fourthp],
                "voted": voted
            }, status=200)

        except Exception:
            return Response(status=400)


    # vote
    def post(self, request: Request):
        try:
            position = request.data.get("position")
            ticker = request.data.get("ticker")


            acc = DataHubAccount.objects.all().filter(account=request.user.username).first()

            if not acc:
                acc = DataHubAccount(account=request.user)
                acc.save()


            t = Symbol.objects.all().filter(symbol=ticker).first()
            
            if not t:
                return Response({"error": "Failed to process your vote, please try again!"}, status=400)

            dat = {"position": position, "ticker": ticker, "account": acc, "hash": f"{acc.account.username}:{position}:{ticker}"}

            s = DataHubPositionPollSerializer(data=dat)

            if s.is_valid():
                s.create(dat)
                return Response({"error": None}, status=200)


            return Response({"error": "Failed to process your vote, please try again!"}, status=400)

        except Exception:
            return Response(data={"error": "Failed to process your vote, please try again!"},status=400)




# make and get votes
class DataHubFeedbackPollView(APIView):
    permission_classes = [IsAuthenticated]


    # get all votes and positions
    def get(self, request: Request):
        try:

            ticker = request.query_params.get("ticker")

            votes = DataHubFeedbackPoll.objects.all().filter(ticker=ticker).count()

            firstp = DataHubFeedbackPoll.objects.all().filter(ticker=ticker, position=1).count()
            secondp = DataHubFeedbackPoll.objects.all().filter(ticker=ticker, position=2).count()
            thirdp = DataHubFeedbackPoll.objects.all().filter(ticker=ticker, position=3).count()
            fourthp = DataHubFeedbackPoll.objects.all().filter(ticker=ticker, position=4).count()


            voted = DataHubFeedbackPoll.objects.all().filter(ticker=ticker, account__account=request.user).first()


            if not voted:
                voted = None
            else:
                voted = voted.position


            return Response(data={
                "votes": votes,
                "positions": [firstp, secondp, thirdp, fourthp],
                "voted": voted
            }, status=200)

        except Exception:
            return Response(status=400)


    # vote
    def post(self, request: Request):
        try:
            position = request.data.get("position")
            ticker = request.data.get("ticker")


            acc = DataHubAccount.objects.all().filter(account=request.user.username).first()

            if not acc:
                acc = DataHubAccount(account=request.user)
                acc.save()


            t = Symbol.objects.all().filter(symbol=ticker).first()
            
            if not t:
                return Response({"error": "Failed to process your vote, please try again!"}, status=400)

            dat = {"position": position, "ticker": ticker, "account": acc, "hash": f"{acc.account.username}:{position}:{ticker}"}

            s = DataHubFeedbackPollSerializer(data=dat)

            if s.is_valid():
                s.create(dat)
                return Response({"error": None}, status=200)


            return Response({"error": "Failed to process your vote, please try again!"}, status=400)

        except Exception:
            return Response(data={"error": "Failed to process your vote, please try again!"},status=400)


