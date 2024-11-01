from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import User
from .permissions import IsMyProfile
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class UserProfileView(RetrieveUpdateAPIView):
    """
    Foydalanuvchi profilini ko'rish va yangilash API ko'rinishi.

    URL: /api/user/<int:pk>/
    Metodlar: GET, PUT, PATCH
    Ruxsat berish: IsAuthor
    """

    queryset = User.objects.all()
    permission_classes = (IsMyProfile,)
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        """
        Foydalanuvchi ma'lumotlarini olish.

        Parametrlar:
            - request: HTTP so'rov
            - pk: Foydalanuvchi identifikatori

        Qaytaruvchi:
            Foydalanuvchi ma'lumotlari (JSON formatida).
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Foydalanuvchi ma'lumotlarini yangilash.

        Parametrlar:
            - request: HTTP so'rov
            - pk: Foydalanuvchi identifikatori

        Qaytaruvchi:
            Yangilangan foydalanuvchi ma'lumotlari (JSON formatida).
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Foydalanuvchi ma'lumotlarini qisman yangilash.

        Parametrlar:
            - request: HTTP so'rov
            - pk: Foydalanuvchi identifikatori

        Qaytaruvchi:
            Yangilangan foydalanuvchi ma'lumotlari (JSON formatida).
        """
        return super().patch(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    """
    Foydalanuvchini tizimga kiritish API ko'rinishi.

    URL: /api/login/
    Metod: POST
    Ruxsat berish: AllowAny
    """

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    """
    Foydalanuvchini ro'yxatdan o'tkazish API ko'rinishi.

    URL: /api/register/
    Metod: POST
    Ruxsat berish: AllowAny
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    Foydalanuvchini tizimdan chiqarish API ko'rinishi.

    URL: /api/logout/
    Metod: POST
    Ruxsat berish: IsAuthenticated
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Foydalanuvchini tizimdan chiqarish.

        Parametrlar:
            - request: HTTP so'rov

        Qaytaruvchi:
            - 205: Muvaffaqiyatli chiqish.
            - 400: Xato, agar refresh token noto'g'ri bo'lsa.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "You are logged out"}, status=205)
        except Exception as e:
            return Response({"message": str(e)}, status=400)
