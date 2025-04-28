from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserCreateSerializer,
    PasswordUpdateSerializer,
    LoginSerializer,
)
from base.utils import set_jwt_cookies


User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        return set_jwt_cookies(response, user)


class UpdatePasswordView(CreateAPIView):
    serializer_class = PasswordUpdateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.request.user
        response = set_jwt_cookies(response, user)
        response.data = {"message": "The password is updated"}
        return response


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        password = request.data.get("password")
        username = request.data.get("username")
        user = authenticate(request, username=username, password=password)
        if user:
            response = Response(
                status=status.HTTP_200_OK, data={"message": "Logged in successfully"}
            )
            return set_jwt_cookies(response, user)
        return Response(
            status=status.HTTP_401_UNAUTHORIZED, data={"message": "Invalid credentials"}
        )


class LogoutUserAPIView(APIView):
    """
    View for logging out the currently authenticated user.

    This view logs out the user and deletes the JWT access and refresh tokens
    from the cookies.

    Example of request:
    {
        No request body required
    }

    Permissions:
        - No special permissions required, but the user must be authenticated.

    Response on success:
    - Status: 200 OK
    - Cookies: JWT access and refresh tokens are deleted

    Note:
    - If no user is authenticated, the view still returns a 200 OK status,
    but no actions are performed.
    """

    def post(self, request):
        if request.user:
            logout(request)

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
