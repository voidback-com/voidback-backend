from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from transformers import pipeline




@api_view(["POST"])
@permission_classes([AllowAny])
def textNSFW(request: Request):
    try:
        model = pipeline("text-classification", "models/NSFW_text_classifier", device="cpu")

        text = request.data.get("text")


        if not text:
            return Response(status=400)

        data = model(text)

        return Response(data=data, status=200)

    except KeyboardInterrupt:
        return Response(status=400)

