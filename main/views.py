from django.core.mail import send_mail
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from .permissions import IsAuthor, IsStudent, IsAdmin
from .serializers import CategorySerializer, CourseSerializer, \
    LessonSerializer, VideoSerializer, FileSerializer, \
    CommentSerializer, RatingSerializer, UpdateSerializer
from .models import Category, Course, Lesson, \
    Video, File, Comment, Rating, User


class CategoryView(ModelViewSet):
    """
    Kategoriya bilan ishlash uchun ViewSet.
    - `GET /api/categories/`: Barcha kategoriyalarni olish.
    - `POST /api/categories/`: Yangi kategoriya yaratish.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthor]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']  # Kategoriyalarning nomi bo'yicha qidirish


class CourseView(ModelViewSet):
    """
    Kurs bilan ishlash uchun ViewSet.
    - `GET /api/courses/`: Barcha kurslarni olish.
    - `POST /api/courses/`: Yangi kurs yaratish.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthor]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name', 'description', 'is_active']  # Kurs nomi va tavsifi bo'yicha qidirish


class LessonView(ModelViewSet):
    """
    Dars bilan ishlash uchun ViewSet.
    - `GET /api/lessons/`: Barcha darslarni olish.
    - `POST /api/lessons/`: Yangi dars yaratish.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthor]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'content']  # Dars nomi va tavsifi bo'yicha qidirish

    def get_queryset(self):
        """Kurs bo'yicha ajratish"""
        course_id = self.request.query_params.get('course_id', None)
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()


class VideoView(ModelViewSet):
    """
    Video bilan ishlash uchun ViewSet.
    - `GET /api/lessons/{lesson_pk}/videos/`: Berilgan darsga tegishli videolarni olish.
    - `POST /api/lessons/{lesson_pk}/videos/`: Yangi video qo'shish.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthor]
    lookup_field = 'pk'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title']  # Video nomi bo'yicha qidirish

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_pk']
        return Video.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_pk']
        lesson = Lesson.objects.get(pk=lesson_id)
        serializer.save(lesson=lesson)


class FileView(ModelViewSet):
    """
    Fayl bilan ishlash uchun ViewSet.
    - `GET /api/lessons/{lesson_pk}/files/`: Berilgan darsga tegishli fayllarni olish.
    - `POST /api/lessons/{lesson_pk}/files/`: Yangi fayl qo'shish.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthor]
    lookup_field = 'pk'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']  # Fayl nomi bo'yicha qidirish

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_pk']
        return File.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_pk']
        lesson = Lesson.objects.get(pk=lesson_id)
        serializer.save(lesson=lesson)


class CommentView(ViewSet):
    """
    Kommentlar bilan ishlash uchun ViewSet.
    - `GET /api/lessons/{lesson_pk}/comments/`: Berilgan darsga tegishli kommentlarni olish.
    - `POST /api/lessons/{lesson_pk}/comments/`: Yangi komment qo'shish.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, lesson_pk=None, *args, **kwargs):
        comments = Comment.objects.filter(lesson_id=lesson_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request, lesson_pk=None, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            lesson = Lesson.objects.get(pk=lesson_pk)  # Darsni toping
            serializer.save(user=request.user, lesson=lesson)  # Yangi kommentni saqlang
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RatingView(ViewSet):
    """
    Baholar bilan ishlash uchun ViewSet.
    - `GET /api/lessons/{lesson_pk}/ratings/`: Berilgan darsga tegishli baholarni olish.
    - `POST /api/lessons/{lesson_pk}/ratings/`: Yangi baho qo'shish yoki mavjud bahoni yangilash.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsStudent]

    def list(self, request, lesson_pk=None, *args, **kwargs):
        ratings = Rating.objects.filter(lesson_id=lesson_pk)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def create(self, request, lesson_pk=None, *args, **kwargs):
        existing_rating = Rating.objects.filter(lesson_id=lesson_pk, user=request.user).first()

        if existing_rating:
            # Mavjud bahoni yangilash
            serializer = RatingSerializer(existing_rating, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        else:
            # Yangi baho yaratish
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                lesson = Lesson.objects.get(pk=lesson_pk)
                serializer.save(user=request.user, lesson=lesson)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class UpdateViewSet(APIView):
    """Foydalanuvchilarga email xabar yuborish"""
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        if self.kwargs.get('version') == 'v1':
            """1-versiya uchun cheklov"""
            return Response({'message': "API 1-versiyada ushbu amalni bajarib bo'lmaydi. Keyingi versiyalardan foydalanib ko'ring"}, status=400)

        serializer = UpdateSerializer(data=self.request.data)

        if serializer.is_valid():
            update = serializer.save()
            users = User.objects.all()
            for user in users:
                try:
                    send_mail(
                        subject=f"Yangilanish: {update.title}",
                        message=update.content,
                        from_email="EduSpacePlatformasi@yandex.ru",
                        recipient_list=[user.email],
                    )
                except:
                    pass
            return Response({'message': "Yuborildi"}, status=201)
        return Response(serializer.errors, status=400)
