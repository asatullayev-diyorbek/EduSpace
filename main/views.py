from rest_framework.viewsets import ModelViewSet

from .permissions import IsStaff
from .serializers import CategorySerializer
from .models import Category


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaff]

