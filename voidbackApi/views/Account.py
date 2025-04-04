from random import randint
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.Account import AccountSerializer, PublicAccountSerializer, FollowSerializer, AccountActiveStatusSerializer
from ..models.Account import Account, AccountActiveStatus, OneTimePassword, Follow
import json
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token




class SignupView(CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]



class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=401)




class LogoutView(APIView):
    def get(self, request: Request, format=None):
        request.user.auth_token.delete()
        return Response(status=200)



# return authenticated user's account
class AccountView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        try:
            serializer = AccountSerializer(request.user)
            return Response(serializer.data, status=200)
        except Exception:
            return Response(status=400)



    def delete(self, request: Request):
        try:
            otp = request.data.get("otp")

            time_now = timezone.now()

            instance = OneTimePassword.objects.all().filter(account=request.user.username).last()


            if instance and instance.expires_at > time_now:
                if instance.otp == otp:
                    instance.verified = True
                    instance.save()

                    inst = Account.objects.all().filter(pk=request.user.id).first()
                    if inst.avatar:
                        inst.avatar.delete(save=False)
                    inst.delete()

                    return Response(status=200)

            return Response(status=404)

        except Exception:
            return Response(status=400)



    def patch(self, request: Request):
        try:
            data = request.data.get("data", None)

            if data:
                data = json.loads(data)
            
            else:
                data = dict()
                data['avatar'] = request.FILES.get("avatar", None)

            instance = Account.objects.all().filter(pk=request.user.id).first()


            serializer = AccountSerializer(data=data, instance=instance, partial=True)

            if serializer.is_valid():
                serializer.update(instance, data)
                return Response(data=serializer.data, status=200)

            return Response(data=serializer.errors, status=400)

        except Exception:
            return Response(status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_otp(request: Request):
    try:

        last_otp = OneTimePassword.objects.all().filter(account=request.user).last()

        time_now = timezone.now()


        if last_otp and last_otp.expires_at >= time_now:
            return Response(data={"error": "Can't request a new otp until the previous one expires.  (otp lifetime is 10 minutes)"}, status=400)


        expires_at = timezone.now() + timezone.timedelta(minutes=10)

        instance = OneTimePassword(account=request.user, expires_at=expires_at, otp=str(randint(1000, 1000000)))

        instance.save()

        html_template = get_template("email/otp.html")

        msg = EmailMultiAlternatives("Voidback OTP", "", "noreply@voidback.com", to=[request.user.email])

        msg.attach_alternative(html_template.render({
            "full_name": request.user.full_name,
            "otp": instance.otp
        }), "text/html")

        msg.send()


        return Response(data={"error": None}, status=200)

    except Exception:
        return Response(data={"error": "Error sending a One Time Password."}, status=400)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_otp(request: Request):
    try:
        otp = request.data.get("otp")

        time_now = timezone.now()

        instance = OneTimePassword.objects.all().filter(account=request.user.username).last()


        if instance and instance.expires_at > time_now:
            if instance.otp == otp:
                instance.verified = True
                if not instance.account.email_verified:
                    instance.account.email_verified = True
                    instance.account.save()
                instance.save()

                return Response(data={"message": "Successful OTP verification."}, status=200)
            else:
                return Response(data={"error": "Wrong otp, please try again."}, status=400)
        else:
            return Response(data={"error": "The OTP is expired please try again."}, status=400)


    except Exception:
        return Response(data={"error": "Error verifying otp."}, status=400)







@api_view(['GET'])
@permission_classes([AllowAny])
def searchAccounts(request: Request):
    try:

        byUsername = request.GET.get("username", None)
        byName = request.GET.get("full_name", None)
        byEmail = request.GET.get("email", None)
        byBio = request.GET.get("bio", None)

        topResults = ...

        if byUsername:
            topResults = Account.objects.all().filter(username__contains=byUsername)[:10]

        elif byName:
            topResults = Account.objects.all().filter(full_name__contains=byName)[:10]


        elif byEmail:
            topResults = Account.objects.all().filter(email__contains=byEmail)[:10]


        elif byBio:
            topResults = Account.objects.all().filter(bio__contains=byBio)[:10]

        else:
            return Response(data=[], status=200)

        serializer = PublicAccountSerializer(topResults, many=True)

        return Response(data=serializer.data, status=200)

    except Exception:
        return Response(data=[], status=200)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def followAccount(request: Request):
    try:
        username = request.query_params.get("username", None)

        if username:
            user_instance = Account.objects.all().filter(username=username).first()

            if user_instance:
                dat = {
                    "follower": request.user,
                    "following": user_instance,
                    "hash": f"{request.user.username}:{username}"
                }

                user_instance.rank+=1
                if user_instance.rank > 100000:
                    user_instance.isVerified = True
                user_instance.save()

                serializer = FollowSerializer(data=dat)

                if serializer.is_valid():
                    serializer.create(dat)

                    return Response(data=serializer.data, status=200)

                return Response(data=serializer.errors, status=400)

            return Response(data={"error": f'"@{username}" does not exists.'}, status=400)

        return Response(data={"error": 'no username provided!'}, status=400)

    except Exception:
        return Response(data={"error": f'Error following user, please try again.'}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unfollowAccount(request: Request):
    try:
        username = request.query_params.get("username", None)

        if username:
            user_instance = Follow.objects.all().filter(follower=request.user.username, following=username).first()


            if user_instance:
                user_instance.following.rank-=1
                user_instance.following.save()
                user_instance.delete()


                return Response(data={"message": f'Unfollowed "@{username}".'}, status=200)

            return Response(data={"error": f'"@{username}" does not exists.'}, status=400)
        return Response(data={"error": "No username provided."}, status=400)
    except Exception:
        return Response(data={"error": f'Error following user, please try again.'}, status=400)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def isAccountFollowed(request: Request):
    try:
        username = request.query_params.get("username", None)

        if username:
            user_instance = Follow.objects.all().filter(follower=request.user.username, following=username).first()

            if user_instance:
                s = FollowSerializer(user_instance)
                return Response(data=s.data, status=200)

            return Response(data={"error": "404"}, status=404)

    except Exception:
            return Response(data={"error": "404"}, status=400)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def isFollowingBack(request: Request):
    try:
        username = request.query_params.get("username", None)

        if username:
            user_instance = Follow.objects.all().filter(follower=username, following=request.user.username).first()

            if user_instance:
                s = FollowSerializer(user_instance)
                return Response(data=s.data, status=200)

            return Response(data={"error": "404"}, status=404)
    except Exception:
        return Response(status=400)





# get all the accounts this username follows
@api_view(["GET"])
@permission_classes([AllowAny])
def getUsernameFollowing(request: Request, username: str):
    try:
        skip = request.query_params.get("skip", 0)
        limit = request.query_params.get("limit", 10)

        if len(username):
            user_instance = Follow.objects.all().filter(follower=username).order_by("-created_at")[int(skip):int(limit)]

            if user_instance:
                s = FollowSerializer(user_instance, many=True)
                return Response(data=s.data, status=200)

            return Response(data=[], status=200)
        return Response(data=[], status=200)
    except Exception:
        return Response(data={"error": "failed to fetch following."}, status=400)



# get all the accounts that follow this username
@api_view(["GET"])
@permission_classes([AllowAny])
def getUsernameFollowers(request: Request, username: str):
    try:
        skip = request.query_params.get("skip", 0)
        limit = request.query_params.get("limit", 10)

        if len(username):
            user_instance = Follow.objects.all().filter(following=username).order_by("-created_at")[int(skip):int(limit)]

            if user_instance:
                s = FollowSerializer(user_instance, many=True)
                return Response(data=s.data, status=200)

            return Response(data=[], status=200)

        return Response(data=[], status=200)
    except Exception:
        return Response(data={"error": "failed to fetch followers."}, status=400)
        


@api_view(["GET"])
@permission_classes([AllowAny])
def getFriends(request: Request, username: str):
    try:
        following = Follow.objects.all().filter(follower=username).values_list("following__username")

        friends = Follow.objects.all().filter(following__username=username, follower__username__in=following).values("follower__username").order_by('-created_at')

        accounts = []

        for friend in friends:
            accounts.append(Account.objects.all().filter(username=friend['follower__username']).first())


        if len(accounts):
            s = PublicAccountSerializer(accounts, many=True)
            return Response(data=s.data, status=200)

        return Response(data=[], status=200)

    except KeyboardInterrupt:
        return Response(data={"error": "failed to fetch friends."}, status=400)

     

# get account by username
@api_view(["GET"])
@permission_classes([AllowAny])
def getAccountByUsername(request: Request, username: str):
    try:
        user_instance = Account.objects.all().filter(username=username).first()

        if user_instance:
            s = PublicAccountSerializer(user_instance)
            return Response(data=s.data, status=200)

        return Response(data={"error": "Account not found."}, status=404)

    except Exception:
        return Response(data={"error": "failed to fetch account."}, status=400)
        




# get all the accounts that this username follows
@api_view(["GET"])
@permission_classes([AllowAny])
def getUsernameFollowingCount(request: Request, username: str):
    try:

        if username:
            user_instance = Follow.objects.all().filter(follower=username).count()

            if user_instance:
                return Response(data={"following": user_instance}, status=200)

            return Response(data={"following": 0}, status=200)
        return Response(data={"following": 0}, status=200)

    except Exception:
        return Response(data={"error": "failed to fetch followers."}, status=400)
 



# get mutual friends between user and this username
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAccountMutuals(request: Request, username: str):
    try:

        if username:
            # all the people i follow
            myFollowing = Follow.objects.all().filter(follower=request.user.username).values("following")

            # all the people that follow this username that also follow me
            mutuals = Follow.objects.all().filter(following=username, follower__in=myFollowing)

            usernames = []

            for i in mutuals:
                usernames.append(i.follower)



            serialized = PublicAccountSerializer(usernames, many=True)

            return Response(data=serialized.data, status=200)

        return Response(data=[], status=200)

    except Exception:
        return Response(data={"error": "failed to fetch mutuals."}, status=400)
 





# get recommended accounts
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAccountRecommendations(request: Request):
    try:

        # 100 accounts max; that i follow
        instance = Follow.objects.all().filter(follower=request.user.username).order_by("created_at").distinct()[0:100]

        if instance:
            recommended = []

            for i in instance:
                # last account followed by top 100 accounts i follow is added to recommended
                last_followed = Follow.objects.all().filter(follower=i.following.username).last()

                if last_followed:
                    followed = Follow.objects.all().filter(follower=request.user.username, following=last_followed.following.username).first()


                    if not followed and last_followed.following.username != request.user.username and last_followed.following not in recommended:
                        recommended.append(last_followed.following)


            serializer = PublicAccountSerializer(recommended, many=True)

            return Response(data=serializer.data, status=200)


        else:
            top100 = Account.objects.all().order_by("-rank")[0:100]

            recommended = []

            for i in top100:
                if i == request.user:
                    continue

                else:
                    isfollowed = Follow.objects.all().filter(follower=request.user.username, following=i.username).first()
                    if not isfollowed:
                        recommended.append(i)


            serializer = PublicAccountSerializer(recommended, many=True)

            return Response(data=serializer.data, status=200)


    except Exception:
        return Response(data={"error": "failed to fetch recommendations."}, status=400)
 




@api_view(['POST'])
@permission_classes([AllowAny])
def resetPassword(request):
    try:
        otp = request.data.get("otp")
        password = request.data.get("password")
        email = request.data.get("email")

        account = Account.objects.all().filter(email=email).first()

        if not account:
            return Response(data={"error": "Error verifying the One Time Password, the specified email is not known to us."}, status=400)

        time_now = timezone.now()

        instance = OneTimePassword.objects.all().filter(account=account).last()


        if instance and instance.expires_at > time_now:
            if instance.otp == otp and instance.account == account:
                instance.verified = True
                instance.save()

                account.set_password(password)
                account.save()

                return Response({"error": None}, status=200)

        return Response({"error": "Error the otp is either expired or invalid."}, status=400)

    except Exception:
        return Response({"error": "Error the otp is either expired or invalid."}, status=400)




@api_view(['GET'])
@permission_classes([AllowAny])
def send_AnonymousOtp(request: Request):
    try:

        email = request.query_params.get("email")

        account = Account.objects.all().filter(email=email).first()

        if not account:
            return Response(data={"error": "Error sending a One Time Password, the specified email is not known to us."}, status=400)


        last_otp = OneTimePassword.objects.all().filter(account=account).last()

        time_now = timezone.now()

        if last_otp and last_otp.expires_at > time_now:
            return Response(data={"error": "Can't request a new otp until the previous one expires. (otp lifetime is 10 minutes)"}, status=400)


        expires_at = timezone.now() + timezone.timedelta(minutes=10)

        instance = OneTimePassword(account=account, expires_at=expires_at, otp=str(randint(1000, 1000000)))

        instance.save()

        html_template = get_template("email/otp.html")

        msg = EmailMultiAlternatives("Voidback OTP", "", "noreply@voidback.com", to=[account.email])

        msg.attach_alternative(html_template.render({
            "full_name": account.full_name,
            "otp": instance.otp
        }), "text/html")

        msg.send()


        return Response(data={"error": None}, status=200)

    except Exception:
        return Response(data={"error": "Error sending a One Time Password."}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAccountStatus(request):
    try:
        acc = request.query_params.get("account")
        instance = AccountActiveStatus.objects.all().filter(account__username=acc).first()

        if instance:
            serialized = AccountActiveStatusSerializer(instance)
            return Response(data=serialized.data, status=200)

        print("no instance")
        return Response(data={"error": "Error couldn't retrieve the user's active status, none found."}, status=400)
    except KeyboardInterrupt:
        return Response(data={"error": "Error couldn't retrieve the user's active status."}, status=400)
        

