from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from main.models import Course, Lesson, Payment, Subscription
from main.paginators import CoursePaginator, LessonPaginator
from main.permissions import IsOwnerOrStaff, IsOwner, CustomCoursePermission
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [CustomCoursePermission]
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsOwnerOrStaff]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.exclude(owner__isnull=True)
        return queryset

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.exclude(owner__isnull=True)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", 'paid_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class SubscribeView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        serializer.save(user=self.request.user, course=course)

class UnsubscribeView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_object(self):
        user = self.request.user
        course_id = self.kwargs['course_id']
        try:
            subscription = Subscription.objects.get(user=user, course_id=course_id)
        except Subscription.DoesNotExist:
            return None
        return subscription

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            self.perform_destroy(instance)
            return Response({"detail": "Подписка отключена."}, status=status.HTTP_200_OK)
        return Response({"detail": "Подписка не найдена."}, status=status.HTTP_404_NOT_FOUND)