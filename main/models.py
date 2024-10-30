from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField


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
    Kateqoriya modeli.

    Maydonlar:
        name (CharField): Kateqoriya nomi.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


# 1. Foydalanuvchi profili
class UserProfile(models.Model):
    """
    Foydalanuvchi profili modeli.

    Maydonlar:
        user (ForeignKey): Foydalanuvchi profili bilan bog'langan asosiy foydalanuvchi.
        bio (TextField): Foydalanuvchi haqida qisqacha ma'lumot.
        profile_picture (ImageField): Profil rasmi.

    Meta:
        ordering: Eng so'nggi qo'shilgan foydalanuvchilar birinchi o'rinda bo'ladi.
        verbose_name: Model uchun birlik nomi "Foydalanuvchi profili".
        verbose_name_plural: Model uchun ko'plik nomi "Foydalanuvchilar profillari".
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-user__date_joined']
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchilar profillari"


# 2. Kurslar
class Course(models.Model):
    """
    Platformadagi kurslarni ifodalovchi model.

    Maydonlar:
        name (CharField): Kurs nomi.
        description (TextField): Kursning batafsil tavsifi.
        created_by (ForeignKey): Kurs yaratgan foydalanuvchi.
        created_at (DateTimeField): Kurs yaratilgan vaqt.
        updated_at (DateTimeField): Kurs oxirgi yangilangan vaqt.
        is_active (BooleanField): Kurs faol yoki yo‘qligini ko‘rsatuvchi belgi.

    Meta:
        ordering: Eng so'nggi kurslar birinchi o‘rinda ko‘rsatiladi.
        verbose_name: Model uchun birlik nomi "Kurs".
        verbose_name_plural: Model uchun ko'plik nomi "Kurslar".
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


# 3. Mavzular (Darslar) kurs uchun
class Lesson(models.Model):
    """
    Kursdagi mavzu yoki dars modeli.

    Maydonlar:
        course (ForeignKey): Mavzu tegishli bo'lgan kurs.
        title (CharField): Mavzu yoki dars nomi.
        content (TextField): Mavzu yoki dars mazmuni.
        created_at (DateTimeField): Mavzu yaratilgan vaqt.
        updated_at (DateTimeField): Mavzu oxirgi yangilangan vaqt.

    Meta:
        ordering: Eng yangi mavzular birinchi ko‘rsatiladi.
        verbose_name: Model uchun birlik nomi "Mavzu".
        verbose_name_plural: Model uchun ko'plik nomi "Mavzular".
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


# 4. Video darslar
class Video(models.Model):
    """
    Darsdagi video material modeli.

    Maydonlar:
        lesson (ForeignKey): Video tegishli bo'lgan dars.
        title (CharField): Video nomi.
        video_file (FileField): Video fayl.
        description (TextField): Video haqida qisqacha ma'lumot.
        uploaded_at (DateTimeField): Video yuklangan vaqt.

    Meta:
        ordering: Eng yangi yuklangan videolar birinchi ko'rsatiladi.
        verbose_name: Model uchun birlik nomi "Video dars".
        verbose_name_plural: Model uchun ko'plik nomi "Video darslar".
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
    Darsdagi fayl material modeli.

    Maydonlar:
        lesson (ForeignKey): Video tegishli bo'lgan dars.
        title (CharField): Fayl nomi.
        content (FileField): Fayl.
        description (TextField): Fayl haqida qisqacha ma'lumot.
        uploaded_at (DateTimeField): Fayl yuklangan vaqt.

    Meta:
        ordering: Eng yangi yuklangan fayllar birinchi ko'rsatiladi.
        verbose_name: Model uchun birlik nomi "Dars uchun fayl".
        verbose_name_plural: Model uchun ko'plik nomi "Dars uchun fayllar".
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


# 5. Izohlar
class Comment(models.Model):
    """
    Darsga yozilgan izoh modeli.

    Maydonlar:
        lesson (ForeignKey): Izoh tegishli bo'lgan dars.
        user (ForeignKey): Izoh yozgan foydalanuvchi.
        content (TextField): Izoh matni.
        created_at (DateTimeField): Izoh yaratilgan vaqt.

    Meta:
        ordering: Eng yangi izohlar birinchi ko'rsatiladi.
        verbose_name: Model uchun birlik nomi "Izoh".
        verbose_name_plural: Model uchun ko'plik nomi "Izohlar".
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


# 6. Baholash (Yoqdi/Yoqmadi)
class Rating(models.Model):
    """
    Darsni baholash modeli (Yoqdi yoki Yoqmadi).

    Maydonlar:
        lesson (ForeignKey): Baholangan dars.
        user (ForeignKey): Baholovchi foydalanuvchi.
        liked (BooleanField): Yoqdi yoki yoqmadi belgisi.

    Meta:
        ordering: Eng yangi baholar birinchi ko'rsatiladi.
        verbose_name: Model uchun birlik nomi "Baholash".
        verbose_name_plural: Model uchun ko'plik nomi "Baholashlar".
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
