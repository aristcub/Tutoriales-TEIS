from rest_framework import generics
from .serializers import ToDoSerializer
from todo.models import ToDo


class ToDoListCreate(generics.ListCreateAPIView):
    # ListCreateAPIView requires two mandatory attributes: serializer_class and get_queryset.
    serializer_class = ToDoSerializer

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        # serializer holds a Django model
        serializer.save(user=self.request.user)