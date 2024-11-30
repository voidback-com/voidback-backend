import json
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import resolve






@api_view(["POST"])
@permission_classes([AllowAny])
def gfetch(request: Request):
    try:


        requests = request.data.get("requests")

        responses = dict()
        

        if not requests:
                return Response(status=400)

        for req in requests:


            r = request._request
            r.method = req['method']
            r.path = req['endpoint']


            if 'headers' in req:
                r.META.update(req['headers'])

                if 'Authorization' in req['headers']:
                    r.META.update({"HTTP_AUTHORIZATION": req['headers']['Authorization']})


            if 'body' in req:
                r._body = json.dumps(req['body']).encode("utf-8")

            if 'files' in req:
                r.FILES = req['files']



            resolved = resolve(req['endpoint'])

            res = resolved.func(r, **resolved.kwargs)


            responses.update({req['endpoint']: res.data})


        return Response(data=responses, status=200)

    except Exception:
        return Response(status=400)

