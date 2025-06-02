from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUser, LoginUser, BlogViewSet, LikePost, CommentPost

router = DefaultRouter()
router.register('posts', BlogViewSet, basename='post')

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('like/<int:pk>/', LikePost.as_view()),
    path('comment/<int:pk>/', CommentPost.as_view()),
    path('', include(router.urls)),
]
