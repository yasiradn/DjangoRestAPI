from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins
from .serializers import PostSerializer
from .models import Post


class PostView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class YeTAnotherView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('id')
        res = super().delete(request,*args,**kwargs)
        if res.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(post_id))
        return res

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        if res.status_code == 200:
            from django.core.cache import cache
            post = res.data
            cache.set('post_data_{}'.format(post['id']), {
                'title': post['title'],
                'description': post['description'],
                'owner': post['owner']
            })
        return res