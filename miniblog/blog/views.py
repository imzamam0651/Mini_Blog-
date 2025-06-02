from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Blog, Like, Comment
from .serializers import UserSerializer, BlogSerializer, LikeSerializer, CommentSerializer

# User Registration
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=201)
        return Response(serializer.errors, status=400)

# User Login
class LoginUser(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)

# Blog Views
class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'retrieve':
            return Blog.objects.filter(author=self.request.user)
        return Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        return super().destroy(request, *args, **kwargs)

# Like a blog post
class LikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            return Response({'message': 'Already liked'}, status=400)
        return Response({'message': 'Liked'}, status=201)

# Comment on a blog post
class CommentPost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


