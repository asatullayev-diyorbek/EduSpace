from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField

# Rol tanlovlari
ADMIN, STUDENT = ('admin', 'student')


def validate_video_file(value):
    """
    Video faylini tekshirish uchun validator.
    Faqat .mp4, .mov, webm, .avi va .mkv formatlarini qabul qiladi.
    """
    valid_extensions = ['.mp4', '.mov', 'webm', '.avi', '.mkv']
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(f"Fayl kengaytmasi {', '.join(valid_extensions)} bo'lishi kerak.")


class Category(models.Model):
    """
    Kurs kategoriya modeli.

    Maydonlar:
        name (CharField): Kateqoriya nomi.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class User(AbstractUser):
    """
    Foydalanuvchi profili modeli.

    Maydonlar:
        role (CharField): Foydalanuvchi roli.
        bio (TextField): Foydalanuvchi haqida ma'lumot.
        picture (ImageField): Profil rasmi.
    """
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=STUDENT)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['-pk']
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def get_image(self):
        return self.picture.url if self.picture else None


class Course(models.Model):
    """
    Kurs modeli.

    Maydonlar:
        category (ForeignKey): Kursning kategoriyasi.
        name (CharField): Kurs nomi.
        description (TextField): Kurs tavsifi.
        created_by (ForeignKey): Kurs yaratgan foydalanuvchi.
        is_active (BooleanField): Kursning faol holati.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class Lesson(models.Model):
    """
    Kurs darslari modeli.

    Maydonlar:
        course (ForeignKey): Mavzuning kursi.
        title (CharField): Mavzu nomi.
        content (RichTextField): Mavzu mazmuni.
    """
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"


class Video(models.Model):
    """
    Dars uchun video modeli.

    Maydonlar:
        lesson (ForeignKey): Video dars.
        title (CharField): Video nomi.
        video_file (FileField): Video fayli.
        description (TextField): Video haqida qisqacha ma'lumot.
    """
    lesson = models.ForeignKey(Lesson, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_file])
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Video dars"
        verbose_name_plural = "Video darslar"


class File(models.Model):
    """
    Dars uchun fayl modeli.

    Maydonlar:
        lesson (ForeignKey): Fayl tegishli dars.
        title (CharField): Fayl nomi.
        content (FileField): Fayl mazmuni.
        description (TextField): Fayl haqida ma'lumot.
    """
    lesson = models.ForeignKey(Lesson, related_name='files', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.FileField(upload_to='files/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Dars uchun fayl"
        verbose_name_plural = "Dars uchun fayllar"


class Comment(models.Model):
    """
    Darsga yozilgan izoh modeli.

    Maydonlar:
        lesson (ForeignKey): Izoh tegishli bo'lgan dars.
        user (ForeignKey): Izoh yozgan foydalanuvchi.
        content (TextField): Izoh mazmuni.
    """
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Izoh {self.user.username} tomonidan {self.lesson.title} darsida"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"


class Rating(models.Model):
    """
    Dars bahosi modeli (Yoqdi yoki yoqmadi).

    Maydonlar:
        lesson (ForeignKey): Baholangan dars.
        user (ForeignKey): Baholovchi foydalanuvchi.
        liked (BooleanField): Yoqdi yoki yoqmadi belgisi.
    """
    lesson = models.ForeignKey(Lesson, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField()

    def __str__(self):
        return f"Baholash {self.user.username} tomonidan - {'Yoqdi' if self.liked else 'Yoqmadi'}"

    class Meta:
        ordering = ['-id']
        verbose_name = "Baholash"
        verbose_name_plural = "Baholashlar"


class Update(models.Model):
    """
    Yangilanish modeli.

    Maydonlar:
        title (CharField): Yangilanish sarlavhasi.
        content (TextField): Yangilanish mazmuni.
        created_at (DateTimeField): Yangilanish sanasi.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
