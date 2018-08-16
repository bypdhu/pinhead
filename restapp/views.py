from django.shortcuts import render
# from django.contrib.auth.models import User, Group
from myuser.models import User, UserGroup
from rest_framework import viewsets
from restapp.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = GroupSerializer
