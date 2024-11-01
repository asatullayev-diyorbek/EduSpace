from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Category, Course, Lesson, Rating, Video, Comment, File, Update


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Ko'rishda category ma'lumotlarini chiqarish uchun CategorySerializer ishlatiladi
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def to_representation(self, instance):
        """Ko'rishda category va created_by ma'lumotlarini serializer orqali chiqaramiz."""
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        return representation

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return Course.objects.create(**validated_data)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'description', 'uploaded_at', 'lesson_id']
        read_only_fields = ['uploaded_at', 'lesson_id']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'title', 'content', 'description', 'uploaded_at', 'lesson_id']
        read_only_fields = ['uploaded_at', 'lesson_id']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'liked']


class LessonSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'title', 'content', 'created_at', 'updated_at',
            'videos', 'files', 'comments', 'ratings'
        ]


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ['id', 'title', 'content', 'created_at']
