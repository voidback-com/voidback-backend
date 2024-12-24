from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from transformers import pipeline




@api_view(["POST"])
@permission_classes([AllowAny])
def textNSFW(request: Request):
    try:
        model = pipeline("text-classification", "models/distilbert-nsfw-text-classifier", device="cpu")

        text = request.data.get("text")


        if not text:
            return Response(status=400)

        data = model(text)

        return Response(data=data[0], status=200)

    except Exception:
        return Response(status=400)




@api_view(["POST"])
@permission_classes([AllowAny])
def imageNSFW(request: Request):
    try:
        img = request.FILES.get('image', None)

        if not img:
            return None


        if img.size > 5e+6:
            return Response(status=400)

        img = Image.open(img)

        model = pipeline("image-classification", "models/vit-base-nsfw-detector", device="cpu")

        data = model(img)
        data = data[0]

        if data['label']=="sfw":
            return Response(data={"label": "SFW"}, status=200)

        return Response(data={"label": "NSFW"}, status=200)

    except Exception:
        return Response(status=400)



