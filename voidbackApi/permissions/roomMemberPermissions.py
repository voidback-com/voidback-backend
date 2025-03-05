from rest_framework import permissions
from rest_framework.request import Request
from ..models.EdgeRoom import EdgeRoom, RoomMembership




class IsRoomMember(permissions.BasePermission):

    edit_methods = ("POST", "GET", "PATCH", "DELETE", "OPTIONS")


    def has_permission(self, request: Request, view):
        if request.user.is_authenticated:
            room = request.query_params.get("room")
            member = RoomMembership.objects.all().filter(account=request.user, room__name=room).first()

            if member:
                return True

            else:
                instance = EdgeRoom.objects.all().filter(config__admin__username=request.user.username).first()

                if instance:
                    return True

            return False

        return False



# for actions such as: posting image, deleting posts
class IsRoomModerator(permissions.BasePermission):

    edit_methods = ("POST", "GET", "PATCH", "DELETE", "OPTIONS")


    def has_permission(self, request: Request, view):
        if request.user.is_authenticated:
            room = request.query_params.get("room")
            member = RoomMembership.objects.all().filter(account=request.user, room__name=room).first()
            # check if the user's membership config is moderator true

            if member:
                return True

            return False

        return False


