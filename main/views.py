from django.shortcuts import render
from rest_framework import viewsets

from main.models import Course
from main.serializers import CourseSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()