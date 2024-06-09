
from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, GroupViewSet, FollowViewSet, PostViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('follow', FollowViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
