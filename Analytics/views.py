from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.utils import timezone

from voidbackApi.models.Post import Hashtag, Symbol
from .serializers import EventSerializer, Event
import plotly.graph_objects as go




@api_view(['POST'])
@permission_classes([AllowAny])
def logEvent(request: Request):
    try:
        
        event = request.data

        serializer = EventSerializer(data=event)



        if serializer.is_valid():
            serializer.create(event)


            if event.get("event_type") == "view-hashtag-posts":
                inst = Hashtag.objects.all().filter(hashtag=event.get("data")['hashtag']).first()

                if inst:
                    now = timezone.now()

                    if inst.created_at+timezone.timedelta(days=30) < now and inst.updated_at+timezone.timedelta(hours=1) < now:
                        # if the Hashtag was created longer than 30 days ago and updated longer than an hour ago then reset it's rank (only the yound and brave survive)
                        inst.rank=0
                        inst.save()
                    else:
                        if inst.updated_at+timezone.timedelta(minutes=10) > now:
                            # if the Hashtag was updated in the last 10 minutes then increment the rank plus a 100
                            inst.rank+=1
                            # hot af rn
                            inst.save() 

                        elif inst.updated_at+timezone.timedelta(hours=1) > now:
                            # if the Hashtag was updated in the last hour then increment the rank
                            inst.rank+=1
                            # picking up steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(hours=4) < now:
                            # if this hashtag's rank was updated in the last 4 hours or more
                            # then decrement the rank (because it's falling off)
                            inst.rank-=1
                            # loosing steam
                            inst.save()

                        elif inst.updated_at+timezone.timedelta(days=1) < now:
                            # if the hashtag was last updated 1 day ago then reset it's rank
                            inst.rank=0
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=2) <= now:

                            # it's dead
                            inst.rank=0
                            inst.save()



            if event.get("event_type") == "view-symbol-posts":
                inst = Symbol.objects.all().filter(symbol=event.get("data")['symbol']).first()
                if inst:

                    now = timezone.now()

                    if inst.created_at+timezone.timedelta(days=30) < now and inst.updated_at+timezone.timedelta(hours=1) < now:
                        # if the symbol was created longer than 30 days ago and updated longer than an hour ago then reset it's rank (only the yound and brave survive)
                        inst.rank=0
                        inst.save()
                    else:

                        if inst.updated_at+timezone.timedelta(minutes=10) > now:
                            # if the symbol was updated in the last 10 minutes then increment the rank plus a 100
                            inst.rank+=1
                            # hot af rn
                            inst.save() 

                        elif inst.updated_at+timezone.timedelta(hours=1) > now:
                            # if the Symbol was updated in the last hour then increment the rank
                            inst.rank+=1
                            # picking up steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(hours=4) < now:
                            # if this symbol's rank was updated in the last 4 hours or more
                            # then decrement the rank (because it's falling off)
                            inst.rank-=1
                            # loosing steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=1) < now:
                            # if the hashtag was last updated 1 day ago then reset it's rank
                            inst.rank=0
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=2) <= now:

                            # it's dead
                            inst.rank=0
                            inst.save()

            return Response(status=200)

        return Response(status=400)

    except Exception:
        return Response(status=400)




def getPostEvents():
 
    lte = timezone.datetime.today()
    gte = timezone.datetime(year=lte.year, month=lte.month, day=lte.day-7)


    deleted_posts = Event.objects.all().filter(event_type="delete-post", created_at__lte=lte, created_at__gte=gte).count()
    created_posts = Event.objects.all().filter(event_type="new-post", created_at__lte=lte, created_at__gte=gte).count()
    view_posts = Event.objects.all().filter(event_type="view-post", created_at__lte=lte, created_at__gte=gte).count()

    like_posts = Event.objects.all().filter(event_type="like-post", created_at__lte=lte, created_at__gte=gte).count()

    unlike_posts = Event.objects.all().filter(event_type="unlike-post", created_at__lte=lte, created_at__gte=gte).count()
    dislike_posts = Event.objects.all().filter(event_type="dislike-post", created_at__lte=lte, created_at__gte=gte).count()
    undislike_posts = Event.objects.all().filter(event_type="undislike-post", created_at__lte=lte, created_at__gte=gte).count()



    labels = ["deleted posts", "created posts", "viewed posts", "liked posts", "unliked posts", 'disliked posts', 'undisliked posts']
    values = [deleted_posts, created_posts, view_posts, like_posts, unlike_posts, dislike_posts, undislike_posts]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    fig.update_layout(autosize=True, title={"text": f"Post Events (last 7 days), Total Events: ({deleted_posts+created_posts+view_posts+like_posts+unlike_posts+dislike_posts+undislike_posts})"})

    fig.update_layout(showlegend=True, legend_visible=True, legend_itemsizing="constant", legend_entrywidth=100, legend_borderwidth=1, legend_orientation="h")

    fig.update_layout(title_subtitle_text=f"[{timezone.now().strftime('%d/%m/%y - %H:%M:%S')}]")

    fig.update_layout(paper_bgcolor="rgb(11, 19, 31)")

    fig.update_layout(font_color="white")

    return fig.to_image(format="svg")



  
 

