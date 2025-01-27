from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Followers
from .serializers import FollowersSerializer


class FollowersList(generics.ListCreateAPIView):
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Followers.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowersDetail(generics.RetrieveDestroyAPIView):
    serializer_class = FollowersSerializer
    permission_classes =[IsOwnerOrReadOnly]
    queryset = Followers.objects.all()