from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    
    def get_queryset(self):
        queryset = Post.objects.select_related('user').order_by('-timestamp')
        
        random_comments = self.request.query_params.get('random_comments', 'false').lower() == 'true'
        
        if random_comments:
            self.request.random_comments = True
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['random_comments'] = getattr(self.request, 'random_comments', False)
        return context