def getViewAccountEvents():
 
    lte = timezone.datetime.today()
    gte = timezone.datetime(year=lte.year, month=lte.month, day=lte.day-7)


    view_acc_posts = Event.objects.all().filter(event_type="view-account-posts", created_at__lte=lte, created_at__gte=gte).count()

    view_acc_liked_posts = Event.objects.all().filter(event_type="view-account-liked-posts", created_at__lte=lte, created_at__gte=gte).count()

    view_account_research = Event.objects.all().filter(event_type="view-account-research", created_at__lte=lte, created_at__gte=gte).count()



    labels = ["view account posts", "view account liked posts", "view account research"]
    values = [view_acc_posts, view_acc_liked_posts, view_account_research]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    fig.update_layout(autosize=True, title={"text": f"View Account Events (last 7 days), Total Events: ({view_acc_posts+view_acc_liked_posts+view_account_research})"})


    fig.update_layout(showlegend=True, legend_visible=True, legend_itemsizing="constant", legend_entrywidth=200, legend_borderwidth=1, legend_orientation="h")

    fig.update_layout(title_subtitle_text=f"[{timezone.now().strftime('%d/%m/%y - %H:%M:%S')}]")

    fig.update_layout(paper_bgcolor="rgb(11, 19, 31)")

    fig.update_layout(font_color="white")


    return fig.to_image(format="svg")



def getViewHashtagSymbolEvents():
 
    lte = timezone.datetime.today()
    gte = timezone.datetime(year=lte.year, month=lte.month, day=lte.day-7)



    view_hashtag_posts = Event.objects.all().filter(event_type="view-hashtag-posts", created_at__lte=lte, created_at__gte=gte).count()

    view_symbol_posts = Event.objects.all().filter(event_type="view-symbol-posts", created_at__lte=lte, created_at__gte=gte).count()



    labels = ["view hashtag posts", "view symbol posts"]
    values = [view_hashtag_posts, view_symbol_posts]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    fig.update_layout(autosize=True, title={"text": f"View Hashtag & Symbol Events (last 7 days), Total Events: ({view_symbol_posts+view_hashtag_posts})"})


    fig.update_layout(showlegend=True, legend_visible=True, legend_itemsizing="constant", legend_entrywidth=200, legend_borderwidth=1, legend_orientation="h")

    fig.update_layout(title_subtitle_text=f"[{timezone.now().strftime('%d/%m/%y - %H:%M:%S')}]")

    fig.update_layout(paper_bgcolor="rgb(11, 19, 31)")

    fig.update_layout(font_color="white")


    return fig.to_image(format="svg")


def getExploreEvents():
 
    lte = timezone.datetime.today()
    gte = timezone.datetime(year=lte.year, month=lte.month, day=lte.day-7)


    explore_search_queries = Event.objects.all().filter(event_type="explore-search-query", created_at__lte=lte, created_at__gte=gte).count()

    explore_category_search_queries = Event.objects.all().filter(event_type="explore-category-search-query", created_at__lte=lte, created_at__gte=gte).count()


    search_query = Event.objects.all().filter(event_type="search-query", created_at__lte=lte, created_at__gte=gte).count()

    labels = ["explore search queries", "explore category search queries", "general search queries"]

    values = [explore_search_queries, explore_category_search_queries, search_query]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    fig.update_layout(autosize=True, title={"text": f"Explore Search Events (last 7 days), Total Events: ({explore_search_queries+explore_category_search_queries+search_query})"})


    fig.update_layout(showlegend=True, legend_visible=True, legend_itemsizing="constant", legend_entrywidth=200, legend_borderwidth=1, legend_orientation="h")

    fig.update_layout(title_subtitle_text=f"[{timezone.now().strftime('%d/%m/%y - %H:%M:%S')}]")

    fig.update_layout(paper_bgcolor="rgb(11, 19, 31)")

    fig.update_layout(font_color="white")


    return fig.to_image(format="svg")



def getResearchEvents():
 
    lte = timezone.datetime.today()
    gte = timezone.datetime(year=lte.year, month=lte.month, day=lte.day-7)


    searched_papers = Event.objects.all().filter(event_type="search-papers", created_at__lte=lte, created_at__gte=gte).count()


    published_papers = Event.objects.all().filter(event_type="publish-research-paper", created_at__lte=lte, created_at__gte=gte).count()


    viewed_myresearch = Event.objects.all().filter(event_type="view-myresearch", created_at__lte=lte, created_at__gte=gte).count()

    deleted_myresearch = Event.objects.all().filter(event_type="delete-research-paper", created_at__lte=lte, created_at__gte=gte).count()

    made_research_imp = Event.objects.all().filter(event_type="make-research-impression", created_at__lte=lte, created_at__gte=gte).count()

    viewed_research = Event.objects.all().filter(event_type="view-research-paper", created_at__lte=lte, created_at__gte=gte).count()

    reported_research = Event.objects.all().filter(event_type="submit-research-report", created_at__lte=lte, created_at__gte=gte).count()


    labels = ["searched papers", "published paper", "viewed their paper", "deleted their paper", "viewed paper", "reported papers"]

    values = [searched_papers, published_papers, viewed_myresearch, deleted_myresearch, made_research_imp, viewed_research, reported_research]

    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    fig.update_layout(autosize=True, title={"text": f"Research Events (last 7 days), Total Events: ({searched_papers+published_papers+viewed_myresearch+viewed_research+deleted_myresearch+made_research_imp+viewed_research+reported_research})"})


    fig.update_layout(showlegend=True, legend_visible=True, legend_itemsizing="constant", legend_entrywidth=200, legend_borderwidth=1, legend_orientation="h")

    fig.update_layout(title_subtitle_text=f"[{timezone.now().strftime('%d/%m/%y - %H:%M:%S')}]")

    fig.update_layout(paper_bgcolor="rgb(11, 19, 31)")

    fig.update_layout(font_color="white")


    return fig.to_image(format="svg")



@api_view(["GET"])
@permission_classes([IsAdminUser])
def eventsOverview(request):

    return Response(data={
        "postEvents": getPostEvents(),
        "ViewAccountEvents": getViewAccountEvents(),
        "viewHashtagSymbolEvents": getViewHashtagSymbolEvents(),
        "exploreEvents": getExploreEvents(),
        "researchEvents": getResearchEvents()
    }, status=200)



