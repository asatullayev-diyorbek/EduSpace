from rest_framework.permissions import BasePermission


class IsMyProfile(BasePermission):
    """
    IsMyProfile ruxsat beruvchi klassi.

    Bu klass foydalanuvchining o'z profil sahifasiga kirishini cheklaydi.
    Agar foydalanuvchi autentifikatsiyadan o'tmagan bo'lsa yoki boshqa
    foydalanuvchining profil sahifasiga kirishga harakat qilsa, kirish rad etiladi.

    Xususiyatlar:
        message (str): Foydalanuvchi kirishni rad etilganda ko'rsatiladigan xabar.

    Usullar:
        has_object_permission(self, request, view, obj):
            Foydalanuvchining o'z profil sahifasiga kirishga ruxsat bor-yo'qligini tekshiradi.
            Agar autentifikatsiya o'tgan bo'lsa va foydalanuvchi IDsi (obj.pk)
            so'rov yuborgan foydalanuvchining IDsi (request.user.pk) bilan mos kelsa, ruxsat beradi.
            Aks holda, rad etadi.

    Foydalanish:
        Ushbu klass `IsMyProfile` sifatida permission (ruxsat) sifatida qo'shiladi va
        profilga faqat so'rovni amalga oshirgan foydalanuvchining o'ziga ruxsat beradi.
    """
    message = "Bu sahifaga kirolmaysiz."

    def has_object_permission(self, request, view, obj):
        # Foydalanuvchi autentifikatsiyadan o'tmagan bo'lsa, rad etiladi
        if not request.user.is_authenticated:
            return False
        # Foydalanuvchi IDsi bilan obyektning IDsi mos kelsa, ruxsat beriladi
        return obj.pk == request.user.pk
