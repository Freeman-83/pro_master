from django.urls import include, path

from rest_framework import routers

from .views import (CategoryViewSet,
                    CommentViewSet,
                    ClientProfileViewSet,
                    CustomUserViewSet,
                    MasterProfileViewSet,
                    ReviewViewSet,
                    ServiceViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('services', ServiceViewSet)
router.register('category', CategoryViewSet)
router.register('users', CustomUserViewSet, basename='users')
router.register('clients', ClientProfileViewSet, basename='clients')
router.register('masters', MasterProfileViewSet, basename='masters')
router.register(
    r'services/(?P<service_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'services/(?P<service_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]