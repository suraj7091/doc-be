from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from .utils import IsAuthenticatedExtendedAdmin

from .models import UserProfile
from .serializers import UserProfileSerializer


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as err:
            return Response({"detail": "invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        login(request, user)
        login_data = super(LoginAPI, self).post(request, format=None)
        return Response({"detail": "login successful", "data": login_data.data}, status=HTTP_400_BAD_REQUEST)


class UserRoles(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({"detail": "fetch successful",
                         "data": {"username": user.username, "groups": user.groups.values_list('name', flat=True)}},
                        status=HTTP_200_OK)


@api_view(('GET', 'PUT', 'DELETE'))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedExtendedAdmin])
def user_detail(request, pk):
    try:
        current_user_profile = UserProfile.objects.get(user_id=request.user.id)
        user_profile = UserProfile.objects.filter(user_id=pk, organization_id=current_user_profile.organization_id). \
            select_related('user').first()
        if not user_profile:
            return Response({"detail": "User not found", "data": {}}, status=HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({"detail": "User not found", "data": {}}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response({"detail": "Fetch successful", "data": serializer.data}, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
