from django.urls import include, path

from rest_framework import routers

from .views import (CategoryViewSet,
                    CommentViewSet,
                    ClientProfileViewSet,
                    CustomUserViewSet,
                    ImageViewSet,
                    ServiceProfileViewSet,
                    ReviewViewSet,)

app_name = 'api'

router = routers.DefaultRouter()


router.register('users', CustomUserViewSet, basename='users')

router.register('category', CategoryViewSet)
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

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]