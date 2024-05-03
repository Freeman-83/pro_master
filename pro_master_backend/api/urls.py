from django.urls import include, path

from rest_framework import routers

from .views import (AppointmentViewSet,
                    CategoryViewSet,
                    CommentViewSet,
                    ClientProfileViewSet,
                    CustomUserViewSet,
                    ImageViewSet,
                    ServiceProfileViewSet,
                    ScheduleViewSet,
                    ReviewViewSet,)

app_name = 'api'

router = routers.DefaultRouter()


router.register('users', CustomUserViewSet, basename='users')

router.register('categories', CategoryViewSet)
router.register('services', ServiceProfileViewSet)
router.register('clients', ClientProfileViewSet, basename='clients')
router.register(
    r'services/(?P<profile_id>\d+)/images',
    ImageViewSet,
    basename='images'
)
router.register(
    r'services/(?P<profile_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'services/(?P<profile_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'services/(?P<profile_id>\d+)/schedules',
    ScheduleViewSet,
    basename='schedules'
)
router.register(
    r'services/(?P<profile_id>\d+)/schedules/(?P<schedule_id>\d+)/appointments',
    AppointmentViewSet,
    basename='appointments'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]