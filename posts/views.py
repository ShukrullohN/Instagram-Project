
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostModel, PostCommentModel, PostLikeModel, CommentLikeModel
from posts.serializers import PostSerializer, CommentSerializer
from shared.custom_pagination import CustomPagination


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return PostCommentModel.objects.filter(post_id=post_id)


class PostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            print(serializer.validated_data)
        post_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, post_id=post_id)


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post_like = PostLikeModel.objects.filter(post_id=pk, user=self.request.user)
        if post_like.exists():
            post_like.delete()
            response = {
                "status": True,
                "message": "Successfully unliked"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            PostLikeModel.objects.create(post_id=pk, user=self.request.user)
            response = {
                "status": True,
                "message": "Successfully liked"
            }
            return Response(response, status=status.HTTP_200_OK)


class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            comment_like = CommentLikeModel.objects.get(comment_id=pk)
            comment_like.delete()
            response = {
                "status": True,
                "message": "Successfully unliked from comment"
            }
            return Response(response, status=status.HTTP_200_OK)
        except CommentLikeModel.DoesNotExist:
            CommentLikeModel.objects.create(
                comment_id=pk,
                user=self.request.user
            )
            response = {
                "status": True,
                "message": "Successfully liked"
            }
            return Response(response, status=status.HTTP_200_OK)
