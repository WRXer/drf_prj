from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentListAPIView, SubscribeView, UnsubscribeView

app_name = MainConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('subscribe/<int:course_id>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<int:course_id>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('course/<int:course_id>/payment/', PaymentCreateAPIView.as_view(), name='payment-create'),
] + router.urls