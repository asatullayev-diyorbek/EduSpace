from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from main.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer klassi.

    Bu serializer `User` modelining ma'lumotlarini JSON formatida qaytaradi.

    Meta:
        model (User): Foydalanuvchi modelini belgilaydi.
        fields (tuple): Serializerda ko'rsatiladigan maydonlarni belgilaydi.
        extra_kwargs (dict): Qo'shimcha sozlamalar, faqat o'qish uchun bo'lgan `id` maydonini o'z ichiga oladi.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'picture')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    MyTokenObtainPairSerializer klassi.

    JWT (JSON Web Token) olish uchun serializer. `username` qo'shimcha ma'lumot sifatida
    token ichiga qo'shiladi.

    Usullar:
        get_token(cls, user): `TokenObtainPairSerializer` sinfidagi `get_token` metodini qayta aniqlaydi va
        foydalanuvchi nomini token ichiga qo'shadi.
    """

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Tokenga foydalanuvchi nomini qo'shish
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    RegisterSerializer klassi.

    Foydalanuvchini ro'yxatdan o'tkazish uchun serializer. Email yagona qiymat
    bo'lishi kerak va parolni tasdiqlash uchun `password2` maydonidan foydalanadi.

    Maydonlar:
        email (EmailField): Yagona email manzil bo'lishi kerak.
        password (CharField): Yozib olish uchun (write-only), majburiy va parol validatsiyasi bilan.
        password2 (CharField): Parolni tasdiqlash maydoni.

    Meta:
        model (User): `User` modelini belgilaydi.
        fields (tuple): Serializerda ko'rsatiladigan maydonlarni belgilaydi.
        extra_kwargs (dict): `first_name` va `last_name` maydonlarini majburiy qilib belgilaydi.

    Usullar:
        validate(self, attrs): Parol va tasdiq paroli mos kelishini tekshiradi.
        create(self, validated_data): Tasdiqlangan ma'lumotlar asosida foydalanuvchini yaratadi va
        parolni xavfsiz shaklda saqlaydi.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        """
        Parol maydonlari mosligini tekshiradi.

        Parametrlar:
            attrs (dict): Tasdiqlanadigan maydonlar.

        Qaytadi:
            dict: Tasdiqlangan maydonlar.

        Xato:
            serializers.ValidationError: Agar parollar mos kelmasa, xato qaytaradi.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Foydalanuvchini yaratadi va parolini saqlaydi.

        Parametrlar:
            validated_data (dict): Tasdiqlangan ma'lumotlar.

        Qaytadi:
            User: Yangi yaratilgan foydalanuvchi obyekti.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Parolni xavfsiz shaklda saqlash
        user.set_password(validated_data['password'])
        user.save()

        return user
